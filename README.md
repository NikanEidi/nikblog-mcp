# nikblog-mcp

A real MCP (Model Context Protocol) server, built to close a gap I kept having to disclaim on résumés: SkillSet and my career-assistant system are Claude Skills and prompt-orchestration, not an actual implementation of MCP. This is the real thing. Started 2026-10-17.

## What it does

Exposes my live portfolio ([nik-blog](https://github.com/NikanEidi/nik-blog)) as tools any MCP-compatible client can call:
- `get_my_projects` — pulls my real project list from `GET /projects`
- `get_my_notes` — pulls my real notes list from `GET /notes`

No fake data, no mocked response — both hit my actual deployed API.

## How it's different from what I'd already built

- **SkillSet** (Claude Skills) is prompt instructions and templates Claude reads inside its own Skills system — no server, no protocol.
- **Code Review Agent** (LangChain tools) wires a Python function into one specific script. Only that script can use it.
- **This** is a standalone server, callable by any MCP client — not tied to one app.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install "mcp[cli]" requests
```

## Running it

```bash
python3 server.py
```

Connect it to Claude Code:

```bash
claude mcp add --transport stdio nikblog -- /path/to/venv/bin/python /path/to/server.py
```

## Real bugs hit along the way

- The installed SDK was `mcp` 2.3.0, a newer major version than the tutorials out there assume. `FastMCP` was renamed to `MCPServer` (now imported from `mcp.server.mcpserver`) in v2 — the original `from mcp.server.fastmcp import FastMCP` import raised a `ModuleNotFoundError` with a migration link right in the error message. Fixed by reading the actual migration guide and inspecting the installed package directly (`inspect.signature`) instead of trusting possibly-outdated docs — the decorators (`@mcp.tool()`, `.run()`) stayed identical, only the class name and import path changed.


## Verified working

Asked Claude Code "use nikblog tool to list my projects" and got back my real, live project list — 11 projects, pulled from the actual deployed API, not anything hardcoded:

![get_my_projects tool call](assets/get-my-projects-call.png)

Then asked it to list my notes — got back all 25, correctly grouped by category:

![get_my_notes tool call](assets/get-my-notes-call.png)

## Notes

Full write-up of what MCP is and how this was built: [`notes/00-what-is-mcp.md`](notes/00-what-is-mcp.md).

## Next steps

- Maybe a `get_project_by_slug` tool with a parameter, to learn how MCP handles tool arguments/schemas beyond a no-arg call.
