"""
Simple MCP Client for testing the AI Agent MCP server
"""

import asyncio
import subprocess
import json

async def test_mcp_server():
    """Test the MCP server"""
    # Start the MCP server process
    process = await asyncio.create_subprocess_exec(
        "python", "mcp_server.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd="."
    )

    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    # Send request
    request_str = json.dumps(init_request) + "\n"
    if process.stdin:
        process.stdin.write(request_str.encode())
        await process.stdin.drain()

    # Read response
    response_line = await process.stdout.readline()
    response = json.loads(response_line.decode())
    print("Initialize Response:", response)

    # Send initialzed notification
    initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    request_str = json.dumps(initialized) + "\n"
    if process.stdin:
        process.stdin.write(request_str.encode())
        await process.stdin.drain()

    # List tools
    list_tools = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    request_str = json.dumps(list_tools) + "\n"
    if process.stdin:
        process.stdin.write(request_str.encode())
        await process.stdin.drain()

    response_line = await process.stdout.readline()
    response = json.loads(response_line.decode())
    print("\nTools List:", json.dumps(response, indent=2))

    # Call search_web tool
    call_tool = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "search_web",
            "arguments": {
                "query": "latest AI developments"
            }
        }
    }
    request_str = json.dumps(call_tool) + "\n"
    if process.stdin:
        process.stdin.write(request_str.encode())
        await process.stdin.drain()

    response_line = await process.stdout.readline()
    response = json.loads(response_line.decode())
    print("\nSearch Result:", response.get("result", {}).get("content", [])[0].get("text", "")[:200])

    # Cleanup
    if process.stdin:
        process.stdin.close()
    await process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
