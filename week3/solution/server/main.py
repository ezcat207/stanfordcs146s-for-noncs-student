"""
GitHub Issues MCP Server - Reference Solution
A production-quality MCP server that wraps the GitHub API.

Features:
- List issues for a repository
- Get details for a specific issue
- Robust error handling with detailed error messages
- Rate limit awareness
- Proper logging
- Type hints throughout
"""
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
import httpx
import logging
from datetime import datetime

# Configure logging (don't use print() in production)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP(name="GitHubIssuesMCPServer")

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"
TIMEOUT_SECONDS = 10.0

# GitHub API allows 60 requests/hour for unauthenticated requests
# For authenticated requests (with token), it's 5000 requests/hour


def _make_github_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Internal helper function to make GitHub API requests.
    Centralizes error handling and logging.

    :param endpoint: API endpoint (e.g., '/repos/owner/repo/issues')
    :param params: Query parameters
    :return: Dictionary with 'success' and either 'data' or 'error'
    """
    url = f"{GITHUB_API_BASE}{endpoint}"
    logger.info(f"Making request to GitHub API: {endpoint}")

    try:
        # GitHub API requires a User-Agent header
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCP-GitHub-Server"
        }

        response = httpx.get(
            url,
            params=params or {},
            headers=headers,
            timeout=TIMEOUT_SECONDS
        )

        # Log response status
        logger.info(f"GitHub API response status: {response.status_code}")

        # Handle rate limiting
        if response.status_code == 403:
            # Check if it's a rate limit issue
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = response.headers.get('X-RateLimit-Remaining')
                reset_time = response.headers.get('X-RateLimit-Reset')
                if remaining == '0':
                    reset_datetime = datetime.fromtimestamp(int(reset_time))
                    return {
                        "success": False,
                        "error": "GitHub API rate limit exceeded",
                        "rate_limit_reset": reset_datetime.isoformat(),
                        "message": f"Rate limit will reset at {reset_datetime}"
                    }

        # Handle not found
        if response.status_code == 404:
            return {
                "success": False,
                "error": "Resource not found",
                "message": "The repository or issue does not exist, or you don't have access to it"
            }

        # Handle other HTTP errors
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"GitHub API returned status code {response.status_code}",
                "message": response.text[:200]  # First 200 chars of error
            }

        # Parse JSON response
        data = response.json()
        return {
            "success": True,
            "data": data
        }

    except httpx.TimeoutException:
        logger.error(f"Request to {endpoint} timed out")
        return {
            "success": False,
            "error": "Request timed out",
            "message": f"GitHub API did not respond within {TIMEOUT_SECONDS} seconds"
        }

    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        return {
            "success": False,
            "error": "Network error",
            "message": str(e)
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": "Unexpected error",
            "message": str(e)
        }


@mcp.tool
def list_repository_issues(
    owner: str,
    repo: str,
    state: str = "open",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Lists issues for a GitHub repository.

    :param owner: Repository owner (username or organization)
    :param repo: Repository name
    :param state: Issue state - 'open', 'closed', or 'all' (default: 'open')
    :param max_results: Maximum number of issues to return (default: 10, max: 100)
    :return: Dictionary containing list of issues or error information
    """
    # Input validation
    if state not in ['open', 'closed', 'all']:
        return {
            "success": False,
            "error": "Invalid state parameter",
            "message": "State must be 'open', 'closed', or 'all'"
        }

    if max_results < 1 or max_results > 100:
        return {
            "success": False,
            "error": "Invalid max_results parameter",
            "message": "max_results must be between 1 and 100"
        }

    # Make API request
    endpoint = f"/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": max_results
    }

    result = _make_github_request(endpoint, params)

    if not result["success"]:
        return result

    # Process the data to return only relevant fields
    issues = result["data"]

    # Handle empty results
    if not issues:
        return {
            "success": True,
            "message": f"No {state} issues found in {owner}/{repo}",
            "issues": []
        }

    # Format issues for easy consumption
    formatted_issues = []
    for issue in issues:
        formatted_issues.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "author": issue["user"]["login"],
            "created_at": issue["created_at"],
            "updated_at": issue["updated_at"],
            "comments_count": issue["comments"],
            "labels": [label["name"] for label in issue.get("labels", [])],
            "url": issue["html_url"]
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "state_filter": state,
        "count": len(formatted_issues),
        "issues": formatted_issues
    }


@mcp.tool
def get_issue_details(
    owner: str,
    repo: str,
    issue_number: int
) -> Dict[str, Any]:
    """
    Gets detailed information about a specific GitHub issue.

    :param owner: Repository owner (username or organization)
    :param repo: Repository name
    :param issue_number: Issue number (e.g., 42)
    :return: Dictionary containing detailed issue information or error
    """
    # Input validation
    if issue_number < 1:
        return {
            "success": False,
            "error": "Invalid issue_number",
            "message": "Issue number must be a positive integer"
        }

    # Make API request
    endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}"
    result = _make_github_request(endpoint)

    if not result["success"]:
        return result

    issue = result["data"]

    # Format the detailed issue information
    formatted_issue = {
        "number": issue["number"],
        "title": issue["title"],
        "state": issue["state"],
        "author": {
            "username": issue["user"]["login"],
            "avatar_url": issue["user"]["avatar_url"],
            "profile_url": issue["user"]["html_url"]
        },
        "body": issue.get("body", "No description provided"),
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "closed_at": issue.get("closed_at"),
        "comments_count": issue["comments"],
        "labels": [
            {"name": label["name"], "color": label["color"]}
            for label in issue.get("labels", [])
        ],
        "assignees": [
            assignee["login"] for assignee in issue.get("assignees", [])
        ],
        "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
        "url": issue["html_url"],
        "api_url": issue["url"]
    }

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "issue": formatted_issue
    }


@mcp.tool
def search_repository_issues(
    owner: str,
    repo: str,
    query: str,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Searches for issues in a repository that match a query string.
    This uses GitHub's search API which has stricter rate limits.

    :param owner: Repository owner (username or organization)
    :param repo: Repository name
    :param query: Search query (searches in title and body)
    :param max_results: Maximum number of results to return (default: 10, max: 30)
    :return: Dictionary containing matching issues or error information
    """
    # Input validation
    if not query or len(query.strip()) == 0:
        return {
            "success": False,
            "error": "Invalid query",
            "message": "Query cannot be empty"
        }

    if max_results < 1 or max_results > 30:
        return {
            "success": False,
            "error": "Invalid max_results parameter",
            "message": "max_results must be between 1 and 30 for search"
        }

    # Build search query
    # Format: "query repo:owner/repo"
    search_query = f"{query} repo:{owner}/{repo}"

    endpoint = "/search/issues"
    params = {
        "q": search_query,
        "per_page": max_results
    }

    result = _make_github_request(endpoint, params)

    if not result["success"]:
        return result

    search_results = result["data"]
    items = search_results.get("items", [])

    # Handle empty results
    if not items:
        return {
            "success": True,
            "message": f"No issues found matching '{query}' in {owner}/{repo}",
            "total_count": 0,
            "issues": []
        }

    # Format results
    formatted_issues = []
    for issue in items:
        formatted_issues.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "author": issue["user"]["login"],
            "created_at": issue["created_at"],
            "score": issue.get("score", 0),  # Search relevance score
            "url": issue["html_url"]
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "query": query,
        "total_count": search_results.get("total_count", 0),
        "returned_count": len(formatted_issues),
        "issues": formatted_issues
    }


if __name__ == "__main__":
    # Run the MCP server
    logger.info("Starting GitHub Issues MCP Server")
    mcp.run()
