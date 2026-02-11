# Lecture Transcript: The Model Context Protocol (MCP)

**Date:** October 3, 2025  
**Topic:** Week 2 - MCP (Model Context Protocol)  
**Based on:** `Lecture_10_3_25_public.pptx` and `simple_mcp.py`

---

## Slide 1: Introduction to MCP

"Welcome back. In our last lecture, we built a coding agent from scratch. We manually wrote the 'glue' code to connect the LLM to our file system. We defined tools, we parsed JSON strings, and we handled the execution loop.

It was educational, but let's be honest: it was messy. If every developer had to write their own custom protocol for agents to talk to tools, the AI ecosystem would be a disaster. It would be like the early days of the internet before HTTP existed.

Today, we are going to introduce the solution: **MCP**, the **Model Context Protocol**."

---

## Slide 2: The Problem with Traditional Integrations

"Let's look at the current state of AI integration without MCP.
Imagine you are building an AI assistant that needs to access:
1.  Your Google Drive.
2.  Your Slack messages.
3.  Your GitHub repository.
4.  Your PostgreSQL database.

**The Old Way (Last Week):**
You would have to write a specific Python function for each API.
- `def read_google_drive(...)`
- `def fetch_slack_messages(...)`
- `def query_postgres(...)`

And worst of all, you have to manually teach the LLM how to use them in the System Prompt.
`'You have a tool called read_google_drive. It takes an auth_token and a file_id...'`

This scales poorly. If Slack updates their API, your agent breaks. If you want to switch from Claude to GPT-4, you might need to rewrite your prompt formats. It's a localized, fragile solution."

---

## Slide 3: What is MCP?

"**MCP is an open standard** for connecting AI systems to data sources.
Think of it like **USB-C for AI**.

*   **Before USB:** You had a specific port for a mouse, a specific port for a printer, and a specific port for your keyboard.
*   **With USB:** You have a standard port. You plug it in, and the computer says, 'Ah, this is a mouse.'

MCP does the same for LLMs.
*   **The Host**: The AI application (like Claude Desktop, Cursor, or your own script).
*   **The Client**: The connector that speaks the protocol.
*   **The Server**: The data source (e.g., a 'Google Drive MCP Server' or a 'Postgres MCP Server').

When you use MCP, your LLM doesn't need to know *how* to talk to Postgres. It just asks the MCP Server: 'What tools do you have?' and the Server replies: 'I have a query tool.' The LLM then uses it. The complexity is hidden."

---

## Slide 4: Why MCP Matters?

"Why should you care?
1.  **Universal Compatibility**: Write your tool once (e.g., a 'Weather Tool'), and it works in Claude, it works in ChatGPT (eventually), and it works in your custom agent.
2.  **Security**: The protocol handles permissions. The user has to explicitly approve tool usage (just like we saw in the terminal last time, but standardized).
3.  **Context Management**: MCP isn't just for tools. It's also for **Prompts** and **Resources**. An MCP server can say, 'Here is the context of the current file,' or 'Here is a template for fixing bugs.' It standardizes *context injection*."

---

## Slide 5: How MCP Works (Architecture)

"Let's look at the flow.

1.  **Discovery**:
    The Host (LLM App) starts up. It connects to the MCP Server (e.g., running locally on a port or via stdio).
    Host: "Hello, what can you do?"
    Server: "I am the FileSystem Server. I have `read_file` and `list_files`."

2.  **Injection**:
    The Host takes these descriptions and automatically injects them into the LLM's system prompt (or checks them against the model's native tool capabilities).

3.  **Execution**:
    User: "Read main.py."
    LLM: "Call tool `read_file`."
    Host: (Intercepts call) -> Sends request to MCP Server via JSON-RPC.
    Server: (Executes code) -> Returns result.
    Host: -> Gives result to LLM.

Notice something? **The logic is identical to our script from last time.** But the *implementation details* are now handled by the protocol, not by us manually parsing strings."

---

## Slide 6: Building with FastMCP (Code Walkthrough)

