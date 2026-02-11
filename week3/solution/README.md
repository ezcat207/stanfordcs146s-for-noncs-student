# GitHub Issues MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with access to GitHub repository issues. This server allows Claude (or any MCP-compatible client) to list, search, and retrieve detailed information about GitHub issues.

## What This Does

This MCP server acts as a bridge between AI assistants and the GitHub API. It provides three main capabilities:

1. **List repository issues** - Get all open, closed, or all issues from a repository
2. **Get issue details** - Retrieve detailed information about a specific issue
3. **Search issues** - Find issues matching a search query

All data is fetched in real-time from GitHub's public API.

## Prerequisites

- Python 3.10 or higher
- Claude Desktop or another MCP-compatible client
- (Optional) A GitHub account for higher rate limits

## Quick Start

### 1. Install Dependencies

```bash
cd week3/solution
pip install -r server/requirements.txt
```

### 2. (Optional) Configure GitHub Token

For unauthenticated requests, GitHub allows 60 requests/hour. For authenticated requests, this increases to 5,000 requests/hour.

To use authentication:

1. Create a GitHub Personal Access Token at: https://github.com/settings/tokens
2. Select scope: `public_repo` (for public repositories only)
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Add your token to `.env`:
   ```
   GITHUB_TOKEN=ghp_your_actual_token_here
   ```

**Note:** Authentication is optional. The server works without it, just with lower rate limits.

### 3. Test the Server Locally

Before integrating with Claude, test the server manually:

```bash
python server/main.py
```

The server will start and wait for MCP connections. Press `Ctrl+C` to stop.

### 4. Add to Claude Desktop

#### On macOS:
1. Open: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### On Windows:
1. Open: `%APPDATA%/Claude/claude_desktop_config.json`

Add this to the `mcpServers` section:

```json
{
  "mcpServers": {
    "github-issues": {
      "command": "python",
      "args": ["/absolute/path/to/week3/solution/server/main.py"]
    }
  }
}
```

**Important:** Replace `/absolute/path/to/` with the actual full path on your computer.

#### Example paths:
- macOS: `"/Users/yourname/projects/week3/solution/server/main.py"`
- Windows: `"C:\\Users\\yourname\\projects\\week3\\solution\\server\\main.py"`

### 5. Restart Claude Desktop

Close and reopen Claude Desktop completely. Your server should now be available.

## Available Tools

### 1. `list_repository_issues`

Lists issues from a GitHub repository.

**Parameters:**
- `owner` (string, required): Repository owner (username or organization)
- `repo` (string, required): Repository name
- `state` (string, optional): Filter by state - `"open"`, `"closed"`, or `"all"` (default: `"open"`)
- `max_results` (integer, optional): Maximum number of issues to return, 1-100 (default: 10)

**Example usage in Claude:**

```
User: "List the open issues in the facebook/react repository"

Claude: [calls list_repository_issues with owner="facebook", repo="react", state="open"]

Returns: List of recent open issues with titles, authors, and links
```

**Response format:**
```json
{
  "success": true,
  "repository": "facebook/react",
  "state_filter": "open",
  "count": 10,
  "issues": [
    {
      "number": 12345,
      "title": "Bug: Something is broken",
      "state": "open",
      "author": "username",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-16T14:20:00Z",
      "comments_count": 5,
      "labels": ["bug", "needs-triage"],
      "url": "https://github.com/facebook/react/issues/12345"
    }
  ]
}
```

### 2. `get_issue_details`

Gets detailed information about a specific GitHub issue.

**Parameters:**
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `issue_number` (integer, required): Issue number (visible in the issue URL)

**Example usage in Claude:**

```
User: "Get details about issue #12345 in facebook/react"

Claude: [calls get_issue_details with owner="facebook", repo="react", issue_number=12345]

Returns: Full issue details including description, comments count, labels, assignees, etc.
```

**Response format:**
```json
{
  "success": true,
  "repository": "facebook/react",
  "issue": {
    "number": 12345,
    "title": "Bug: Something is broken",
    "state": "open",
    "author": {
      "username": "reporter",
      "avatar_url": "https://...",
      "profile_url": "https://github.com/reporter"
    },
    "body": "Full issue description here...",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-16T14:20:00Z",
    "closed_at": null,
    "comments_count": 5,
    "labels": [
      {"name": "bug", "color": "d73a4a"}
    ],
    "assignees": ["developer1", "developer2"],
    "milestone": "v18.3.0",
    "url": "https://github.com/facebook/react/issues/12345"
  }
}
```

### 3. `search_repository_issues`

Searches for issues matching a query string.

**Parameters:**
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `query` (string, required): Search query (searches in title and body)
- `max_results` (integer, optional): Maximum results to return, 1-30 (default: 10)

**Example usage in Claude:**

```
User: "Search for issues about 'hooks' in facebook/react"

Claude: [calls search_repository_issues with owner="facebook", repo="react", query="hooks"]

Returns: Issues containing "hooks" in title or description
```

**Response format:**
```json
{
  "success": true,
  "repository": "facebook/react",
  "query": "hooks",
  "total_count": 234,
  "returned_count": 10,
  "issues": [
    {
      "number": 12345,
      "title": "useEffect hooks issue",
      "state": "open",
      "author": "username",
      "created_at": "2025-01-15T10:30:00Z",
      "score": 125.3,
      "url": "https://github.com/facebook/react/issues/12345"
    }
  ]
}
```

## Error Handling

The server implements comprehensive error handling:

