
import httpx
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("GitHub Server")

# Define MCP tool
@mcp.tool()
async def list_pull_requests(owner: str, repo: str):
    """List open pull requests for a GitHub repository."""

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"state": "open", "per_page": 100}
        )
        response.raise_for_status()

    return [
        {
            "title": pr["title"],
            "number": pr["number"],
            "url": pr["html_url"]
        }
        for pr in response.json()
    ]

# Run MCP server
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