"Now, let's look at `simple_mcp.py`. This uses a library called `fastmcp` which makes writing these servers incredibly easy.

*(Opening file...)*

### Setup (Lines 1-5)
```python
from fastmcp import FastMCP
mcp = FastMCP(name="SimpleMCPTestServer")
```
We initialize the server. We give it a name. That's it. We don't need to set up a `while` loop, or `input()` handling, or `openai` clients. We are just building the *Server* side—the thing that provides the tools.

### Defining Tools (Lines 17-32)
```python
@mcp.tool
def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    """
    # ... implementation ...
```
This is the magic: **The Decorator `@mcp.tool`**.
By adding this one line, FastMCP inspects the function.
1.  It reads the function name: `read_file_tool`.
2.  It reads the type hints: `filename: str`.
3.  It reads the docstring: "Gets the full content..."

**It automatically generates the JSON schema** required for the LLM.
In our manual script last week, we had to write a helper function `get_tool_str_representation` to verify signatures. Here, the library does it for us.

### Security Note (Lines 8-15)
We still include `resolve_abs_path`. Even with MCP, you are responsible for the security of your *implementation*. The protocol creates the connection, but if your code allows deleting the root directory, MCP won't stop you. Always sanitize inputs!

### Running the Server (Lines 83-84)
```python
if __name__ == "__main__":
    mcp.run()
```
When you run this script (`python simple_mcp.py`), it doesn't open a chat window. It doesn't ask for a prompt.
Instead, it starts listening (usually on stdio or a local port).
It waits for an MCP Client (like Claude Desktop App) to connect to it.

**How to stick this into Claude Desktop:**
You would go to your Claude Desktop config and add:
```json
"mcpServers": {
  "my-file-server": {
    "command": "python",
    "args": ["/path/to/simple_mcp.py"]
  }
}
```
Now, when you open Claude, it *automatically* knows it can read your files. You didn't write any UI code. You just wrote the capability."

---

## Slide 7: MCP vs. Manual Parsing (Comparison)

"Let's compare the two approaches directly.

**Manual (coding_agent_from_scratch.py):**
*   **Pros**: You control everything. No dependencies. Good for learning.
*   **Cons**: Fragile parsing (`tool: name(...)`). You have to handle the loop. You have to handle errors. Hard to share with others.

**MCP (`simple_mcp.py`):**
*   **Pros**: Standardized. Robust. The 'Host' (the AI app) handles the loop and the parsing. You just focus on the logic.
*   **Cons**: Requires an MCP-compatible client (which most modern AI apps are becoming).

In this specific example, `simple_mcp.py` is actually *shorter* than the formatting code in our manual script."

---

## Slide 8: The Ecosystem

"MCP is growing fast. There are already pre-built MCP servers for:
*   **Postgres**: Query your DB.
*   **GitHub**: Manage issues/PRs.
*   **Brave Search**: Let the agent browse the web.
*   **Slack**: Send messages.

As a developer, your job is shifting. Instead of prompting, you are becoming a **Tool Builder**. You build the MCP server that exposes your company's internal API, and suddenly every AI agent in your company can use it safely."

---

## Slide 9: Limitations

"Is it perfect? No.
1.  **Context Window**: Every tool you add takes up token space in the system prompt. If you add 1000 tools, the model will get confused or run out of memory.
2.  **Model Intelligence**: Just because you give a model a tool doesn't mean it knows *when* to use it. You still need good naming and docstrings.
3.  **State Management**: MCP is stateless by default. If you need a long-running transaction (like 'start a server and keep it running'), you need to manage that state carefully in your server code."

---

## Conclusion

"In Week 2, we have moved from 'talking to AI' to 'equipping AI'.
*   **Scripts** let us understand the Agent Loop.
*   **MCP** lets us standardize that loop and build reusable, professional tools.

For your assignment, you will be building a feature using these principles. You won't necessarily need to write a full MCP server for the assignment (we'll use Ollama directly for simplicity), but understanding this architecture is crucial for the final project where you will build complex multi-agent systems."
