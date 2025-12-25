import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("example-server")


# MCP Protocol handlers
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="calculate_sum",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="get_greeting",
            description="Generate a personalized greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person's name"}
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="calculate_product",
            description="Calculate the product of two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="get_server_info",
            description="Get information about this MCP server",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Route tool calls to implementation functions"""
    if name == "calculate_sum":
        logging.info(f"Calculating sum of {arguments['a']} and {arguments['b']}")
        result = arguments["a"] + arguments["b"]
    elif name == "get_greeting":
        logging.info(f"Generating greeting for {arguments['name']}")
        result = f"Hello, {arguments['name']}! Welcome to the MCP stdio server."
    elif name == "calculate_product":
        logging.info(f"Calculating product of {arguments['a']} and {arguments['b']}")
        result = arguments["a"] * arguments["b"]
    elif name == "get_server_info":
        # Return dict directly - decorator will wrap it
        return {
            "server_name": "example-stdio-server",
            "version": "1.0.0",
            "transport": "stdio",
            "capabilities": ["tools"],
        }
    else:
        raise ValueError(f"Unknown tool: {name}")

    # Return content blocks (decorator wraps in CallToolResult automatically)
    return [TextContent(type="text", text=str(result))]


async def main():
    # Use stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
