from mcp.server.mcpserver import MCPServer
import requests
import os
import secrets
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

class StaticTokenVerifier:
    async def verify_token(self, token:str) -> AccessToken | None:
        key = os.environ.get("MCP_AUTH_TOKEN")
        compare_key = secrets.compare_digest(key, token)
        if compare_key:
            return AccessToken(token= token,client_id="nik-test", scopes=['read'])
        else:
            return None

mcp = MCPServer(
    "nikblog",
    auth=AuthSettings(issuer_url="https://nikblog-mcp.onrender.com", resource_server_url="https://nikblog-mcp.onrender.com",validate_token_resource=False),
    token_verifier=StaticTokenVerifier(), 
    
)

@mcp.tool()
def get_my_projects() -> str:
    """Get Nikan's list of software projects from his live portfolio."""
    try:
        response = requests.get("https://nik-blog.onrender.com/projects", timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Could not reach nik-blog's API right now: {e}"

@mcp.tool()
def get_my_notes() -> str:
    """Get Nikan's list of software notes from his live portfolio."""
    try:
        response = requests.get("https://nik-blog.onrender.com/notes", timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Could not reach nik-blog's API right now: {e}"
@mcp.tool()
def get_project_by_slug(slug: str) -> str:
    """Get details for one of Nikan's projects by its slug (e.g. 'nik-blog', 'ledgerlite')."""
    try:
        response = requests.get(f"https://nik-blog.onrender.com/projects/{slug}", timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Could not reach nik-blog's API right now: {e}"



if __name__ == "__main__":
    port = os.environ.get("PORT")
    if port:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=int(port))
    else:
        mcp.run()