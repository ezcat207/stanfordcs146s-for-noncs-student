# Week 7 Review: The Human in the Loop

## 1. The "Blind Trust" Trap

### Mistake: Merging Graphite's Suggestions Without Thinking
**Symptom**: You see a green checkmark from the AI, so you hit merge. Then CI fails.
**The Reality**: AI Reviewers are great at syntax and pattern matching ("You missed a type hint"), but bad at *intent*.
- Graphite might suggest: "Remove this unused variable."
- Reality: That variable was there because you planned to use it in the next stacked PR. 
**Fix**: Treat Graphite as a Junior Engineer. Verify every suggestion.

---

## 2. The "Stacked PR" Confusion

### Mistake: Changing the Bottom of the Stack
**Symptom**: You edit Task 3 (Models) *after* you started Task 4 (Tests), and now Task 4 has merge conflicts.
**The Fix**:
- If you change the base, you must **restack**.
- Command: `gt stack submit --restack` (or `gt restack`).
- This rebases your upper branches onto the lower ones.

---

## 3. Testing Gaps (Task 4)

### Mistake: Testing the "Happy Path" Only
**Symptom**: You added pagination, and tested `limit=10`.
**The Review Comment**: "What happens if `limit=-1`? or `limit=999999`?"
**The Lesson**: AI is actually very good at spotting these edge cases. If Graphite brings it up, add a test for it (`tests/test_pagination.py`).

---

## 4. Self-Correction Checklist

1.  [ ] **Did I read the AI review?** (Don't just look at the score).
2.  [ ] **Did I restack?** (Ensure your PR chain is clean).
3.  [ ] **Did I add description?** (An empty PR description is a crime, even for AI).
