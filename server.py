from mcp.server.mcpserver import MCPServer
import requests

mcp = MCPServer("nikblog")

@mcp.tool()
def get_my_projects() -> str:
    """Get Nikan's list of software projects from his live portfolio."""
    response = requests.get("https://nik-blog.onrender.com/projects")
    return response.text

@mcp.tool()
def get_my_notes() -> str:
    """Get Nikan's list of software notes from his live portfolio."""
    response = requests.get("https://nik-blog.onrender.com/notes")
    return response.text

@mcp.tool()
def get_project_by_slug(slug: str) -> str:
    """Get details for one of Nikan's projects by its slug (e.g. 'nik-blog', 'ledgerlite')."""
    response = requests.get(f"https://nik-blog.onrender.com/projects/{slug}")
    return response.text 

if __name__ == "__main__":
    mcp.run()