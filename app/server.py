"""
Low-level MCP stdio server.
"""

from __future__ import annotations
import asyncio
import logging

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from app.tools import TOOLS
from app.tools.handler import handle_call_tool
from app.tools.math import MathArgs
import app.tools.math  # ensures tool modules register themselves

logger = logging.getLogger(__name__)
server = Server("ral-math-mcp")


MATH_SCHEMA = MathArgs.model_json_schema()


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    tools: list[types.Tool] = []
    for name, func in TOOLS.items():
        description = (func.__doc__ or "No description provided").strip()
        tools.append(
            types.Tool(
                name=name,
                description=description,
                inputSchema=MATH_SCHEMA,
            )
        )
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, str] | None):
    logger.info("Calling tool %s with args %s", name, arguments)
    return await handle_call_tool(name, arguments or {})


async def main():
    logging.basicConfig(level=logging.INFO)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received interrupt, shutting down gracefully.")
