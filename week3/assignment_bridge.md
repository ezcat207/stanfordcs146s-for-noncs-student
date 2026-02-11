# Assignment Bridge: From Lecture to Implementation

**Purpose:** Connect the concepts from this week's lecture to the specific requirements in your assignment.

**Target Audience:** 18-year-olds with no CS background who might be feeling overwhelmed.

---

## Don't Panic: You Know More Than You Think

"I know what you're thinking: 'The lecture was about a weather API with 100 lines of code. The assignment says I need to build a whole server with authentication and error handling and documentation. How do I do that?'

**Take a deep breath.** You're not starting from zero. Let's map what you learned in the lecture to what the assignment is asking for."

---

## The Mental Model: Lecture → Assignment Mapping

| Lecture Concept | Assignment Requirement | Translation |
|----------------|------------------------|-------------|
| `@mcp.tool` decorator | "Expose at least 2 MCP tools" | Use the decorator twice on two different functions |
| `httpx.get()` with error handling | "Graceful errors for HTTP failures, timeouts" | Copy the try/except pattern from the demo |
| Function docstrings | "Tool reference: names, parameters, example inputs/outputs" | Your docstrings become the documentation |
| `if __name__ == "__main__": mcp.run()` | "STDIO server, runnable from your machine" | Already know how to do this |
| Weather API example | "Choose an external API" | Pick a different API (GitHub, Spotify, etc.) and use the same pattern |

**See?** You're not learning 10 new things. You're applying one pattern to a different API.

---

## Step-by-Step: From Zero to Submission

### Step 1: Choose Your API (5 minutes)

