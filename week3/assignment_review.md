# Week 3 Assignment Review: Building Custom MCP Servers

**Purpose:** Help you understand what makes a production-quality MCP server and provide a self-grading checklist.

**After completing your assignment, use this document to:**
1. Understand the "why" behind each requirement
2. Check your work against professional standards
3. Identify areas for improvement

---

## The "Why" Behind Each Requirement

### Why Build an MCP Server?

This assignment isn't just about making an API wrapper. It's about:

1. **Learning Professional Patterns:** Real-world software wraps external APIs constantly. You're learning the standard approach.

2. **Understanding Abstraction:** MCP servers abstract complexity. Claude doesn't need to know GitHub's API structure—it just knows "list_issues exists."

3. **Building Reusable Infrastructure:** A good MCP server can be used by anyone with an MCP client. You're building a public utility.

4. **Defensive Programming:** External APIs fail. Your code must handle failure gracefully. This is a core skill.

---

## Key Architectural Decisions: What the Pros Do

### 1. Why Use Type Hints?

**Student code (bad):**
```python
def get_weather(city):
    ...
```

**Professional code (good):**
```python
def get_weather(city: str) -> Dict[str, Any]:
    ...
```

**Why it matters:**
- MCP libraries use type hints to auto-generate JSON schemas
- Prevents bugs (Python can warn you if you pass wrong types)
- Makes code self-documenting
- Industry standard in modern Python codebases

**Actionable takeaway:** Add type hints to every function parameter and return value.

---

### 2. Why Use a Helper Function for API Requests?

**Anti-pattern (bad):**
```python
@mcp.tool
def list_issues(...):
    # 30 lines of HTTP request logic
    ...

@mcp.tool
def get_issue(...):
    # Same 30 lines copy-pasted
    ...
```

**Professional pattern (good):**
```python
def _make_api_request(endpoint, params):
    # Centralized HTTP logic
    ...

@mcp.tool
def list_issues(...):
    return _make_api_request("/issues", {...})

@mcp.tool
def get_issue(...):
    return _make_api_request("/issues/123", {})
```

