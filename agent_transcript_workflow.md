# Agent Workflow: The Week 2 Content Pipeline

This document outlines the standard operating procedure (SOP) for an AI Agent to generate the complete educational package for a Modern Software Development course module.

The pipeline consists of three phases, designed to take a student from raw lectures to completing the assignment.

---

## Phase 1: The Lecture Transcript
**Goal**: Convert raw slides and code demos into an engaging, readable lecture for a specific audience.

- **Inputs**:
    - `Lecture_Slides.pptx` (Source of truth for topics)
    - `demo_code.py` (Source of truth for implementation)
- **Process**:
    1.  **Extract Text**: Pull raw text from slides.
    2.  **Analyze Code**: Read `demo_code.py`. Identify the "Story" of the code (Imports -> Setup -> Logic).
    3.  **Synthesize**: logical flow.
        - *Introduction*: Hook the reader.
        - *Slide-by-Slide*: Expand bullet points into full paragraphs.
        - *Code Walkthrough*: Stop at relevant slides and explain the code line-by-line.
        - *Analogy*: Use a consistent analogy (e.g., "AI is a Chef", "MCP is USB").
- **Target Output Effect**:
    - The student feels like they are in the room. Complex code feels simple because of the analogies.
- **Reference (The Gold Standard)**:
    - See `week2/slides/mcp_lecture_transcript.md` for an example of how to weave `simple_mcp.py` into `Lecture_10_3.pptx`.
    - See `week2/slides/lecture_transcript_detailed.md` for the coding agent example.

---

## Phase 2: The Assignment Bridge
**Goal**: Connect the high-level concepts from Phase 1 to the specific tasks in the homework.

- **Inputs**:
    - `assignment.md` (The tasks)
    - Phase 1 Transcripts (The context)
- **Process**:
    1.  **Identify the Gap**: Lecture said "Build an Agent" -> Assignment says "Extract Todos".
    2.  **Create Mapping**:
        - Lecture "Tool" = Assignment "Extract Function".
        - Lecture "Testing" = Assignment "Unit Tests".
        - Lecture "Cursor" = Assignment "Agentic Mode".
    3.  **Explain the Environment**:
        - Explicitly list setup steps (Conda, Poetry, Ollama).
    4.  **Explain the Code Structure**:
        - Walk through the directory tree (`apps/`, `services/`, `tests/`).
- **Target Output Effect**:
    - The student stops panicking. They see exactly *where* in the complex codebase they need to touch.
- **Reference (The Gold Standard)**:
    - See `week2/assignment_bridge_transcript.md`.

---

---

## Phase 3: The Reference Solution Generation
**Goal**: Create a perfect, production-quality implementation of the assignment to serve as the answer key.

- **Inputs**:
    - `assignment.md` (Requirements)
    - `python` environment (Tools)
- **Process**:
    1.  **Scaffold**: If starting from scratch, create the folder structure (`app/`, `tests/`).
    2.  **Test-Driven Development (TDD)**:
        - Write the test first (e.g., `test_extract.py` failing because function doesn't exist).
        - Mock external dependencies (Ollama) immediately.
    3.  **Implement Core Logic**:
        - Write the Pydantic models.
        - Write the LLM integration code (`extract.py`).
    4.  **Verify**:
        - Run `pytest`. All green?
        - Manual sanity check (run the app and curl the endpoint).
- **Target Output Effect**:
    - A clean, well-commented codebase in `week2/solution/` that acts as the source of truth.
- **Reference (The Gold Standard)**:
    - See `week2/solution/app/services/extract.py`.
    - See `week2/solution/tests/test_extract.py`.

---

## Phase 4: The Review & Solution
**Goal**: Validate the student's attempt and correct misconceptions.

- **Inputs**:
    - `solution/` (Reference code from Phase 3)
- **Process**:
    1.  **Explain the "Why"**: Why did we use Pydantic? (Structured outputs). Why did we use Mocking? (Speed/Reliability).
    2.  **Identify Anti-Patterns**:
        - "Lazy Prompting" (Just asking "Find todos").
        - "Hardcoding".
        - "No Error Handling".
    3.  **Provide a Checklist**: A simple [ ] list for the student to self-grade.
- **Target Output Effect**:
    - The student learns *professional* engineering standards, moving beyond "it just works".
- **Reference (The Gold Standard)**:
    - See `week2/assignment_review.md`.

---

## Summary of Deliverables

| Phase | Artifact Name | Purpose |
| :--- | :--- | :--- |
| **1** | `*_transcript.md` | Teach Concepts |
| **2** | `*_bridge_transcript.md` | Contextualize Assignment |
| **3** | `solution/` codebase | Source of Truth |
| **4** | `*_review.md` | Corrigé & Best Practices |
