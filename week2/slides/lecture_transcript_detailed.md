# Lecture Transcript: Building a Coding Agent from Scratch

**Date:** September 29, 2025  
**Topic:** Week 2 - Agents & Tools  
**Based on:** `Lecture_9_29_25_public.pptx` and `coding_agent_from_scratch_lecture.py`

---

## Slide 1: Introduction

"Good morning everyone, and welcome back to Modern Software Development. Today, we are tackling one of the most exciting topics in AI right now: **Building a Coding Agent from Scratch**.

You've probably used ChatGPT or Claude to ask questions. You might have even pasted some code and asked for a fix. That's a passive interaction. Today, we are going to change that. We are going to build a system where the AI doesn't just talk—it *acts*. It will read your files, understand your project structure, and even edit your code directly. We call this an 'Agent'.

And the best part? We are going to build it from scratch, in Python, without any fancy frameworks like LangChain or CrewAI, just so you can see exactly how the magic works under the hood."

---

## Slide 2: Terminology - Agents

"Before we write code, let's define what an 'Agent' actually is. It sounds complex, but it really boils down to four simple components working together.

1.  **Unique System Prompt**: This is the 'identity' we give the AI. We don't just say 'You are a helpful assistant.' We say, 'You form a thinking loop. You have access to tools. You must use them in a specific format.' This primes the model to behave like a software engineer rather than a chatbot.

2.  **Tools**: These are the 'hands' of the agent. An LLM (Large Language Model) is a brain in a jar—it has no connection to the outside world. Tools are simple Python functions that we give it permission to call. For a coding agent, these tools are things like `read_file`, `list_files`, and `write_file`.

3.  **Loop**: This is the heartbeat of the agent. An agent doesn't just answer once and stop. It enters a cycle:
    *   **Think**: What do I need to do?
    *   **Act**: Call a tool (e.g., read a file).
    *   **Observe**: Look at the output of that tool.
    *   **Repeat**: Based on what I saw, what do I do next?
    This loop continues until the task is finished.

4.  **Memory**: The agent needs to remember what it just did. If it reads a file, it needs to retain that content in its context window so it can use it to fix a bug in the next step.

So, **Agent = LLM + Tools + Loop + Memory**. That's it."

---

## Slide 3: It's that simple

"I want to emphasize this: **It is that simple.**

There is no black magic here. When you see products like Cursor, or Devin, or GitHub Copilot Workspace, they are all built on this fundamental loop. They might have better prompts, faster tools, or smarter memory management, but the core architecture is exactly what we are going to build today.

Don't be intimidated by the jargon. If you can write a `while` loop and call an API, you can build an agent."

---

## Slide 4: Terminology - Prompts

"Let's break down the different types of prompts we'll be using. You need to understand these to debug your agent.

1.  **System Prompt**:
    *   **Who writes it?** You, the developer.
    *   **What does it do?** It sets the rules of engagement. This is where we tell the LLM: 'You are a coding assistant. You have access to these specific tools. When you want to use a tool, output text in this specific JSON format.'
    *   **Permanence**: This is usually pinned to the start of the conversation and never leaves the context.

2.  **User Prompt**:
    *   **Who writes it?** The end-user (or you, when testing).
    *   **What does it do?** This is the specific task. E.g., 'Fix the bug in `main.py` where the database connection fails.'

3.  **Assistant Prompt (or Output)**:
    *   **Who writes it?** The LLM.
    *   **What does it do?** This is the model's response. It might be a natural language answer, or it might be a tool call request like `tool: read_file('main.py')`."

---

## Slide 5: The Steps

"So, what does the flow look like? We call this the **ReAct** (Reasoning + Acting) pattern.

1.  **Read User Input**: We start by getting the command from the terminal.
2.  **Append to Conversation**: We add this user message to our list of messages (our memory).
3.  **The Loop Begins**:
    *   We send the whole conversation history to the LLM.
    *   **LLM Decides**: The LLM looks at the history. It sees the user wants to fix a bug. It knows (from the System Prompt) that it has a `list_files` tool. It thinks: 'I should see what files are here first.'
    *   **Tool Request**: The LLM outputs: `tool: list_files('.')`.
    *   **Pause**: The LLM stops generating. It's waiting.
    *   **Execution (Offline)**: Our Python script parses that string. It runs the actual `os.listdir()` function on your laptop. The LLM is cloud-based, but the tool runs locally on your machine.
    *   **Tool Result**: We capture the output (e.g., `['main.py', 'requirements.txt']`). We format this as a message: `Tool Output: ['main.py', 'requirements.txt']`.
    *   **Feed Back**: We append this tool output to the conversation history and send it *back* to the LLM.
    *   **Repeat**: The LLM receives the new history. Now it knows what files exist. It decides the next step: `tool: read_file('main.py')`.

This cycle repeats until the LLM decides it has enough information to answer the user, at which point it responds with plain text."

---

## Slide 6: Let's build a coding agent from scratch! (Code Walkthrough)

"Okay, enough slides. Let's open `coding_agent_from_scratch_lecture.py` and see how this is implemented line-by-line.

*(Opening file...)*

