from __future__ import annotations

from collections.abc import Awaitable, Callable

ToolArgs = dict[str, str]
ToolCallable = Callable[[ToolArgs], Awaitable[str]]

TOOLS: dict[str, ToolCallable] = {}


def tool(name: str):
    def decorator(func: ToolCallable):
        TOOLS[name] = func
        return func

    return decorator
