"""
Low-level MCP server with basic auth using streamable-http transport.
Tools are defined in app/tools/math.py
"""

from __future__ import annotations

import logging

import uvicorn
from mcp import types
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount

from app.auth import BasicAuthMiddleware
from app.tools import TOOLS
from app.tools.handler import handle_call_tool
from app.tools.math import MathArgs
import app.tools.math  # noqa: F401 - ensures tools register themselves

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


# Create session manager for streamable-http transport
session_manager = StreamableHTTPSessionManager(app=server)

# Create Starlette app with the session manager's handle_request as ASGI app
app = Starlette(
    routes=[
        Mount("/mcp", app=session_manager.handle_request),
    ],
    lifespan=lambda app: session_manager.run(),
)

app.add_middleware(BasicAuthMiddleware)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
