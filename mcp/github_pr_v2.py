
import os
import httpx
from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier

# Read token from environment
TOKEN = os.environ["MCP_AUTH_TOKEN"]

# Configure authentication
auth = StaticTokenVerifier(
    tokens={
        TOKEN: {
            "sub": "student",
            "client_id": "mcp-demo-client",
            "scopes": ["github:read"]
        }
    }
)

# Create MCP server with authentication
mcp = FastMCP("GitHub Server", auth=auth)

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

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