### Imports and Setup (Lines 1-13)
We start with standard imports. `openai` is our client for the LLM. `pathlib` is crucial for handling file paths across different operating systems (Windows uses `\`, Mac/Linux use `/`). We load our API key from `.env`.

### The System Prompt (Lines 14-23)
Here is our `SYSTEM_PROMPT`. Look closely at line 20:
> "When you want to use a tool, reply with exactly one line in the format: 'tool: TOOL_NAME({{JSON_ARGS}})' and nothing else."

This is **Prompt Engineering**. We are being extremely strict. We don't want the model to say, 'I'm thinking about reading the file...' No. We want a machine-readable string. We are programming the English language to act like code.

### The Tools (Lines 30-100)
We interpret the AI's desires into Python actions.

1.  **`resolve_abs_path` (Line 30)**: This is a security helper. It ensures we aren't trying to read files outside our allowed directories (though in this simple demo, it's just resolving paths).

2.  **`read_file_tool` (Line 39)**:
    *   Takes a `filename`.
    *   Returns a dictionary with `file_path` and `content`.
    *   Note: We return not just the content but also the path, so the LLM is reminded of exactly what it just read.

3.  **`list_files_tool` (Line 54)**:
    *   Iterates through a directory.
    *   Returns a structured list of names and types (file vs dir). This helps the LLM navigate the project tree.

4.  **`edit_file_tool` (Line 72)**:
    *   This is where it gets dangerous (in a cool way).
    *   We are using a naive 'search and replace'.
    *   Arguments: `path`, `old_str`, `new_str`.
    *   Logic: We read the file, look for `old_str`.
    *   If `old_str` is `""` (empty string), we treat it as 'Create New File' or 'Overwrite'.
    *   If `old_str` isn't found, we return an error. This is vital! If the LLM hallucinates the content of the file, this error tells it: 'Hey, that text isn't in the file. Read it again.' The agent can then correct itself.

### The Tool Registry (Lines 102-106)
We map strings to functions.
`"read_file": read_file_tool`
This allows us to take the string "read_file" from the LLM and look up the actual function object.

### Dynamic Documentation (Lines 108-121)
This function `get_full_system_prompt` is clever. It uses `inspect.signature(tool)` to automatically read the Python function signatures and docstrings.
Why do we do this?
Because we paste these signatures into the System Prompt!
If we change our python code (e.g., add a new parameter to `read_file`), the System Prompt automatically updates. The LLM always reads the *current* truth of what the tools do.

### The Parser (Lines 123-144)
`extract_tool_invocations` is our 'listener'.
The LLM sends back a block of text. We need to find the line that starts with `tool:`.
We split the string, parse the arguments as JSON using `json.loads`.
If the JSON is broken (which happens with LLMs!), we catch the exception. In a production system, we would feed that error back to the LLM so it can try again.

### The Main Loop (Lines 154-198)
This is the `run_coding_agent_loop`.

1.  **Initialize Conversation**: We start with the System Prompt (Line 156).
2.  **User Input**: `input("You: ")`.
3.  **Outer Loop**: We keep chatting until the user quits.
4.  **Inner Loop (Line 169)**: This is the Agentic Loop.
    *   `execute_llm_call`: We ask GPT-5 (or 4) for a completion.
    *   **Check for Tools**: We run our parser `extract_tool_invocations`.
    *   **Branch 1 (No Tools)**: If the LLM didn't ask for a tool, it means it's talking to the user. We print the response and break the inner loop to wait for new user input.
    *   **Branch 2 (Tool Call)**: If it *did* ask for a tool:
        *   We look up the function in `TOOL_REGISTRY`.
        *   We execute it with the arguments: `tool(args...)`.
        *   **CRITICAL STEP (Line 193)**: We create a new message with role `user` (or sometimes `tool` in modern APIs) containing the result: `tool_result(<JSON output>)`.
        *   We append this to the conversation.
        *   We strictly **do not break** the inner loop. We loop back immediately to `execute_llm_call`. Why? Because after seeing the tool result, the LLM usually needs to say something else or call another tool. It's essentially talking to itself (thinking) until it's ready to handle the user again.

And that's it. That is the entire source code for a functional coding agent."

---

## Slide 7: The "Secret" Sauce

"Now, the script we just walked through is a toy. It works, but it's fragile. What makes a production agent like Claude or Cursor robust? This slide lists the 'Secret Sauce'.

1.  **Front-loading Context**:
    Instead of waiting for the agent to `list_files`, advanced agents automatically scan your repo structure, open files, and git history, and stuff a summary of it into the System Prompt immediately. This gives the agent 'Project Awareness' from the very first millisecond.

2.  **System Reminders (<system-reminder>)**:
    LLMs drift. After 20 turns of conversation, they might forget they are supposed to output JSON.
    We use 'System Reminders'. We inject tiny reminders at the end of every prompt: *'Remember, if you write code, verify it first.'* or *'Remember to format tools correctly.'* This keeps the model on track.

3.  **Command Prefix Extraction**:
    Parsing natural language is hard. Training models to output special tokens (like `<tool_code>`) or strict prefixes helps reliable parsing.

4.  **Sub-Agents**:
    If I ask an agent to 'Build a full website', the context window fills up fast.
    Smart systems spawn 'Sub-Agents'.
    - One agent focuses solely on writing the HTML.
    - One agent writes the CSS.
    - One agent fixes bugs.
    They share a central memory but have specialized prompts. This prevents 'Context Overloading' where the LLM gets confused by too much information.

---

## Conclusion

Today we demystified the Agent. It is not a sentient being. It is a loop. It is a Python script that lets an LLM call functions.
Your assignment this week is to take this concept and apply it. Instead of a coding agent, you'll build an 'Extraction Agent' for notes. But the principles—Tools, Loop, Parsing—are exactly the same."
