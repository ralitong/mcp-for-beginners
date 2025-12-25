# MCP for Beginners - AI Agent Instructions

## Project Overview
Learning repository for Model Context Protocol (MCP) servers using Python. Contains multiple server implementations (FastMCP and low-level Server API), client examples, and LLM integration with Azure AI.

## Critical Setup
- **Dev Container only**: This project MUST run in `.devcontainer`. Do not support local/native setup.
- **Auto-install**: `make install` runs on container creation—creates `.venv` and installs dependencies.
- **Python paths**: Always use `.venv/bin/python` and `.venv/bin/mcp` explicitly in configs/scripts.

## Server Patterns (Two Styles)

### 1. FastMCP (Recommended)
Reference: `server.py`, `complete_server.py`, `stream_server.py`
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""  # Docstring becomes tool description
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}"

if __name__ == "__main__":
    mcp.run()  # stdio by default, or mcp.run(transport="streamable-http")
```

### 2. Low-level Server API
Reference: `stdio_server.py`, `app/server.py`
- Requires `@server.list_tools()` returning `list[types.Tool]` with explicit `inputSchema`
- Requires `@server.call_tool()` handler routing by tool name
- Return `types.TextContent` objects, run with `asyncio.run(main())`

### Modular Tool Architecture
See `app/tools/` for registry pattern:
- `__init__.py`: `@tool(name)` decorator registers to `TOOLS` dict
- `math.py`: Tools use Pydantic models (`MathArgs`) for validation
- `handler.py`: Generic dispatcher returns `list[types.TextContent]`

## Running & Testing

| Command | Purpose |
|---------|---------|
| `make run` | Run `server.py` via `.venv/bin/mcp run` |
| `make run_client` | Run `client_connecting_with_llm.py` (needs `GITHUB_ACCESS_TOKEN` in `.env`) |
| `make inspector` | Launch MCP Inspector UI (debug tools interactively) |
| `make lint` | Run flake8 on `simple_mcp_server.py` |

**VS Code integration**: `.vscode/mcp.json` auto-connects `server.py` to GitHub Copilot—no manual start needed.

## Client Patterns
- **Simple client** (`simple_client.py`): Direct MCP tool calls via `session.call_tool()`
- **LLM bridge** (`client_connecting_with_llm.py`): Converts MCP tools to OpenAI function schema, uses `azure-ai-inference` (not `openai` library)
- **Streaming** (`stream_client.py`): Uses `streamablehttp_client` with notification handlers

## Key Gotchas
- **Logging**: Print to `stderr` only—`stdout` breaks stdio protocol
- **Tool returns**: FastMCP can return primitives; low-level must return `TextContent` objects
- **Decorator syntax**: FastMCP uses `@mcp.tool()`, low-level uses `@server.call_tool()`
- **Port forwarding**: Inspector may bind to different ports—check VS Code Ports panel
- **Azure AI token**: Set `GITHUB_ACCESS_TOKEN` in `.env` for `client_connecting_with_llm.py`

## File Reference
- `server.py`: Minimal FastMCP example (start here)
- `complete_server.py`: FastMCP with multiple tools + help tool
- `stdio_server.py`: Low-level server with manual schema definitions
- `app/`: Modular architecture example with tool registry pattern
- `stream_server.py` + `stream_client.py`: HTTP streaming transport example
- `asyncio_learning/`: Educational Python async examples (ignore for MCP work)

## asyncio_learning/
Educational examples of Python async/event loops—ignore when building MCP servers.