### Rate Limiting
- **Unauthenticated:** 60 requests/hour
- **Authenticated:** 5,000 requests/hour

When rate limit is exceeded, the server returns:
```json
{
  "success": false,
  "error": "GitHub API rate limit exceeded",
  "rate_limit_reset": "2025-01-15T11:00:00Z",
  "message": "Rate limit will reset at 2025-01-15 11:00:00"
}
```

### Network Errors
```json
{
  "success": false,
  "error": "Request timed out",
  "message": "GitHub API did not respond within 10 seconds"
}
```

### Invalid Repository/Issue
```json
{
  "success": false,
  "error": "Resource not found",
  "message": "The repository or issue does not exist, or you don't have access to it"
}
```

### Input Validation
All parameters are validated before making API calls:
```json
{
  "success": false,
  "error": "Invalid state parameter",
  "message": "State must be 'open', 'closed', or 'all'"
}
```

## Logging

The server uses Python's built-in `logging` module (not `print()`) for production-quality logging.

Logs include:
- API request URLs and endpoints
- Response status codes
- Error conditions
- Rate limit warnings

**Example log output:**
```
2025-01-15 10:30:00 - __main__ - INFO - Starting GitHub Issues MCP Server
2025-01-15 10:30:15 - __main__ - INFO - Making request to GitHub API: /repos/facebook/react/issues
2025-01-15 10:30:16 - __main__ - INFO - GitHub API response status: 200
```

## Rate Limits

### GitHub API Rate Limits

| Type | Limit | Resets |
|------|-------|--------|
| Unauthenticated | 60 requests/hour | Every hour |
| Authenticated | 5,000 requests/hour | Every hour |
| Search API | 10 requests/minute | Every minute |

**Best Practices:**
1. Use authentication for production use
2. Cache responses when possible
3. Avoid making the same request multiple times in quick succession

**Rate Limit Headers:**
The GitHub API includes these headers in responses:
- `X-RateLimit-Remaining`: Requests remaining this hour
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## Code Quality Features

### Type Hints
All functions use Python type hints for clarity:
```python
def get_issue_details(
    owner: str,
    repo: str,
    issue_number: int
) -> Dict[str, Any]:
```

### Input Validation
Parameters are validated before making API calls:
- State must be 'open', 'closed', or 'all'
- max_results must be within allowed ranges
- Issue numbers must be positive integers
- Search queries cannot be empty

### Error Recovery
Three levels of exception handling:
1. HTTP-specific errors (timeouts, network issues)
2. GitHub API errors (rate limits, not found)
3. Unexpected errors (catch-all for unforeseen issues)

### Code Organization
- Helper function `_make_github_request()` centralizes API logic
- DRY (Don't Repeat Yourself) principle throughout
- Clear separation of concerns

## Troubleshooting

### "Module not found" error
**Problem:** `ModuleNotFoundError: No module named 'fastmcp'`

**Solution:**
```bash
pip install -r server/requirements.txt
```

### "Connection refused" or server doesn't start
**Problem:** Server starts but Claude can't connect

**Solution:**
1. Check that the path in `claude_desktop_config.json` is absolute (not relative)
2. Check that Python is in your PATH: `which python` or `where python`
3. Try running the server manually: `python server/main.py`

### "Rate limit exceeded" error
**Problem:** Too many requests in a short time

**Solution:**
1. Wait until the rate limit resets (check the `rate_limit_reset` timestamp in the error)
2. Add a GitHub token to `.env` for higher limits
3. Reduce the frequency of requests

### Server works locally but not in Claude Desktop
**Problem:** `python server/main.py` works, but Claude says server is unavailable

**Solution:**
1. Restart Claude Desktop completely (Quit and reopen)
2. Check Claude's logs: `~/Library/Logs/Claude/` (macOS) or `%APPDATA%/Claude/logs/` (Windows)
3. Ensure config JSON is valid (no trailing commas, proper quotes)

## Project Structure

```
week3/solution/
├── server/
│   ├── main.py           # MCP server implementation
│   └── requirements.txt  # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore           # Files to exclude from git
└── README.md            # This file
```

## Extra Credit Features

### Implemented:
- ✅ **Robust Error Handling:** All HTTP failures, timeouts, and edge cases handled
- ✅ **Rate Limit Awareness:** Detects and reports rate limit status
- ✅ **Input Validation:** All parameters validated before API calls
- ✅ **Structured Logging:** Production-quality logging with timestamps
- ✅ **Type Hints:** All functions fully typed
- ✅ **Clear Documentation:** Comprehensive README with examples

### Not Implemented (but possible to add):
- ❌ **Remote HTTP Transport:** Currently uses STDIO (local only)
- ❌ **OAuth2 Authentication:** Currently uses optional token auth

## Testing the Server

### Manual Testing
```python
# In server/main.py, temporarily add at the bottom:
if __name__ == "__main__":
    # Test directly
    result = list_repository_issues("facebook", "react", "open", 5)
    print(result)
```

### Integration Testing with Claude Desktop

1. Start Claude Desktop with your server configured
2. Ask: "What tools do you have available?"
3. Claude should list the three GitHub tools
4. Try: "List 5 open issues in the facebook/react repository"
5. Try: "Get details about issue #28000 in facebook/react"
6. Try: "Search for 'hooks' in facebook/react issues"

## License

This is a reference solution for educational purposes.

## Author

Reference solution for CS146S - The Modern Software Developer
Stanford University, Fall 2025
