# MCP for Beginners - AI Agent Instructions

## Project Overview
Learning repository for Model Context Protocol (MCP) servers using Python. Contains multiple MCP server implementations (FastMCP and low-level Server API) and client examples integrating with Azure OpenAI.

## Critical Setup
- **Dev Container only**: This project MUST run in the `.devcontainer` environment. Do not support local/native setup.
- **Auto-install**: `postCreateCommand: make install` runs automatically on container creation—creates `.venv` and installs dependencies.
- **Python interpreter**: Always use `.venv/bin/python` (set in `devcontainer.json`). The `mcp` CLI wrapper is at `.venv/bin/mcp`.

## MCP Server Patterns

### Two Server Styles (Pick One)
1. **FastMCP** (recommended, simpler): `server.py`, `simple_mcp_server.py`
   ```python
   from mcp.server.fastmcp import FastMCP
   mcp = FastMCP("Demo")
   
   @mcp.tool()
   def add(a: int, b: int) -> int:
       return a + b
   
   if __name__ == "__main__":
       mcp.run()  # Handles stdio automatically
   ```

2. **Low-level Server API**: `stdio_server.py` (async, manual setup)
   - Requires `@server.list_tools()` and `@server.call_tool()` handlers
   - Must use `async def` and return `CallToolResult` objects
   - Run with `asyncio.run(main())`

### Running Servers
- **Production**: `make run` → runs `server.py` via `.venv/bin/mcp run`
- **Inspector (debug)**: `make inspector` → launches MCP Inspector UI (ports 6277/6274 auto-forwarded)
- **VS Code integration**: `.vscode/mcp.json` connects `server.py` to GitHub Copilot—no manual start needed

## Key Files
- `server.py`: Main FastMCP server (tools: `add`, resource: `greeting://{name}`)
- `client_connecting_with_llm.py`: MCP client that bridges to Azure OpenAI (requires `GITHUB_ACCESS_TOKEN` in `.env`)
- `Makefile`: All workflows (`install`, `run`, `run_client`, `inspector`, `lint`)
- `.vscode/mcp.json`: Auto-connects MCP server to Copilot (uses `${workspaceFolder}/.venv/bin/mcp`)

## Common Patterns
- **Logging**: Print to `stderr` (not `stdout`) to avoid breaking stdio protocol
- **Tool returns**: Return dicts for structured output (avoid bare primitives to prevent Inspector warnings)
- **Async**: FastMCP handles async internally; low-level API requires explicit `async def` handlers
- **Environment**: Load secrets from `.env` (e.g., `GITHUB_ACCESS_TOKEN` for Azure AI)

## Development Workflow
1. Modify `server.py` or add new tools
2. Test with Inspector: `make inspector` (UI opens at forwarded port)
3. Or test via Copilot: type `@workspace` in Copilot Chat to invoke tools
4. Format on save (Black formatter configured in devcontainer)
5. Lint: `make lint` (flake8 on `simple_mcp_server.py`)

## Gotchas
- **Port forwarding**: Inspector may bind to different ports—check VS Code Ports panel
- **Decorator syntax**: FastMCP uses `@mcp.tool()`, low-level uses `@server.call_tool()` with specific signatures
- **Venv paths**: Always reference `.venv/bin/{python,mcp}` explicitly in configs/scripts
- **Azure AI**: `client_connecting_with_llm.py` uses `azure-ai-inference` (not `openai` library)

## asyncio_learning/
Educational examples of Python async/event loops—ignore when building MCP servers.
