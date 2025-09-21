from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an additional tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divides two numbers"""
    return a / b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers"""
    return a * b


@mcp.tool()
def help():
    return """
Available tools to use are the following:
- add
- subtract
- divide
- multiply
Args: a, b
""".strip()


# Add a dynamic
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalzied greeting"""
    return f"Hello, {name}"


# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()