**Why it matters:**
- **DRY (Don't Repeat Yourself):** If the API changes, you update one place
- **Consistency:** All tools handle errors the same way
- **Testability:** You can test the helper function in isolation
- **Readability:** Tool functions focus on "what," helper focuses on "how"

**Actionable takeaway:** Extract common logic into helper functions (prefix with `_` to indicate "internal use").

---

### 3. Why Return Structured Dictionaries (Not Strings)?

**Anti-pattern (bad):**
```python
@mcp.tool
def get_weather(city: str) -> str:
    return f"Temperature in {city} is 72 degrees"
```

**Professional pattern (good):**
```python
@mcp.tool
def get_weather(city: str) -> Dict[str, Any]:
    return {
        "city": city,
        "temperature": 72,
        "unit": "fahrenheit",
        "conditions": "sunny"
    }
```

**Why it matters:**
- Claude can **parse structured data** programmatically
- Enables **chaining tools:** Claude can extract temperature and use it in another calculation
- **Internationalization:** Easy to convert units or translate
- **Future-proof:** Adding new fields doesn't break existing code

**Real example:**
If Claude needs to compare temperatures in two cities, structured data makes this possible. With strings, it would have to parse natural language.

**Actionable takeaway:** Always return dictionaries with clear keys. Include a "success" boolean for error handling.

---

### 4. Why Use Logging Instead of print()?

**Anti-pattern (bad):**
```python
print("Making API request...")
print(f"Response: {response.status_code}")
```

**Professional pattern (good):**
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Making API request to /issues")
logger.debug(f"Response status: {response.status_code}")
```

**Why it matters:**
- **STDIO transport conflict:** MCP uses stdout/stdin for communication. `print()` interferes with this.
- **Log levels:** Different environments need different verbosity (DEBUG in dev, ERROR in prod)
- **Structured logging:** Timestamps, module names, and severity levels are automatic
- **Professional standard:** No production system uses `print()` for logging

**Actionable takeaway:** Use `logging.getLogger(__name__)` and methods like `.info()`, `.error()`, `.debug()`.

---

### 5. Why Validate Inputs Before API Calls?

**Anti-pattern (bad):**
```python
@mcp.tool
def list_issues(state: str):
    # Directly call API without checking 'state'
    response = httpx.get(f"/issues?state={state}")
```

**What happens:** If user passes `state="invalid"`, you waste an API call and get a cryptic error.

**Professional pattern (good):**
```python
@mcp.tool
def list_issues(state: str):
    if state not in ['open', 'closed', 'all']:
        return {
            "error": "Invalid state",
            "message": "State must be 'open', 'closed', or 'all'"
        }
    # Now make API call
```

**Why it matters:**
- **Fail fast:** Error happens immediately, not after a slow API call
- **Clear error messages:** User knows exactly what went wrong
- **Rate limit conservation:** Don't waste API quota on invalid requests
- **User experience:** Claude can immediately tell the user what's wrong

**Actionable takeaway:** Validate all inputs before making external calls. Return helpful error messages.

---

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Lazy Prompting (Bad Docstrings)

**Bad:**
```python
@mcp.tool
def get_data(x, y):
    """Gets data."""
```

**Why it's bad:**
- Claude reads docstrings to understand tools
- "Gets data" doesn't explain what data, from where, or how to use it
- Claude might misuse the tool

**Good:**
```python
@mcp.tool
def get_repository_stars(owner: str, repo: str) -> Dict[str, Any]:
    """
    Gets the number of stars (GitHub popularity metric) for a repository.

    :param owner: Repository owner (username or organization), e.g., 'facebook'
    :param repo: Repository name, e.g., 'react'
    :return: Dictionary with 'stars', 'watchers', and 'forks' counts
    """
```

**Actionable takeaway:** Write docstrings as if explaining to someone who has never used GitHub.

---

### Anti-Pattern 2: Hardcoding Values

**Bad:**
```python
GITHUB_TOKEN = "ghp_123456789abcdef"  # NEVER do this
```

**Why it's bad:**
- **Security:** Token is visible in code
- **Version control:** If you commit this, token is exposed forever (even if you delete it later)
- **Inflexibility:** Can't change token without editing code

**Good:**
```python
import os
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
```

**Actionable takeaway:** All secrets go in environment variables. Use `.env` files and `.gitignore`.

---

### Anti-Pattern 3: No Error Handling

**Bad:**
```python
@mcp.tool
def get_weather(city):
    response = httpx.get(f"api.weather.com?city={city}")
    return response.json()
```

**What breaks:**
- Network timeout → Unhandled exception, server crashes
- City doesn't exist → API returns 404, `.json()` fails
- API rate limit → Returns HTML error page, `.json()` crashes

**Good:**
```python
@mcp.tool
def get_weather(city: str) -> Dict[str, Any]:
    try:
        response = httpx.get(f"api.weather.com?city={city}", timeout=10)

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}"}

        return {"success": True, "data": response.json()}

    except httpx.TimeoutException:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": f"Unexpected: {str(e)}"}
```

**Actionable takeaway:** Wrap all external calls in try/except. Handle HTTP errors explicitly.

---

### Anti-Pattern 4: Returning Raw API Responses

**Bad:**
```python
@mcp.tool
def get_issue(owner, repo, number):
    response = httpx.get(f"/repos/{owner}/{repo}/issues/{number}")
    return response.json()  # Returns 50+ fields
```

**Why it's bad:**
- API response has fields Claude doesn't need (internal IDs, timestamps, etc.)
- Wastes tokens/context
- Harder for Claude to parse
- Couples your tool to API's exact structure

**Good:**
```python
@mcp.tool
def get_issue(owner, repo, number):
    response = httpx.get(f"/repos/{owner}/{repo}/issues/{number}")
    data = response.json()

    # Extract only relevant fields
    return {
        "title": data["title"],
        "state": data["state"],
        "author": data["user"]["login"],
        "url": data["html_url"]
    }
