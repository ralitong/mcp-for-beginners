## Simple server
```python
    mcp = FastMCP("Demo")

    # Add an addition tool
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b
```

## Low level server
```python
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="add",
                description="Add two numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "number to add"},
                        "b": {"type": "number", "description": "number to add"}
                    },
                    # a and b params are required for add
                    "required": ["a", "b"]
                },
            )
        ]
```

## Architecture
This could be how the project is arranged
```
app
--| tools
----| add
----| subtract
--| resources
----| products
----| schemas
--| prompts
----| product-description
```

## Low level call handler
```python
async def handle_call_tool(
    name: str, arguments: dict[str, str] | None
) -> list[types.TextContent]:
    # tools is a dictionary with tool names as keys
    if name not in tools.tools:
        raise ValueError(f"Unknown tool: {name}")
    tool = tools.tools[name]

    result = "default"
    try:
        result = await tool["handler"](arguments)
    except Exception as e:
        raise ValueError(f"Error calling tool {name}: {str(e)}")

    return [
        types.TextContent(type="text", text=str(result))
    ]
```

## Validating the inputs
```python
# schema.py
from pydantic import BaseModel

class AddInputModel(BaseModel):
    a: float
    b: float

# add.py
async def add_handler(args) -> float:
    try:
        # Validate input using Pydantic model
        input_model = AddInputModel(**args)
    except Exception as e:
        raise ValueError(f"Invalid input: {str(e)}")

    # TODO: add Pydantic, so we can create an AddInputModel and validate args

    """Handler function for the add tool."""
    return float(input_model.a) + float(input_model.b)

tool_add = {
    "name": "add",
    "description": "Adds two numbers",
    "input_schema": AddInputModel,
    "handler": add_handler
}
```