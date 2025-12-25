"""MCP client that lets an OpenAI model call your tools."""

from __future__ import annotations

import asyncio
import base64
import json
import os

from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client
from openai import AsyncOpenAI

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Load userrs from users.json
USERS_FILE = Path(__file__).parent / "users.json"
USERS = json.loads(USERS_FILE.read_text())


def convert_tools(tools: list[types.Tool]) -> list[dict]:
    openai_tools = []
    for tool in tools:
        openai_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema or {"type": "object"},
                },
            }
        )
    return openai_tools


def make_auth_header(username: str, password: str) -> dict:
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


async def run_conversation() -> None:
    """One user -> LLM -> tool -> LLM round trip."""
    username = "admin"
    password = USERS[username]
    headers = make_auth_header(username, password)

    async with streamablehttp_client(
        url="http://localhost:8000/mcp", headers=headers
    ) as (
        read,
        write,
        _,
    ):
        user_message = input("Ask something that needs the math tools: ")
        async with ClientSession(read, write) as session:
            await session.initialize()

            listed_tools = await session.list_tools()
            tools_as_openai = convert_tools(listed_tools.tools)

            client = AsyncOpenAI()

            # First turn: let the model which tool(s) to call
            initial = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": user_message}],
                tools=tools_as_openai,
            )

            choice = initial.choices[0].message
            tool_calls = choice.tool_calls or []
            if not tool_calls:
                print("Model replied directly:")
                print(choice.content)
                return

            follow_up_messages: list[dict] = [
                {"role": "user", "content": user_message},
                {
                    "role": "assistant",
                    "content": choice.content,
                    "tool_calls": tool_calls,
                },
            ]

            # Execute requested tools via MCP and attach results
            for tool_call in tool_calls:
                args = json.loads(tool_call.function.arguments or "{}")
                result = await session.call_tool(
                    tool_call.function.name, arguments=args
                )
                follow_up_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": result.content[0].text if result.content else "",
                    }
                )

            # Second turn: model produces the final answer with tool outputs
            final = await client.chat.completions.create(
                model=OPENAI_MODEL, messages=follow_up_messages
            )

            print("Assistant reply:")
            print(final.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(run_conversation())
