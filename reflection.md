# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My design has four classes:

- **Task**: one care activity (like "Breakfast" or "Bathroom"). It holds a description, time, duration, priority, frequency (once, daily, weekly), due date, which pet it belongs to, and whether it is completed. It can mark itself complete.
- **Pet**: holds the pet's name and species plus a list of its tasks. It can add a task and return its tasks.
- **Owner**: holds the owner's name and a list of pets. It can add a pet and gather every task from all of its pets.
- **Scheduler**: the "brain". It takes an Owner, collects all tasks across pets, sorts them by time, filters them, detects conflicts, handles recurring tasks, and builds the daily schedule.

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler works with one Owner.

**b. Design changes**

My design changed in a few ways while I built it. First, I added a `pet_name` field to Task so the Scheduler can filter by pet and show which pet a task belongs to; `Pet.add_task()` sets it automatically. Second, I added a `due_date` field so recurring tasks can calculate their next date. Third, I added `Task.next_occurrence()` and had `Scheduler.mark_task_complete()` add the new task to the correct pet, which keeps the recurrence logic small and in one place.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers date, time, and whether a task is done. It sorts by date and then time, flags tasks at the same time, and can filter by pet or status. Priority and duration are stored and shown in the schedule, but they are not used to order tasks yet. I put time first because a pet owner mostly needs to know what comes next, and exact times are the simplest thing to sort and check correctly.

**b. Tradeoffs**

My scheduler only detects a conflict when two tasks have the exact same date and time. It does not check whether tasks overlap based on duration (for example, a 30-minute walk at 07:00 and a feeding at 07:15). This is reasonable for this scenario because pet care tasks are usually short and scheduled at set times, and an exact-match check is simple, easy to read, and easy to test. The cost is that it can miss real overlaps, so a future version could compare start and end times.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI chat assistant to work through the project one phase at a time: choosing the three core actions, drafting the UML in Mermaid, generating the class skeleton, and then building the logic, tests, and UI step by step. The most helpful prompts gave it the phase instructions and asked for complete code with short comments, because I am new to Python. I also pasted my terminal output back into the chat after each step so it could check that things worked before we moved on. I used one continuous chat for the whole project instead of separate sessions for each phase. That kept the context in one place, but it made the conversation long, so separate sessions would probably have been more organized.

**b. Judgment and verification**

I did not accept the AI's suggestions without adapting them. For example, I chose to use my own name (Ena) and my own pet (Pika) as the sample data instead of generic example names, so the demo reflects a real daily routine of bathroom breaks and meals. I also did not trust any code until I ran it: I checked the CLI output from `main.py`, ran all 11 pytest tests, and clicked through the Streamlit app to make sure pets and tasks stayed in memory and the conflict warnings appeared. When my app first showed the old starter page, I checked the actual contents of `app.py` in the terminal and found the new code had only been partly pasted, so I replaced the whole file.

---

## 4. Testing and Verification

**a. What you tested**

I tested sorting (tasks added out of order come back in time order), recurrence (daily tasks create a next-day task, weekly tasks create one 7 days later, one-time tasks create nothing), conflict detection (same-time tasks are flagged, different times are not, finished tasks are ignored), filtering by pet and status, and an edge case (a pet with no tasks). These matter because they are the "smart" parts of the app, and they are the easiest things to break without noticing.

**b. Confidence**

I'm fairly confident (4 out of 5) that the scheduler works for the normal cases, since all the tests pass. If I had more time, I would test overlapping durations (for example, a 30-minute walk starting at 07:00 and a feeding at 07:15), invalid time formats like "7:30" without the leading zero, and weekly tasks that cross a month or year boundary.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the logic layer worked on its own. I could check sorting, filtering, conflicts, and recurring tasks in the terminal and with 11 passing tests before the UI used them, and then the Streamlit app worked once it was connected.

**b. What you would improve**

I would make conflict detection check overlapping durations, use priority when ordering tasks, and save pets and tasks to a file so they survive closing the app.

**c. Key takeaway**

Building and testing the logic first made the UI step much easier. Even when AI writes a lot of the code, I still have to decide what the system should do, run it, and check the results myself.