```

**Actionable takeaway:** Curate the response. Return only what's useful.

---

## Self-Grading Checklist

Use this checklist to evaluate your submission:

### Functionality (35 points)

- [ ] **At least 2 tools implemented** (using `@mcp.tool`)
- [ ] **Tools actually work** (tested with manual calls and Claude Desktop)
- [ ] **API integration is correct** (data comes from the real API, not hardcoded)
- [ ] **Outputs are meaningful** (not just `{"success": true}`)
- [ ] **Tools are related/complementary** (e.g., list + details, or search + get)

**How to test:** Call each tool manually, verify it returns real data.

---

### Reliability (20 points)

- [ ] **Input validation** (check parameters before API calls)
- [ ] **Error handling for HTTP failures** (network errors, timeouts)
- [ ] **Error handling for API errors** (404, 500, rate limits)
- [ ] **Error handling for empty results** (API returns no data)
- [ ] **Rate limit awareness** (documented in README or handled in code)
- [ ] **Timeouts set** (don't wait forever for API response)
- [ ] **Logging instead of print()** (use `logging` module)

**How to test:**
- Pass invalid parameters (wrong type, out of range)
- Simulate timeout (disconnect from internet mid-request)
- Request non-existent resource (404 case)

---

### Developer Experience (20 points)

- [ ] **Clear README with setup instructions**
- [ ] **Prerequisites listed** (Python version, dependencies)
- [ ] **Environment setup explained** (how to install, configure)
- [ ] **How to add to Claude Desktop** (exact config with example path)
- [ ] **Tool reference section** (lists all tools with parameters and examples)
- [ ] **Sensible folder structure** (e.g., `server/main.py`, not loose files)
- [ ] **requirements.txt exists** (with specific versions)
- [ ] **.gitignore exists** (excludes .env, __pycache__, etc.)

**How to test:**
- Ask a friend to follow your README from scratch
- Can they run your server in < 5 minutes without asking questions?

---

### Code Quality (15 points)

- [ ] **Readable code** (good variable names: `issue_number` not `x`)
- [ ] **Type hints throughout** (all function parameters and return types)
- [ ] **Minimal complexity** (no unnecessary nested ifs, extract helpers)
- [ ] **No code duplication** (use helper functions for repeated logic)
- [ ] **Docstrings for all tools** (explain what, params, return value)
- [ ] **Comments where needed** (explain "why," not "what")
- [ ] **Consistent formatting** (use a formatter like `black` if possible)

**How to test:**
- Read your code out loud. If you stumble, simplify.
- Check for copy-pasted blocks—refactor into functions.

---

### Extra Credit (10 points)

#### Remote HTTP Server (+5 points)
- [ ] Deployed to Vercel, Cloudflare Workers, or similar
- [ ] Accessible over HTTP (not just STDIO)
- [ ] README explains how to access remotely

#### Authentication (+5 points)
- [ ] API key support via environment variable
- [ ] OR OAuth2 implementation with token validation
- [ ] README explains how to configure authentication
- [ ] Never passes user tokens to upstream APIs (for OAuth2)

---

## Grading Rubric Breakdown

### What Graders Look For

**Functionality (35 pts):**
- Grader will call your tools via Claude Desktop
- Must return real data, not errors or hardcoded responses
- If one tool fails, partial credit for the other

**Reliability (20 pts):**
- Grader will test edge cases:
  - Invalid repository name → Should return clear error, not crash
  - Disconnected internet → Should timeout gracefully
  - Rate limit exceeded → Should explain when it resets
- Look at code for try/except blocks and input validation

**Developer Experience (20 pts):**
- Grader will follow your README
- Must be able to run server without Slack/email questions
- README must have concrete examples, not just "configure it properly"

**Code Quality (15 pts):**
- Subjective but based on industry standards
- Type hints: +3 points
- No duplication: +3 points
- Clear names: +3 points
- Docstrings: +3 points
- Clean structure: +3 points

---

## Examples: Bad vs. Good Submissions

### Example 1: Error Handling

**Bad (loses points):**
```python
@mcp.tool
def get_weather(city):
    url = f"api.weather.com?city={city}"
    response = httpx.get(url)
    return response.json()["temperature"]
```

**Issues:**
- No timeout (can hang forever)
- No error handling (crashes on 404, timeout, malformed JSON)
- Returns raw value, not structured data
- No type hints

**Good (full points):**
```python
@mcp.tool
def get_weather(city: str) -> Dict[str, Any]:
    """Gets current temperature for a city."""
    try:
        response = httpx.get(
            f"api.weather.com?city={city}",
            timeout=10.0
        )

        if response.status_code != 200:
            return {"error": f"API error: {response.status_code}"}

        data = response.json()
        return {
            "city": city,
            "temperature": data.get("temperature"),
            "success": True
        }
    except httpx.TimeoutException:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": str(e)}
