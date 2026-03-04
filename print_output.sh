#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# run_mcp_client.sh
# Launch MCP client with the weather server using the project's .venv
# -----------------------------------------------------------------------------

# Exit on any error
set -e

# Navigate to project root
cd "$(dirname "$0")"

# Activate the project's virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Error: .venv not found. Please create a virtual environment first."
    exit 1
fi

# Run the MCP client Python script
python <<'PY'
import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Use the same Python interpreter as the virtualenv
    python_path = sys.executable

    server = StdioServerParameters(
        command=python_path,
        args=[os.path.join("weather-server-python", "weather.py")]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])

            result1 = await session.call_tool(
                "get_alerts",
                {"state": "CA"}
            )

            print("\nRAW RESULT OBJECT:")
            print(result1)

            print("================================================")
            print("================================================")

            print("\nFULL TEXT CONTENT:")
            for item in result1.content:
                text = getattr(item, "text", str(item))
                print(text)

            result2 = await session.call_tool(
                "get_forecast",
                {"latitude": 34,
                "longitude": -118}
            )

            print("\nRAW RESULT OBJECT:")
            print(result2)

            print("\nFULL TEXT CONTENT:")
            for item in result2.content:
                text = getattr(item, "text", str(item))
                print(text)
asyncio.run(main())
PY