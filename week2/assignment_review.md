# Week 2 Assignment Review: Prompt Quality → Code Quality

This document shows how **different prompt qualities** produce **different code**. Use this to evaluate your own work.

---

## Exercise 1: The LLM Function — Prompt Comparison

### ❌ Bad Prompt
> "Write a function that gets action items from text using AI"

**What Cursor generates (typical):**
```python
def extract_action_items_llm(text):
    response = chat(model="llama3.2", messages=[{"role": "user", "content": text}])
    return response.message.content.split("\n")
```

**Problems:**
- No type hints → hard to maintain
- No structured output → LLM might return `"Sure! Here are your tasks: 1. Buy milk..."` 
- Returns raw string split → `["Sure! Here are your tasks:", "1. Buy milk"]` (garbage)
- No error handling → app crashes if Ollama is down

---

### ✅ Good Prompt (applies K-shot + constraints)
> "I need a Python function `extract_action_items_llm(text: str) -> List[str]` in `week2/app/services/extract.py`.
> It should use the `ollama` library's `chat()` function with model `llama3.2`.
> **Constraint:** Use Pydantic `BaseModel` with `model_json_schema()` to force JSON output (see https://ollama.com/blog/structured-outputs).
> **Error handling:** Wrap the call in try/except — return `[]` on any failure.
> **Example:** Input: 'Buy milk and walk dog' → Output: `['Buy milk', 'Walk dog']`"

**What Cursor generates:**
```python
from pydantic import BaseModel
from typing import List
from ollama import chat

class ActionItems(BaseModel):
    items: List[str]

def extract_action_items_llm(text: str, model_name: str = "llama3.2") -> List[str]:
    prompt = f"Extract action items from: {text}"
    try:
        response = chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            format=ActionItems.model_json_schema(),
        )
        data = ActionItems.model_validate_json(response['message']['content'])
        return data.items
    except Exception as e:
        print(f"Error: {e}")
        return []
```

**Why it's better:**
- Type hints everywhere
- Pydantic schema forces valid JSON (no parsing nightmares)
- Error handling prevents crashes
- Configurable model name (not hardcoded)

---

## Exercise 2: Unit Tests — Prompt Comparison

### ❌ Bad Prompt
> "Write tests for my function"

**What Cursor generates:**
```python
def test_extract():
    result = extract_action_items_llm("Buy milk")
    assert len(result) > 0  # This calls REAL Ollama every time!
```

**Problems:**
- Calls real Ollama → slow (5-10 seconds per test)
- Non-deterministic → LLM might return different things each run
- No edge case coverage

### ✅ Good Prompt (applies Reflexion thinking)
> "Write `unittest` tests for `extract_action_items_llm` in `week2/tests/test_extract.py`.
> **Critical:** Use `unittest.mock.patch` to mock `week2.app.services.extract.chat`. Do NOT call real Ollama.
> Test cases:
> 1. Success: mock returns `{"items": ["Buy milk", "Walk dog"]}` → assert exact list
> 2. Empty: mock returns `{"items": []}` → assert `[]`
> 3. Error: mock raises `Exception("Ollama down")` → assert function returns `[]` gracefully"

**What Cursor generates:**
```python
from unittest.mock import patch
from week2.app.services.extract import extract_action_items_llm

class TestExtractLLM(unittest.TestCase):
    @patch('week2.app.services.extract.chat')
    def test_success(self, mock_chat):
        mock_chat.return_value = {'message': {'content': '{"items": ["Buy milk"]}'}}
        result = extract_action_items_llm("Buy milk")
        self.assertEqual(result, ["Buy milk"])

    @patch('week2.app.services.extract.chat')
    def test_error_graceful(self, mock_chat):
        mock_chat.side_effect = Exception("Ollama down")
        result = extract_action_items_llm("anything")
        self.assertEqual(result, [])
```

**Why it's better:**
- Mocked → runs in 0.1s, not 10s
- Deterministic → same result every time
- Tests error handling → proves the app won't crash

---

## Exercise 4: Agentic Mode — Prompt Comparison

### ❌ Bad Prompt
> "Add a button"

**Result:** Cursor might add a random button that does nothing, or wire it to the wrong endpoint.

### ✅ Good Prompt (applies context + specificity)
> "I have `extract_action_items_llm` in `week2/app/services/extract.py`. Please:
> 1. Add a POST endpoint `/action-items/extract-llm` in the router that accepts `{"text": "..."}` and returns the LLM extraction result
> 2. In `week2/app/frontend/index.html`, add an 'Extract with AI' button next to the existing Extract button
> 3. Wire the new button to call `/action-items/extract-llm` via fetch() and display results in the same list
> Match the existing code patterns and UI style."

**Result:** Cursor modifies both backend and frontend files correctly, matching existing patterns.

---

## How Week 1 Techniques Apply Here

| Week 1 Technique | How to Apply in Week 2 |
|---|---|
| **K-shot** | Provide input/output examples in your prompt: "Input: 'Buy milk' → Output: `['Buy milk']`" |
| **Chain-of-Thought** | Ask Cursor to "analyze the codebase first, then make changes" |
| **Self-Consistency** | Try the same prompt 2-3 times, pick the best generated code |
| **RAG** | Reference documentation URLs in your prompt (e.g., Ollama structured outputs blog) |
| **Reflexion** | If Cursor's code has bugs, paste the error back and ask it to fix |
| **Tool Calling** | Exercise 4 IS tool calling — the LLM uses Ollama as a "tool" |

---

## Self-Grading Checklist

1. [ ] Does `extract_action_items_llm` return `[]` on empty input?
2. [ ] Does it return `[]` when Ollama is turned off? (not crash)
3. [ ] Are unit tests instant (<0.5s)? → If slow, you're not mocking
4. [ ] Does the "Extract with AI" button work in the browser?
5. [ ] Did you document **specific, detailed prompts** in `writeup.md`? (not just "write code")
6. [ ] Does your README explain how to set up and run the project?

> **Scoring reminder:** Each exercise is worth 20 points — **10 for code, 10 for the prompt quality.** A perfect function with a lazy prompt = 50% score.
