from dataclasses import dataclass, field
from datetime import date
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
        """(Phase 4) Return tasks in time order."""
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        """(Phase 4) Return tasks matching a pet name and/or done status."""
        pass

    def detect_conflicts(self):
        """(Phase 4) Return warnings for tasks at the same time."""
        pass

    def mark_task_complete(self, task: Task):
        """(Phase 4 adds recurring) Mark a task complete."""
        task.mark_complete()

    def generate_schedule(self):
        """Return all tasks sorted by time, earliest first."""
        # sorted() puts them in order; the lambda says "sort by each task's time"
        return sorted(self.get_all_tasks(), key=lambda task: task.time)