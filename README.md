# nikblog-mcp

A real MCP (Model Context Protocol) server, built to close a gap I kept having to disclaim on résumés: SkillSet and my career-assistant system are Claude Skills and prompt-orchestration, not an actual implementation of MCP. This is the real thing. Started 2026-10-17.

## What it does

Exposes my live portfolio ([nik-blog](https://github.com/NikanEidi/nik-blog)) as tools any MCP-compatible client can call:
- `get_my_projects` — pulls my real project list from `GET /projects`
- `get_my_notes` — pulls my real notes list from `GET /notes`
- `get_project_by_slug(slug)` — pulls one project's full detail from `GET /projects/{slug}`

No fake data, no mocked response — all three hit my actual deployed API.

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

Then asked it for one specific project's details by slug (`ledgerlite`) — got back the real record, not a guess:

![get_project_by_slug tool call](assets/get-project-by-slug-call.png)

## Notes

- [`00-what-is-mcp.md`](notes/00-what-is-mcp.md) — what MCP is, the building blocks, and building the first tool
- [`01-second-tool-get-my-notes.md`](notes/01-second-tool-get-my-notes.md) — adding a second no-argument tool
- [`02-tool-with-a-parameter.md`](notes/02-tool-with-a-parameter.md) — a tool that takes an argument, and how the schema gets built

## Next steps

- Error handling: right now none of the three tools handle a bad input (e.g. a slug that doesn't exist) or the API being down.
