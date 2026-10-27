from pawpal_system import Pet, Task


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