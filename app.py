import streamlit as st
from datetime import time as dtime   # used for the time picker

# Bring in the classes you built in pawpal_system.py
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Little icons so priority is easy to scan in the table
PRIORITY_ICONS = {"high": "🔴 high", "medium": "🟡 medium", "low": "🟢 low"}

# session_state is Streamlit's "memory".
# "owners" is a dictionary: each owner's name -> that owner's Owner object.
# Every Owner keeps its OWN list of pets, so pets never get mixed up.
if "owners" not in st.session_state:
    st.session_state.owners = {"Ena": Owner("Ena")}

owners = st.session_state.owners   # shortcut so we can type "owners"

# ---------- Owners ----------
st.subheader("Owners")

# A form lets you press Enter OR click the button to submit
with st.form("owner_form", clear_on_submit=True):
    new_owner_name = st.text_input("New owner name")
    add_owner_clicked = st.form_submit_button("Add owner")

if add_owner_clicked:
    name = new_owner_name.strip()
    if name == "":
        st.warning("Please type an owner name.")
    elif name in owners:
        st.warning(f"{name} already exists.")
    else:
        owners[name] = Owner(name)                # makes a brand-new Owner with no pets
        st.session_state.current_owner = name     # switch the dropdown to the new owner
        st.success(f"Added owner {name}!")

# Pick whose pets and tasks you are adding to
current_name = st.selectbox("Current owner", list(owners.keys()), key="current_owner")
owner = owners[current_name]   # the Owner object for the selected name

st.divider()

# ---------- Add a pet ----------
st.subheader(f"Add a Pet for {owner.name}")

with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Pika")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    existing_names = [pet.name for pet in owner.pets]   # only this owner's pets
    if pet_name.strip() == "":
        st.warning("Please type a pet name.")
    elif pet_name.strip() in existing_names:
        st.warning(f"{pet_name} is already one of {owner.name}'s pets.")
    else:
        owner.add_pet(Pet(pet_name.strip(), species))   # calls your Owner.add_pet
        st.success(f"Added {pet_name} to {owner.name}'s pets!")

# Show every pet and which owner it belongs to
pet_rows = [
    {"Pet": pet.name, "Species": pet.species, "Owner": owner_obj.name}
    for owner_obj in owners.values()   # go through each owner
    for pet in owner_obj.pets          # then each of that owner's pets
]
if pet_rows:
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------- Add a task ----------
st.subheader(f"Add a Task for {owner.name}'s Pets")

if owner.pets:
    chosen_pet = st.selectbox("Which pet?", [pet.name for pet in owner.pets])
    task_title = st.text_input("Task title", value="Breakfast")

    col1, col2, col3, col4 = st.columns(4)   # puts 4 inputs side by side
    with col1:
        task_time = st.time_input("Time", value=dtime(7, 30))
    with col2:
        duration = st.number_input("Minutes", min_value=1, max_value=240, value=10)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])

    if st.button("Add task"):
        new_task = Task(
            description=task_title,
            time=task_time.strftime("%H:%M"),   # turns 7:30 into the text "07:30"
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
        )
        for pet in owner.pets:
            if pet.name == chosen_pet:
                pet.add_task(new_task)           # calls your Pet.add_task
        st.success(f"Added {task_title} for {chosen_pet}!")
else:
    st.info(f"{owner.name} has no pets yet. Add a pet first, then you can add tasks.")

st.divider()

# ---------- Mark a task complete (all owners) ----------
st.subheader("Mark a Task Complete")

# Collect every not-done task from EVERY owner, as (owner, task) pairs
pending = [
    (owner_obj, task)
    for owner_obj in owners.values()
    for task in Scheduler(owner_obj).filter_tasks(completed=False)
]

if pending:
    labels = [
        f"{o.name} | {t.due_date} {t.time} - {t.pet_name}: {t.description}"
        for o, t in pending
    ]
    choice = st.selectbox("Pick a task", labels)

    if st.button("Mark complete"):
        task_owner, task = pending[labels.index(choice)]   # the owner and task that match the choice
        next_task = Scheduler(task_owner).mark_task_complete(task)  # your logic (handles repeats)
        if next_task is not None:
            st.success(f"Done! Next {task.frequency} {task.description} is set for {next_task.due_date}.")
        else:
            st.success("Done!")
else:
    st.info("Nothing to complete right now.")

st.divider()

# ---------- Today's schedule (all owners) ----------
st.subheader("Today's Schedule")

# Every task from every owner, as (owner name, task) pairs
all_pairs = [
    (owner_obj.name, task)
    for owner_obj in owners.values()
    for task in Scheduler(owner_obj).get_all_tasks()
]

if not all_pairs:
    st.info("No tasks yet. Add some above.")
else:
    # Conflict warnings: checked for each owner separately
    # (two different people can do things at the same time)
    found_conflict = False
    for owner_obj in owners.values():
        for message in Scheduler(owner_obj).detect_conflicts():
            st.warning(f"{message} (owner: {owner_obj.name}). Consider moving one of them.")
            found_conflict = True
    if not found_conflict:
        st.success("No scheduling conflicts. You're all set!")

    # Filters: owner, pet, and status
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        owner_filter = st.selectbox("Show owner", ["All owners"] + list(owners.keys()))
    with col_b:
        all_pet_names = sorted({p.name for o in owners.values() for p in o.pets})
        pet_filter = st.selectbox("Show pet", ["All pets"] + all_pet_names)
    with col_c:
        status_filter = st.selectbox("Show status", ["All", "Not done", "Done"])

    # Turn the dropdown choices into what filter_tasks expects (None means "don't filter")
    pet_arg = None if pet_filter == "All pets" else pet_filter
    status_arg = {"All": None, "Not done": False, "Done": True}[status_filter]

    # Use your Scheduler's filter for each owner, then combine the results
    shown = []
    for owner_obj in owners.values():
        if owner_filter != "All owners" and owner_obj.name != owner_filter:
            continue   # skip owners we aren't showing
        for task in Scheduler(owner_obj).filter_tasks(pet_name=pet_arg, completed=status_arg):
            shown.append((owner_obj.name, task))

    # Sort the combined list by date, then time (pair[1] is the task)
    shown.sort(key=lambda pair: (pair[1].due_date, pair[1].time))

    st.caption(f"Showing {len(shown)} of {len(all_pairs)} tasks across all owners, sorted by date and time.")

    # Turn each (owner, task) pair into a row the table can show
    rows = [
        {
            "Done": "✅" if task.completed else "⬜",
            "Date": str(task.due_date),
            "Time": task.time,
            "Owner": owner_name,
            "Pet": task.pet_name,
            "Task": task.description,
            "Minutes": task.duration_minutes,
            "Priority": PRIORITY_ICONS[task.priority],
            "Repeats": task.frequency,
        }
        for owner_name, task in shown
    ]
    st.table(rows)