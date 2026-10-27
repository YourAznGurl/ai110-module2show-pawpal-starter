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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
