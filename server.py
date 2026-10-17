from mcp.server.mcpserver import MCPServer
import requests
import os

mcp = MCPServer("nikblog")

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