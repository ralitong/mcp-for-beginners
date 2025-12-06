"""Entry point for MCP tool invocations."""

from mcp import types

from . import TOOLS, ToolArgs


async def handle_call_tool(
    name: str,
    arguments: ToolArgs | None,
) -> list[types.TextContent]:
    """Dispatch ToolRequest calls to registered tool callables."""

    tool = TOOLS.get(name)
    if tool is None:
        message = f"Unknown tool '{name}'."
    else:
        try:
            result = await tool(arguments or {})
            message = result
        except Exception as exc:  # pylint: disable=broad-except
            message = f"Tool '{name}' failed: {exc}"

    return [types.TextContent(type="text", text=message)]
