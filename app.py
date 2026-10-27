import streamlit as st
from datetime import time as dtime   # used for the time picker

# Bring in the classes you built in pawpal_system.py
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

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

# ---------- Today's schedule ----------
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()   # calls your Scheduler logic

    if schedule:
        # Turn each Task into a row the table can show
        rows = [
            {
                "Time": task.time,
                "Pet": task.pet_name,
                "Task": task.description,
                "Minutes": task.duration_minutes,
                "Priority": task.priority,
                "Repeats": task.frequency,
            }
            for task in schedule
        ]
        st.table(rows)
    else:
        st.info("No tasks yet. Add some above.")