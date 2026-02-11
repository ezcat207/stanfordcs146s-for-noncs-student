# Lecture Transcript: The Art of AI Code Review
**Date:** November 3, 2025  
**Topic:** Week 7 - AI-Assisted Code Review & Graphite  
**Based on:** Synthesized from Assignment Topics

---

## Slide 1: The Bottleneck of Software Engineering

"We've spent 6 weeks learning how to *write* code faster.
But any senior engineer will tell you: **Writing code is easy. Reading code is hard.**

The biggest bottleneck in modern teams isn't generating lines of code; it's **Code Review**.
Pull Requests (PRs) sit stale for days. Engineers context-switch to review 500 lines of diffs, miss bugs, and nitpick style.
It's a slow, painful, blocking process.
And now that we have AI agents writing code 10x faster, this bottleneck is about to explode."

---

## Slide 2: Enter the AI Reviewer

"What if the first line of defense wasn't a human, but an AI?
We aren't talking about a linter that checks indentation.
We are talking about a **Semantic Reviewer**.

An Agent that understands:
- 'This API change breaks backward compatibility.'
- 'You missed a null check here.'
- 'This variable name is confusing compared to the rest of the file.'

Tools like **Graphite** use LLMs to analyze your PRs *before* a human sees them. They act as the 'Junior Engineer' who does the first pass, letting the Senior Engineer focus on architecture and logic."

---

## Slide 3: Stacking PRs (The Workflow Change)

"To make this work, we need to change how we ship code.
The old way:
1.  Create big branch `feature-x`.
2.  Write 1000 lines.
3.  Open massive PR.
4.  Wait 3 days for review.

The **Stacked** way (popularized by Facebook/Uber and tools like Graphite):
1.  Create small branch `feat-part-1`.
2.  Open PR.
3.  Immediately branch off *that* branch (`feat-part-2`).
4.  Keep coding.

This creates a 'stack' of small, reviewable PRs. AI loves small PRs. It can reason about 50 lines much better than 5000."

---

## Slide 4: The Assignment - Agent vs. Agent

"This week, you are going to play a game of 'Agent vs. Agent'.
1.  You will use an **AI Coding Agent** (Cursor/Windsurf) to implement features.
2.  You will use an **AI Review Agent** (Graphite) to critique that code.
3.  **You** are the judge in the middle.

You will see firsthand:
- Does the Reviewer catch the Coder's bugs?
- Does the Reviewer hallucinate issues?
- Is the Coder 'lazy' (e.g., adding endpoints without validation), and does the Reviewer call it out?"

---

## Slide 5: The Future of Quality

"We are moving toward a world where 'LGTM' (Looks Good To Me) isn't just a rubber stamp.
It's a signed certificate from a suite of AI agents that have analyzed security, performance, and style.
Your job is understanding this pipeline. Because soon, you won't just be reviewing code; you'll be reviewing the reviews."

---

## Summary

This week:
- Sign up for Graphite.
- Implement 4 tasks using AI.
- Let Graphite review them.
- Compare the AI's feedback to your own.
This is meta-engineering at its finest."