Don't overthink this. Pick an API that:
1. **Has a free tier** (no credit card required)
2. **Interests you personally** (you'll be staring at this for hours—make it fun)
3. **Has decent documentation** (check if they have code examples)

**Good starter APIs:**
- **GitHub API:** Create issues, list repos, search code (no API key needed for public data)
- **Open-Meteo:** Weather data (free, no API key)
- **PokeAPI:** Pokemon data (yes, really—it's perfect for learning)
- **REST Countries:** Country info, flags, populations (free, easy)
- **JokeAPI:** Random jokes (simple, fun, great for testing)

**Where to find APIs:** https://github.com/public-apis/public-apis

**Pro tip:** Choose an API with a 'no authentication' option for your first try. You can add auth as extra credit later.

### Step 2: Set Up Your Environment (10 minutes)

Create this folder structure:
```
week3/
├── server/
│   ├── main.py          ← Your MCP server code goes here
│   └── requirements.txt ← List of libraries you need
├── README.md            ← Your documentation
└── .env.example         ← Template for environment variables
```

**Why this structure?**
- `server/` folder: Keeps your code organized
- `main.py`: Standard name—makes it obvious where to look
- `requirements.txt`: Lists dependencies so anyone can install them with `pip install -r requirements.txt`
- `README.md`: Your instruction manual
- `.env.example`: Shows what environment variables are needed without exposing secrets

**Create requirements.txt:**
```
fastmcp==0.2.0
httpx==0.27.0
python-dotenv==1.0.0  # For loading environment variables
```

**Why these libraries?**
- `fastmcp`: The library that makes building MCP servers easy (you used this in the lecture)
- `httpx`: Modern HTTP client for calling external APIs (you used this in the lecture)
- `python-dotenv`: Loads API keys from a `.env` file (best practice for secrets)

### Step 3: Build Your First Tool (30 minutes)

Open `server/main.py` and start with this template:

```python
from typing import Any, Dict
from fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server
mcp = FastMCP(name="YourServerNameHere")

# API Configuration
API_BASE_URL = "https://api.example.com"  # Replace with your API
API_KEY = os.getenv("API_KEY")  # Optional: only if your API needs auth

@mcp.tool
def your_first_tool(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what this tool does.

    :param param1: Description of first parameter
    :param param2: Description of second parameter
    :return: Description of return value
    """
    try:
        # Step 1: Build the API request
        url = f"{API_BASE_URL}/endpoint"
        params = {"key1": param1, "key2": param2}

        # Step 2: Make the HTTP request
        response = httpx.get(url, params=params, timeout=10.0)

        # Step 3: Check for errors
        if response.status_code != 200:
            return {
                "error": f"API returned status code {response.status_code}",
                "details": response.text
            }

        # Step 4: Parse and return data
        data = response.json()
        return {
            "success": True,
            "data": data
        }

    except httpx.TimeoutException:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
```

**Now replace the placeholders:**
1. Change `YourServerNameHere` to something descriptive (e.g., `GitHubMCPServer`)
2. Change `API_BASE_URL` to your API's base URL (check their docs)
3. Change `your_first_tool` to a descriptive name (e.g., `get_github_issues`)
4. Change `param1`, `param2` to actual parameters your API needs
5. Change the `/endpoint` part to the actual API endpoint

**Test it manually:**
```python
# Add this at the bottom temporarily
if __name__ == "__main__":
    result = your_first_tool("test", 123)
    print(result)
    # mcp.run()  # Comment out for testing
```

Run: `python server/main.py`

If it prints data without errors, you're good. Remove the test code and uncomment `mcp.run()`.

### Step 4: Build Your Second Tool (20 minutes)

Copy-paste the first tool and modify it:
1. Change the function name
2. Change the parameters
3. Change the API endpoint
4. Update the docstring

**Pro tip:** Your second tool can be related to the first. Examples:
- Tool 1: `list_repos(username)` → Lists all repos for a user
- Tool 2: `get_repo_details(username, repo_name)` → Gets details for one repo

This is better than two completely unrelated tools because they work together (like our weather example with `get_city_coordinates` + `get_current_weather`).

### Step 5: Add Error Handling (15 minutes)

The assignment says "graceful errors for HTTP failures, timeouts, and empty results."

**You already have this if you used the template!**

But let's add one more check for empty results:

```python
data = response.json()
if not data:  # Empty response
    return {
        "error": "API returned empty data",
        "success": False
    }
```

**Rate limit awareness:**
Add a comment in your code explaining the rate limit:

```python
# Note: GitHub API allows 60 requests/hour for unauthenticated requests
# If rate limit exceeded, API returns 403 status code
if response.status_code == 403:
    return {
        "error": "Rate limit exceeded. Try again in an hour.",
        "rate_limit": True
    }
```

### Step 6: Write Your README.md (20 minutes)

This is **not** optional. The assignment says "Developer experience (20 points): Clear setup/docs."

Here's a template:

```markdown
# [Your Project Name] MCP Server

A Model Context Protocol server that provides access to [API name] data.

## What This Does

[1-2 sentence explanation in plain English]

Example: "This MCP server lets Claude access GitHub repository data. You can list repositories, get issue details, and search for code."

## Prerequisites

- Python 3.10 or higher
- A [API name] account (if needed)
- Claude Desktop or another MCP-compatible client

## Setup

### 1. Install Dependencies

\`\`\`bash
cd week3
pip install -r server/requirements.txt
\`\`\`

### 2. Configure Environment Variables (if needed)

Create a \`.env\` file in the \`week3/\` directory:

\`\`\`
API_KEY=your-api-key-here
\`\`\`

### 3. Add to Claude Desktop

Edit your Claude Desktop config file:
- **Mac:** \`~/Library/Application Support/Claude/claude_desktop_config.json\`
- **Windows:** \`%APPDATA%/Claude/claude_desktop_config.json\`

Add this to the \`mcpServers\` section:

\`\`\`json
{
  "mcpServers": {
    "your-server-name": {
      "command": "python",
      "args": ["/absolute/path/to/week3/server/main.py"]
    }
  }
}
\`\`\`

**Important:** Replace \`/absolute/path/to/\` with the actual path on your computer.

### 4. Restart Claude Desktop

Close and reopen Claude Desktop. Your server should now be available.

## Available Tools

### \`tool_name_1\`

**Description:** [What it does]

**Parameters:**
- \`param1\` (string): [Description]
- \`param2\` (integer): [Description]

**Example:**
\`\`\`
User: "Use tool_name_1 with param1='example' and param2=42"
Claude: [calls tool] → Returns: {...}
\`\`\`

### \`tool_name_2\`

[Same format as above]

## Troubleshooting

**"Module not found" error:**
Make sure you ran \`pip install -r server/requirements.txt\`

**"API key not found" error:**
Check that your \`.env\` file exists and has the correct format.

**"Connection timeout" error:**
Check your internet connection. The API might be down.

## Rate Limits

[Explain the API's rate limits and what happens if exceeded]

## Extra Credit Implemented

- [ ] Remote HTTP server deployment
- [ ] Authentication (API key or OAuth2)

[If you implemented these, add details about how to use them]
\`\`\`

**Pro tip:** Write the README as you build. Don't leave it for the end.

### Step 7: Test with Claude Desktop (10 minutes)

1. Add your server to Claude Desktop config (see README)
2. Restart Claude Desktop
3. In the chat, type: "What tools do you have available?"
4. Claude should list your tools
5. Ask Claude to use one: "Use [your_tool] to [do something]"

**If it doesn't work:**
- Check the Claude Desktop logs for error messages
- Make sure the path in the config is absolute (not relative)
- Try running `python server/main.py` manually to see if there are errors

---

## Bonus: Authentication (Extra Credit)

The assignment offers +5 points for "Auth implemented correctly."

**Two options:**

### Option 1: API Key (Easier)

Many APIs require an API key in the request headers:

```python
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
response = httpx.get(url, headers=headers, timeout=10.0)
```

Then in your README, explain how users get their API key and add it to `.env`.

### Option 2: OAuth2 (Harder, but impressive)

This requires implementing the OAuth2 flow. Only attempt this if you're comfortable with the basics.

Check the MCP Authorization spec: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

---

## Bonus: Remote HTTP Server (Extra Credit)

The assignment offers +5 points for "Remote HTTP MCP server."

**What this means:**
Instead of running the server locally (STDIO), you deploy it to a server (like Vercel or Cloudflare Workers) and access it over HTTP.

**Why this is harder:**
- You need to understand HTTP transports in MCP (not just STDIO)
- You need to deploy to a cloud platform
- You need to handle CORS, authentication, and other web concerns

**If you want to attempt this:**
1. Read the Cloudflare Workers guide: https://developers.cloudflare.com/agents/guides/remote-mcp-server/
2. Or the Vercel guide: https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel
3. Start with local STDIO first, then upgrade to HTTP if you have time

---

## Common Mistakes to Avoid

### 1. "I picked an API with complex authentication and got stuck"

**Solution:** Start with a no-auth API. Add auth as extra credit if you have time.

### 2. "My docstrings are too vague and Claude doesn't understand my tools"

**Bad:** `def get_data(x):`

**Good:** `def get_github_repo(username: str, repo_name: str):`

**Solution:** Be **extremely** specific in function names and docstrings. Claude reads these to understand your tools.

### 3. "I forgot to handle errors and my server crashes"

**Solution:** Every HTTP request needs try/except. Use the template above.

### 4. "My README doesn't have clear setup instructions"

**Solution:** Ask a friend to follow your README from scratch. If they get confused, clarify.

### 5. "I hardcoded my API key in the code and pushed it to GitHub"

**Solution:** Use `.env` files and add `.env` to your `.gitignore`. **Never** commit secrets.

---

## Evaluation Rubric Breakdown

Let's decode what the graders are looking for:

### Functionality (35 points):
- ✅ Both tools work when called
- ✅ API integration is correct (data comes back)
- ✅ Outputs are meaningful (not just "success: true")

**How to get full points:** Test your tools manually. Make sure they return real data, not error messages.

### Reliability (20 points):
- ✅ Input validation (check if parameters are valid before making API calls)
- ✅ Error handling (try/except blocks)
- ✅ Logging (use `logging` module instead of `print()`)
- ✅ Rate limit awareness (mention it in docs or handle it in code)

**How to get full points:** Use the template above. Add logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Calling API with params: {params}")
```

### Developer Experience (20 points):
- ✅ Clear README with setup steps
- ✅ Easy to run locally
- ✅ Sensible folder structure

**How to get full points:** Have someone else follow your README. If they can run your server in < 5 minutes, you're good.

### Code Quality (15 points):
- ✅ Readable code (good variable names)
- ✅ Type hints (`param: str`, `return -> Dict[str, Any]`)
- ✅ Minimal complexity (don't overcomplicate)

**How to get full points:** Read your code out loud. If you stumble explaining it, simplify.

---

## Timeline: How to Finish in < 3 Hours

- **30 min:** Pick API and read its documentation
- **30 min:** Set up environment and build first tool
- **30 min:** Build second tool
- **30 min:** Write README and test with Claude Desktop
- **30 min:** Add error handling and polish code
- **30 min:** Buffer for debugging

**Total: 3 hours**

Extra credit (if you want it): +2 hours

---

## Final Pep Talk

"You're not building a Google-scale production system. You're demonstrating that you understand:
1. How to call an external API
2. How to wrap it in an MCP tool
3. How to handle errors
4. How to document your work

**That's it.** The assignment is scary because it's open-ended, but the actual code is simple. You've seen the entire pattern in the lecture. Now apply it.

Start small. Get one tool working. Then add the second. Then polish.

You've got this."

---

## Additional Resources

- **FastMCP Examples:** https://github.com/jlowin/fastmcp/tree/main/examples
- **Public APIs List:** https://github.com/public-apis/public-apis
- **MCP Inspector Tool:** https://github.com/modelcontextprotocol/inspector (for debugging your server)
- **httpx Documentation:** https://www.python-httpx.org/
- **Python Type Hints Cheat Sheet:** https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

---

## Need Help?

If you're stuck:
1. Read the error message carefully (90% of bugs are explained in the error)
2. Check the API documentation (maybe you're using the wrong endpoint?)
3. Test your tool function in isolation (call it directly, don't use MCP yet)
4. Ask for help with specific errors (not "it doesn't work"—copy-paste the actual error message)

Good luck! 🚀
