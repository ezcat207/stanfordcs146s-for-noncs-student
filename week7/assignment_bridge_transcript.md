# Week 7 Bridge: The AI Code Review Workflow

**Target Audience:** 18-year-old student who knows how to code but has never done "Real" code review.
**Goal:** Explain how to use **Graphite** to stack PRs and leverage AI for review.

---

## 1. The Setup (Graphite)

"Before you write a single line of code, you need to set up your reviewer.

1.  **Sign Up**: Go to graphite.dev and sign up.
2.  **Install CLI**: `brew install graphite-cli` (or npm).
3.  **Auth**: Run `gt auth`.
4.  **Repo**: Go to your `week7` folder and run `gt repo init`.

**Why?** Graphite replaces `git` for us. Instead of `git checkout -b`, we use `gt create`. It handles the messy stacking logic for you."

---

## 2. Task 1: The "Lazy" Endpoint (And how to catch it)

**The Task:** "Add more endpoints and validations."
**Your Move:**
1.  Open `app/routers/notes.py`.
2.  Ask Cursor: "Add a POST endpoint to create a note."
3.  **The Catch**: Cursor might forget input validation (e.g., empty title).
4.  **The Review**:
    - Commit (`gt commit -m "Add create note"`).
    - Submit (`gt submit`).
    - **Wait for Graphite**.
    - If Graphite says "Missing validation for empty strings", **it wins**. Fix it.

---

## 3. Task 2: Extraction Logic (Regex vs. semantics)

**The Task:** "Enhance extraction logic."
**Context**: Currently, `services/extract.py` uses simple Regex to find "TODO:".
**Your Move:**
1.  Ask Cursor to make it smarter. Maybe handle "FIXME" or "[ ]".
2.  **The Review**:
    - Does Graphite catch edge cases? "What if the TODO is inside a string literal?"
    - Compare your manual review notes with Graphite's.

---

## 4. Tasks 3 & 4: The Stacked PR

"This is where the magic happens.
You don't wait for Task 3 to be merged before starting Task 4.

1.  Finish Task 3 (Database Models). `gt submit`.
2.  **Immediately** run `gt create task-4-tests`.
3.  Start writing tests that *depend* on the new models from Task 3.
4.  Graphite manages the dependency. If you change Task 3, it updates Task 4 automatically.
5.  This is how Senior Engineers ship fast."

---

## 5. The Deliverable: The "vs" Report

"The most important part of this assignment isn't the code. It's the `writeup.md`.
I want to see screenshots of Graphite roasting your code.
I want to see instances where **you** caught something Graphite missed.
That difference—between what the AI sees and what you see—is your value as an engineer."
