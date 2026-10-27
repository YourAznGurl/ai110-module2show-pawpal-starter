from pawpal_system import Owner, Pet, Task, Scheduler

# Make the owner (you!)
owner = Owner("Ena")

# Make two pets (change the species if needed)
pika = Pet("Pika", "dog")
mochi = Pet("Mochi", "cat")

# Add the pets to the owner
owner.add_pet(pika)
owner.add_pet(mochi)

# Add tasks to Pika (each has a description, time, duration, priority)
pika.add_task(Task("Bathroom", "07:00", 10, "high"))
pika.add_task(Task("Breakfast", "07:30", 10, "high"))
pika.add_task(Task("Bathroom", "12:00", 10, "high"))
pika.add_task(Task("Lunch", "12:30", 10, "medium"))
pika.add_task(Task("Bathroom", "17:30", 10, "high"))
pika.add_task(Task("Dinner", "18:00", 10, "high"))

# Add a couple of tasks to Mochi
mochi.add_task(Task("Feeding", "08:00", 5, "high"))
mochi.add_task(Task("Play time", "19:00", 15, "low"))

# Ask the Scheduler to build today's schedule
scheduler = Scheduler(owner)
schedule = scheduler.generate_schedule()

# Print it neatly
print(f"Today's Schedule for {owner.name}")
print("-" * 50)
for task in schedule:
    box = "[x]" if task.completed else "[ ]"   # shows done or not done
    print(f"{box} {task.time}  {task.pet_name:<6} {task.description:<10} "
          f"({task.duration_minutes} min, {task.priority})")