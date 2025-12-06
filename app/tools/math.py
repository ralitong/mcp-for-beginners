
from . import tool, ToolArgs
from pydantic import BaseModel

class MathArgs(BaseModel):
    a: float
    b: float

@tool("add")
async def add(arguments: ToolArgs) -> str:
    """Adds two numbers"""
    args = MathArgs(**arguments)
    return str(args.a + args.b)

@tool("subtract")
async def subtract(arguments: ToolArgs) -> str:
    """Subtracts two numbers"""
    args = MathArgs(**arguments)
    return str(args.a - args.b)

@tool("multiply")
async def multiply(arguments: ToolArgs) -> str:
    """Multiplies two numbers"""
    args = MathArgs(**arguments)
    return str(args.a * args.b)

@tool("divide")
async def divide(arguments: ToolArgs) -> str:
    """Divides two numbers"""
    args = MathArgs(**arguments)
    return str(args.a / args.b)