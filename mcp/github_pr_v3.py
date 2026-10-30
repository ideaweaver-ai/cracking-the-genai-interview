import os
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier

MCP_AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN")
GITHUB_PAT = os.environ.get("GITHUB_PAT")

if not MCP_AUTH_TOKEN:
    raise RuntimeError("MCP_AUTH_TOKEN is required to start this server.")

if not GITHUB_PAT:
    raise RuntimeError(
        "GITHUB_PAT is required. Create a GitHub personal access token "
        "and export it before starting the server: export GITHUB_PAT=ghp_..."
    )

auth = StaticTokenVerifier(
    tokens={
        MCP_AUTH_TOKEN: {
            "sub": "student",
            "client_id": "mcp-demo-client",
            "scopes": ["github:read"],
        }
    }
)

mcp = FastMCP("GitHub Server", auth=auth)

GITHUB_API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_PAT}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "github-mcp-server",
}


async def github_get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Call the GitHub REST API with the configured PAT."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"https://api.github.com{path}",
            headers=GITHUB_API_HEADERS,
            params=params,
        )
        if response.status_code == 401:
            raise PermissionError(
                "GitHub rejected the PAT. Check that GITHUB_PAT is valid "
                "and has the repo scope."
            )
        if response.status_code == 403:
            raise PermissionError(
                "GitHub denied this request. The PAT may lack permission "
                "for this repository, or the rate limit was exceeded."
            )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_pull_requests(owner: str, repo: str) -> list[dict[str, Any]]:
    """List open pull requests for a GitHub repository."""
    pulls = await github_get(
        f"/repos/{owner}/{repo}/pulls",
        params={"state": "open", "per_page": 100},
    )
    return [
        {
            "title": pr["title"],
            "number": pr["number"],
            "url": pr["html_url"],
        }
        for pr in pulls
    ]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
    )