```

---

### Example 2: Documentation

**Bad README (loses points):**
```markdown
# My MCP Server

Install dependencies and run it.

## Usage
Configure Claude and it works.
```

**Issues:**
- No specific commands
- No tool descriptions
- No troubleshooting
- Assumes knowledge

**Good README (full points):**
```markdown
# Weather MCP Server

## Setup

1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Add to Claude config:
   \`\`\`json
   {
     "mcpServers": {
       "weather": {
         "command": "python",
         "args": ["/Users/you/week3/server/main.py"]
       }
     }
   }
   \`\`\`

3. Restart Claude Desktop

## Tools

### get_weather
Gets temperature for a city.

**Parameters:**
- city (string): City name, e.g., "San Francisco"

**Example:** "What's the weather in Boston?"

## Troubleshooting

**Error: Module not found**
Run: \`pip install -r requirements.txt\`
```

---

## Actionable Improvement Checklist

Before submitting, run through this checklist:

### Code Review

1. **Read your code aloud:** If you stumble, simplify
2. **Check for duplication:** 3+ lines repeated? Extract to function
3. **Verify type hints:** Every function parameter and return type
4. **Check error handling:** Every `httpx.get()` in a try/except?
5. **Test with invalid inputs:** Pass wrong types, empty strings, negative numbers

### Documentation Review

6. **README test:** Give it to a friend. Can they run your server?
7. **Tool descriptions:** Could Claude understand your tools from docstrings alone?
8. **Example usage:** Does README show concrete examples, not generic instructions?

### Integration Testing

9. **Test in Claude Desktop:** Do tools appear? Do they work?
10. **Test edge cases:** Non-existent repo, rate limit, network failure
11. **Check logs:** Are you using `logging`, not `print()`?

---

## Professional Standards: Beyond the Grade

This assignment teaches patterns you'll use in real jobs:

### Pattern 1: API Wrapper Design
**Industry use:** Every company wraps external APIs (Stripe, Twilio, AWS)
**What you learned:** Error handling, rate limits, input validation, structured responses

### Pattern 2: Protocol Implementation
**Industry use:** Implementing REST APIs, GraphQL, gRPC, WebSockets
**What you learned:** Following a spec (MCP protocol), using decorators, defining schemas

### Pattern 3: Defensive Programming
**Industry use:** Building reliable systems that handle failure gracefully
**What you learned:** Try/except, input validation, timeout handling, clear error messages

### Pattern 4: Developer Experience (DX)
**Industry use:** Writing internal tools that coworkers actually want to use
**What you learned:** Clear documentation, easy setup, good defaults, troubleshooting guides

---

## Final Self-Reflection Questions

Before submitting, answer these honestly:

1. **Would I be comfortable using this server in production?**
   - If no, what would you improve?

2. **Could a stranger run my server by only reading the README?**
   - If no, what's missing from the docs?

3. **If the API goes down, does my server crash or handle it gracefully?**
   - Test by disconnecting internet mid-request

4. **Would I want to maintain this code in 6 months?**
   - Is it readable? Well-organized? Documented?

5. **Does my code reflect professional standards I'd expect in a job?**
   - Type hints, logging, error handling, documentation?

---

## Resources for Improvement

### Official Documentation
- **MCP Spec:** https://modelcontextprotocol.io/specification
- **FastMCP Examples:** https://github.com/jlowin/fastmcp/tree/main/examples
- **Python Type Hints:** https://docs.python.org/3/library/typing.html

### Learning Error Handling
- **Real Python Guide:** https://realpython.com/python-exceptions/
- **httpx Documentation:** https://www.python-httpx.org/exceptions/

### Code Quality Tools
- **black** (auto-formatter): `pip install black && black server/`
- **mypy** (type checker): `pip install mypy && mypy server/`
- **ruff** (fast linter): `pip install ruff && ruff check server/`

---

## Conclusion: From Student to Professional

The difference between a "working" solution and a "professional" solution is:

1. **Error handling:** It works when things go wrong, not just when they go right
2. **Documentation:** Others can use it without asking you questions
3. **Code quality:** You can modify it 6 months later without crying
4. **Defensive programming:** You assume the worst and handle it gracefully

**This assignment isn't about building the fanciest MCP server.**
**It's about building a reliable one.**

Good luck! 🚀
