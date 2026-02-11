# Week 2 Comprehensive Guide: From Zero to Agent

**Target Audience:** 18-year-old beginner.
**Goal:** Use AI (Cursor / Antigravity) to build an LLM-powered Action Item Extractor — learning **prompt engineering** along the way.

---

## Part 1: Setting Up Your Workshop (Environment)

### 1.1 Conda Environment
```bash
conda create -n cs146s python=3.11 -y
conda activate cs146s
```
*Check:* Your prompt should show `(cs146s)`.

### 1.2 Poetry (Dependency Manager)
```bash
pip install poetry
```
Go to the project folder `week2` and install dependencies:
```bash
poetry install
```

> **Troubleshooting:** If you encounter a `ModuleNotFoundError` (e.g., missing `fastapi`, `uvicorn`, etc.), manually install:
> ```bash
> pip install <package_name>
> ```

### 1.3 Ollama (The AI Brain)
1.  Download from [ollama.com](https://ollama.com) and run the app.
2.  Pull a model:
    ```bash
    ollama pull llama3.2
    ```
    *Check:* `ollama list` should show `llama3.2`.

> **Alternative: Cloud Models**
> If your computer can't run local models, use cloud-based models:
> 1. Run `ollama list` and look for models ending with `-cloud` (e.g., `deepseek-v3.1:671b-cloud`)
> 2. When writing your prompt for Cursor, specify this model name instead of `llama3.2`
> 3. Cloud models don't need to be "pulled" — they run on remote servers

---

## Part 2: Verify Your Environment

```bash
poetry run uvicorn week2.app.main:app --reload
```
Open `http://127.0.0.1:8000`. Type "Buy milk" and click **Extract**. If you see results, your environment is ready.

---

## Part 3: The Assignment — Prompt-First Workflow

> **Core Idea:** This assignment is NOT about writing code by hand. It's about **crafting good prompts** for Cursor (or Antigravity) and evaluating what the AI generates. Think of yourself as a **manager** giving instructions to an AI engineer.

> **Remember Week 1:** You practiced K-shot prompting, Chain-of-Thought, Self-Consistency, RAG, and Reflexion. Those same principles apply here — the more specific, structured, and contextual your prompt, the better the generated code.

### Exercise 1: Scaffold a New Feature (`extract_action_items_llm`)

**What you're building:** A function that calls an LLM (via Ollama) to intelligently extract action items from text, replacing the dumb regex approach.

**How to do it:** Open Cursor, press `Cmd+L`, and write a prompt. Here's the strategy:

1. **Read the existing code first.** Open `week2/app/services/extract.py` and understand `extract_action_items()`.
2. **Craft your prompt for Cursor.** Apply Week 1 techniques:
   - **Be specific** (like K-shot: give examples of input → output)
   - **Add constraints** (like Chain-of-Thought: tell the AI to think step by step about error handling)
   - **Provide context** (like RAG: reference the Ollama docs on structured outputs)

**Example prompt structure** (adapt to your own words):
> "Look at the existing `extract_action_items()` in `week2/app/services/extract.py`.
> I need a new function `extract_action_items_llm(text: str) -> List[str]` that:
> 1. Uses the `ollama` Python library's `chat()` function
> 2. Uses Pydantic `BaseModel` with `model_json_schema()` to force structured JSON output (see https://ollama.com/blog/structured-outputs)
> 3. Handles errors gracefully — if Ollama is down, return an empty list
> 4. Uses model `llama3.2` (or `deepseek-v3.1:671b-cloud` for cloud)"

3. **Review & Apply** what Cursor generates. Don't blindly accept — check if it matches your intent.
4. **Document your prompt** in `writeup.md` under Exercise 1.

### Exercise 2: Add Unit Tests

**What you're building:** Tests that verify your LLM function works — **without** calling the real Ollama API.

**How to do it:** Prompt Cursor to write tests. The key concept is **mocking**:

**Example prompt structure:**
> "Write `unittest` tests for `extract_action_items_llm` in `week2/tests/test_extract.py`.
> **Critical constraint:** Do NOT call the real Ollama API. Use `unittest.mock.patch` to mock `week2.app.services.extract.chat`.
> Test these cases:
> 1. Normal input → returns expected items
> 2. Empty input → returns empty list
> 3. Ollama crashes → function handles gracefully, returns `[]`"

**Verify:** Run `poetry run pytest week2/tests/test_extract.py` — all tests should pass in under 1 second (if they're slow, you're not mocking correctly).

### Exercise 3: Refactor Existing Code

**What you're building:** Cleaner, more professional code across the backend.

**How to do it:** This is where **Chain-of-Thought prompting** shines — ask Cursor to analyze before acting:

**Example prompt structure:**
> "Analyze the `week2/app/` codebase. As a senior Python engineer, identify and fix:
> 1. Missing Pydantic schemas for API request/response contracts
> 2. Database layer issues (raw SQL vs. parameterized queries)
> 3. Missing error handling on endpoints
> 4. Any code style inconsistencies
> Explain each change you make with inline comments."

### Exercise 4: Agentic Mode — Full-Stack Feature

**What you're building:** A new `/extract-llm` endpoint + "Extract with AI" button in the frontend + a "List Notes" feature.

**How to do it:** This is **Agentic Mode** — you give Cursor a high-level goal and it modifies multiple files:

**Example prompt structure:**
> "I have `extract_action_items_llm` in `week2/app/services/extract.py`.
> Please:
> 1. Create a new POST endpoint `/action-items/extract-llm` in the router that calls this function
> 2. Update `week2/app/frontend/index.html` to add an 'Extract with AI' button next to the existing one
> 3. Also add a 'List Notes' button that calls GET `/action-items` and displays results
> Match the existing code style and UI design."

### Exercise 5: Generate a README

**What you're building:** A `README.md` that documents the entire project.

**Example prompt:**
> "@Codebase Generate a README.md for this project. Include: project overview, setup instructions (Conda, Poetry, Ollama), how to run the server, API endpoints, and how to run tests."

---

## Part 4: What the Finished Product Looks Like

When you're done, your app at `http://127.0.0.1:8000` should have:

1. **Original "Extract" button** — uses the old regex-based extraction
2. **New "Extract with AI" button** — calls your LLM-powered function, producing much smarter results
3. **"List Notes" button** — displays all previously saved notes

**Example interaction:**
- Input: *"Tomorrow I need to email the boss, fix the login bug, and buy groceries after work"*
- Old Extract: might only catch "fix the login bug" (if it matches a keyword)
- **AI Extract:** returns `["Email the boss", "Fix the login bug", "Buy groceries"]` — because the LLM *understands* natural language

**Your tests** should all pass:
```bash
poetry run pytest week2/tests/test_extract.py
# Expected: 3 passed in ~0.1s
```

---

## Deliverables Checklist
- [ ] `writeup.md` — filled with your **actual prompts** and generated code locations
- [ ] `extract.py` — contains working `extract_action_items_llm()`
- [ ] `test_extract.py` — contains mocked unit tests (all passing)
- [ ] Refactored backend code with comments
- [ ] New endpoint + updated frontend
- [ ] Generated `README.md`

> **Remember:** You're graded 50% on code, 50% on prompts. A lazy prompt like *"write code"* will lose you points. A structured, context-rich prompt demonstrates mastery.
