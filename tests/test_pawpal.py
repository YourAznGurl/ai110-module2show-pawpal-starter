from datetime import timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def make_scheduler():
    """Helper: build an owner with one pet, plus a scheduler for that owner."""
    owner = Owner("Ena")
    pet = Pet("Pika", "dog")
    owner.add_pet(pet)
    return Scheduler(owner), pet


# ---------- Original tests ----------

def test_mark_complete_changes_status():
    """Calling mark_complete() should flip completed to True."""
    task = Task("Breakfast", "07:30")
    assert task.completed is False      # starts as not done
    task.mark_complete()
    assert task.completed is True       # now it's done


def test_add_task_increases_task_count():
    """Adding a task to a Pet should make its task list one longer."""
    pet = Pet("Pika", "dog")
    assert len(pet.tasks) == 0          # starts empty
    pet.add_task(Task("Lunch", "12:30"))
    assert len(pet.tasks) == 1          # now has one


# ---------- Sorting ----------

def test_sort_by_time_is_chronological():
    """Tasks added out of order should come back earliest first."""
    scheduler, pet = make_scheduler()
    pet.add_task(Task("Dinner", "18:00"))
    pet.add_task(Task("Breakfast", "07:30"))
    pet.add_task(Task("Lunch", "12:30"))

    times = [task.time for task in scheduler.sort_by_time()]
    assert times == ["07:30", "12:30", "18:00"]


# ---------- Recurring tasks ----------

def test_daily_task_creates_next_day_task():
    """Completing a daily task should add a new, not-done task for tomorrow."""
    scheduler, pet = make_scheduler()
    task = Task("Breakfast", "07:30", frequency="daily")
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.completed is False
    assert len(pet.tasks) == 2          # the original plus the new one


def test_weekly_task_creates_task_seven_days_later():
    """Completing a weekly task should add a new task 7 days later."""
    scheduler, pet = make_scheduler()
    task = Task("Grooming", "10:00", frequency="weekly")
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert next_task.due_date == task.due_date + timedelta(days=7)


def test_once_task_does_not_repeat():
    """Completing a one-time task should NOT create a new task."""
    scheduler, pet = make_scheduler()
    task = Task("Vet visit", "09:00", frequency="once")
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert next_task is None
    assert len(pet.tasks) == 1


# ---------- Conflict detection ----------

def test_conflict_detection_flags_same_time():
    """Two not-done tasks at the same date and time should create a warning."""
    scheduler, pet = make_scheduler()
    pet.add_task(Task("Breakfast", "07:30"))
    pet.add_task(Task("Medication", "07:30"))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "07:30" in warnings[0]


def test_no_conflict_when_times_differ():
    """Tasks at different times should produce no warnings."""
    scheduler, pet = make_scheduler()
    pet.add_task(Task("Breakfast", "07:30"))
    pet.add_task(Task("Lunch", "12:30"))

    assert scheduler.detect_conflicts() == []


def test_completed_task_does_not_conflict():
    """A finished task shouldn't count as a conflict."""
    scheduler, pet = make_scheduler()
    first = Task("Breakfast", "07:30")
    pet.add_task(first)
    pet.add_task(Task("Medication", "07:30"))
    first.mark_complete()

    assert scheduler.detect_conflicts() == []


# ---------- Edge cases and filtering ----------

def test_pet_with_no_tasks():
    """A pet with no tasks should give an empty schedule and no warnings."""
    scheduler, pet = make_scheduler()

    assert scheduler.generate_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_filter_by_pet_and_status():
    """filter_tasks should narrow tasks by pet name and by done status."""
    scheduler, pika = make_scheduler()
    mochi = Pet("Mochi", "cat")
    scheduler.owner.add_pet(mochi)

    breakfast = Task("Breakfast", "07:30")
    pika.add_task(breakfast)
    pika.add_task(Task("Lunch", "12:30"))
    mochi.add_task(Task("Feeding", "08:00"))
    breakfast.mark_complete()

    assert len(scheduler.filter_tasks(pet_name="Pika")) == 2
    assert len(scheduler.filter_tasks(completed=True)) == 1
    assert len(scheduler.filter_tasks(pet_name="Mochi", completed=True)) == 0