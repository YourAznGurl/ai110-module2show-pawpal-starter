from pawpal_system import Owner, Pet, Task, Scheduler


def show(title, tasks):
    """Print a list of tasks neatly under a title."""
    print(f"\n{title}")
    print("-" * 60)
    if not tasks:
        print("(none)")
    for task in tasks:
        box = "[x]" if task.completed else "[ ]"   # done or not done
        print(f"{box} {task.due_date} {task.time}  {task.pet_name:<6} "
              f"{task.description:<10} ({task.frequency})")


# Make the owner and two pets
owner = Owner("Ena")
pika = Pet("Pika", "dog")
mochi = Pet("Mochi", "cat")
owner.add_pet(pika)
owner.add_pet(mochi)

# Add tasks OUT OF ORDER on purpose, so sorting has something to fix
breakfast = Task("Breakfast", "07:30", 10, "high", "daily")
pika.add_task(Task("Dinner", "18:00", 10, "high", "daily"))
pika.add_task(breakfast)
pika.add_task(Task("Lunch", "12:30", 10, "medium"))
pika.add_task(Task("Bathroom", "07:00", 10, "high"))
mochi.add_task(Task("Play time", "19:00", 15, "low"))
mochi.add_task(Task("Feeding", "07:30", 5, "high"))   # same time as Pika's breakfast = conflict!

scheduler = Scheduler(owner)

# 1. Before sorting (the order we added them)
show("1. Unsorted (order added)", scheduler.get_all_tasks())

# 2. Sorted by time
show("2. Sorted by time", scheduler.sort_by_time())

# 3. Filter by pet
show("3. Only Pika's tasks", scheduler.filter_tasks(pet_name="Pika"))

# 4. Conflict detection
print("\n4. Conflict check")
print("-" * 60)
warnings = scheduler.detect_conflicts()
if warnings:
    for warning in warnings:
        print(warning)
else:
    print("No conflicts found.")

# 5. Recurring task: finishing a daily task creates tomorrow's
next_task = scheduler.mark_task_complete(breakfast)
print(f"\n5. Completed Pika's Breakfast. Next one created for {next_task.due_date}")

show("6. Done tasks", scheduler.filter_tasks(completed=True))
show("7. Not done tasks (sorted)", [t for t in scheduler.sort_by_time() if not t.completed])