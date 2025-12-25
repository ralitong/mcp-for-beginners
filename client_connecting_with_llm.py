import json
import os

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.rest import HttpRequest
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "complete_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


def convert_to_llm_tool(tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"],
            },
        },
    }
    return tool_schema


def call_llm(prompt, functions):
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    endpoint = "https://models.inference.ai.azure.com"

    client = ChatCompletionsClient(
        endpoint=endpoint, credential=AzureKeyCredential(token)
    )

    model_name = "gpt-4o"
    print("CALLING LLM")
    response = client.complete(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        model=model_name,
        tools=functions,
        # Optional parameters
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0,
    )

    response_message = response.choices[0].message

    functions_to_call = []

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print("TOOL: ", tool_call)
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({"name": name, "args": args})
    return functions_to_call


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available resources
            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)

            # List available tools
            tools = await session.list_tools()
            print("LISTING TOOLS")
            for tool in tools.tools:
                print("Tool: ", tool.name)
                print("Tool", tool.inputSchema["properties"])

            functions = []

            for tool in tools.tools:
                print("Tool: ", tool.name)
                print("Tool", tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))

            prompt = "Add 2 to 20"
            # ask LLM what tools to call, if any
            functions_to_call = call_llm(prompt, functions)

            # call suggested functions
            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments=f["args"])
                print("TOOLS result: ", result.content)

            prompt = "Divide 20 by 5"
            functions_to_call = call_llm(prompt, functions)
            # call suggested functions
            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments=f["args"])
                print("TOOLS result: ", result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
