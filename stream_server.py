# server.py
import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

mcp = FastMCP("Streamable DEMO")
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "stream_welcome.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


async def event_stream(message: str):
    for i in range(1, 4):
        yield f"Processing file {i}/3...\n"
        await asyncio.sleep(1)
    yield f"Here's the file content: {message}\n"

@app.get("/stream")
async def stream(message: str = "hello"):
    return StreamingResponse(event_stream(message), media_type="text/event-stream")

@mcp.tool(description="A tool that simulates file processing and sends progress notifications")
async def process_files(message: str, ctx: Context) -> TextContent:
    files = [f"file_{1}.txt" for i in range(1, 4)]
    for idx, file in enumerate(files, 1):
        await ctx.info(f"Processing {file} ({idx}/{len(files)})...")
        await asyncio.sleep(1)
    await ctx.info("All files processed!")
    return TextContent(type="text", text=f"Processed files: {', '.join(files)} | Message: {message}")

if __name__ == "__main__":
    import sys
    if "mcp" in sys.argv:
        # Configure MCP server with streamable-http transport
        print("Starting MCP server with streamable-http transport")
        # MCP server will create its own FastAPI app with the /mcp endpoint
        # The mcp object will use the port configuration of uvicorn below
        # The mcp can be contacted at port=8000
        mcp.run(transport="streamable-http")
    else:
        # Start FastAPI app for classic HTTP streaming
        print("Starting FastAPI server for classic HTTP streaming...")
        uvicorn.run("stream_server:app", host="127.0.0.1", port=8000, reload=True)