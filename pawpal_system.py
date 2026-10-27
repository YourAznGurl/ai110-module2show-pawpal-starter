from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List


@dataclass  # @dataclass auto-writes the setup code for a class that just holds data
class Task:
    """One care activity, like Breakfast or Bathroom."""
    description: str
    time: str                          # "HH:MM" like "07:30"
    duration_minutes: int = 10
    priority: str = "medium"           # "low", "medium", or "high"
    frequency: str = "once"            # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
    pet_name: str = ""                 # filled in automatically when added to a Pet
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self):
        """Return a new Task for the next day/week, or None if it doesn't repeat."""
        if self.frequency == "daily":
            days = 1
        elif self.frequency == "weekly":
            days = 7
        else:
            return None                # "once" tasks never repeat
        # replace() makes a copy of this task with a few fields changed.
        # timedelta(days=1) means "one day", so today + timedelta = tomorrow.
        return replace(self, due_date=self.due_date + timedelta(days=days), completed=False)


@dataclass
class Pet:
    """A pet and its list of tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)  # starts as an empty list

    def add_task(self, task: Task):
        """Add a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self):
        """Return this pet's tasks."""
        return self.tasks


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Collect tasks from every pet into one list."""
        all_tasks = []
        for pet in self.pets:                      # go through each pet
            all_tasks.extend(pet.get_tasks())      # add that pet's tasks to the big list
        return all_tasks


class Scheduler:
    """The brain: organizes and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self):
        """Ask the owner for every task across all pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self):
        """Return tasks in order: earliest date first, then earliest time."""
        # sorted() orders a list. The lambda tells it what to sort by:
        # each task's (date, time). "HH:MM" text sorts correctly as-is.
        return sorted(self.get_all_tasks(), key=lambda task: (task.due_date, task.time))

    def filter_tasks(self, pet_name=None, completed=None):
        """Return tasks matching a pet name and/or done status (None = ignore)."""
        tasks = self.sort_by_time()   # start from the sorted list so results stay in time order
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]   # keep one pet's tasks
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]  # keep done or not done
        return tasks

    def detect_conflicts(self):
        """Return warning messages for not-done tasks at the exact same date and time."""
        seen = {}          # remembers the first task found at each (date, time)
        warnings = []
        for task in self.get_all_tasks():
            if task.completed:
                continue                       # finished tasks can't conflict
            key = (task.due_date, task.time)
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Warning: {task.pet_name}'s {task.description} and "
                    f"{other.pet_name}'s {other.description} are both at {task.time} on {task.due_date}"
                )
            else:
                seen[key] = task
        return warnings                        # an empty list means no conflicts

    def mark_task_complete(self, task: Task):
        """Mark a task done; if it repeats, add the next one to the same pet."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            for pet in self.owner.pets:
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
        return next_task                       # None if the task doesn't repeat

    def generate_schedule(self):
        """Return all tasks sorted by date and time."""
        return self.sort_by_time()