import streamlit as st
from datetime import time as dtime   # used for the time picker

# Bring in the classes you built in pawpal_system.py
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Little icons so priority is easy to scan in the table
PRIORITY_ICONS = {"high": "🔴 high", "medium": "🟡 medium", "low": "🟢 low"}

# session_state is Streamlit's "memory". This makes the Owner ONE time,
# then reuses it on every re-run instead of creating a fresh empty one.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Ena")

owner = st.session_state.owner   # shortcut so we can type "owner"

# ---------- Owner ----------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

# ---------- Add a pet ----------
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Pika")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing_names = [pet.name for pet in owner.pets]
    if pet_name.strip() == "":
        st.warning("Please type a pet name.")
    elif pet_name.strip() in existing_names:
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(pet_name.strip(), species))   # calls your Owner.add_pet
        st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------- Add a task ----------
st.subheader("Add a Task")

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
    st.info("Add a pet first, then you can add tasks.")

st.divider()

# One Scheduler for the rest of the page (it just reads the owner's data)
scheduler = Scheduler(owner)

# ---------- Mark a task complete ----------
st.subheader("Mark a Task Complete")

pending = scheduler.filter_tasks(completed=False)   # only tasks that aren't done yet
if pending:
    labels = [f"{t.due_date} {t.time} - {t.pet_name}: {t.description}" for t in pending]
    choice = st.selectbox("Pick a task", labels)

    if st.button("Mark complete"):
        task = pending[labels.index(choice)]          # find the task that matches the choice
        next_task = scheduler.mark_task_complete(task)  # your Scheduler logic (handles repeats)
        if next_task is not None:
            st.success(f"Done! Next {task.frequency} {task.description} is set for {next_task.due_date}.")
        else:
            st.success("Done!")
else:
    st.info("Nothing to complete right now.")

st.divider()

# ---------- Today's schedule ----------
st.subheader("Today's Schedule")

all_tasks = scheduler.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add some above.")
else:
    # Conflict warnings come first so the owner sees them right away
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for message in conflicts:
            st.warning(message + ". Consider moving one of them.")
    else:
        st.success("No scheduling conflicts. You're all set!")

    # Filters: pick a pet and/or a status
    col_a, col_b = st.columns(2)
    with col_a:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with col_b:
        status_filter = st.selectbox("Show status", ["All", "Not done", "Done"])

    # Turn the dropdown choices into what filter_tasks expects (None means "don't filter")
    pet_arg = None if pet_filter == "All pets" else pet_filter
    status_arg = {"All": None, "Not done": False, "Done": True}[status_filter]
    shown = scheduler.filter_tasks(pet_name=pet_arg, completed=status_arg)

    st.caption(f"Showing {len(shown)} of {len(all_tasks)} tasks, sorted by date and time.")

    # Turn each Task into a row the table can show
    rows = [
        {
            "Done": "✅" if task.completed else "⬜",
            "Date": str(task.due_date),
            "Time": task.time,
            "Pet": task.pet_name,
            "Task": task.description,
            "Minutes": task.duration_minutes,
            "Priority": PRIORITY_ICONS[task.priority],
            "Repeats": task.frequency,
        }
        for task in shown
    ]
    st.table(rows)