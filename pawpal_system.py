from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass  # @dataclass auto-writes the boring setup code for a class that just holds data
class Task:
    """One care activity, like Breakfast or Bathroom."""
    description: str
    time: str                          # when it happens, written "HH:MM" like "07:30"
    duration_minutes: int = 10         # how long it takes
    priority: str = "medium"           # "low", "medium", or "high"
    frequency: str = "once"            # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)  # defaults to today's date
    pet_name: str = ""                 # which pet this task is for
    completed: bool = False            # False until it's done

    def mark_complete(self):
        # Will set completed to True (and later, make the next daily/weekly task)
        pass


@dataclass
class Pet:
    """A pet and its list of tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)  # starts as an empty list

    def add_task(self, task: Task):
        # Will add a task to this pet's list
        pass

    def get_tasks(self):
        # Will return this pet's tasks
        pass


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []      # starts as an empty list of pets

    def add_pet(self, pet: Pet):
        # Will add a pet to this owner
        pass

    def get_all_tasks(self):
        # Will collect tasks from every pet into one list
        pass


class Scheduler:
    """The brain: organizes and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self):
        # Will ask the owner for every task
        pass

    def sort_by_time(self):
        # Will return tasks in time order
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        # Will return only tasks matching a pet name and/or done status
        pass

    def detect_conflicts(self):
        # Will return warning messages for tasks at the same time
        pass

    def mark_task_complete(self, task: Task):
        # Will complete a task and create the next one if it repeats
        pass

    def generate_schedule(self):
        # Will build today's sorted schedule
        pass