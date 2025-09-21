from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add an additional tool
@mcp.tool()
def add(a:int, b:int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic
def get_greeting(name: str) -> str:
    """Get a personalzied greeting"""
    return f"Hello, {name}"

# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()