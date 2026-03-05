import asyncio
import sys
import json
from contextlib import AsyncExitStack
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from llm.factory import create_provider

load_dotenv()

class MCPClient:

    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.llm = create_provider()

    async def connect_to_server(
            self,
            server_script_path,
    ):
        
       path = Path(server_script_path).resolve()

       server_params = StdioServerParameters(
           command="uv",
           args=[
               "--directory",
               str(path.parent),
               "run",
               path.name,
           ],
       )

       stdio_transport = await self.exit_stack.enter_async_context(
           stdio_client(server_params)
       )
        #should these be self.stdio, self.write = stdio_transport
       stdio, write = stdio_transport

       self.session = await self.exit_stack.enter_async_context(
           ClientSession(stdio, write)
       )

       await self.session.initialize()

       response = await self.session.list_tools()
       tools = response.tools
       print(
           "Connected tools:",
           [tool.name for tool in tools],
       )

    async def process_query(self, query: str) -> str:
        
        messages = [{"role": "user", "content": query}]

        ### ??? Should it be response instead of tool_response
        tool_response = await self.session.list_tools()

        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    ### ??? "input_schema": t.inputSchema
                    "parameters": t.inputSchema
                },
            }
            for t in tool_response.tools
        ]

        ### ???
        response = await self.llm.chat(
            messages,
            tools,
        )

        ### ???
        print(response)

        msg = response["messages"]

        output = []

        if msg.get("content"):
            output.append(
                msg["content"]
            )

        if msg.get("tool_calls"):
            for call in msg["tool_calls"]:

                name = call["function"]["name"]

                args = json.loads(
                    call["function"]["arguments"]
                )

                result = await self.session.call_tool(
                    name,
                    args,
                )

                messages.append(msg)

                messages.append(
                    {
                        "role": "tool",
                        "content": result.content,
                    }
                )

                response = await self.llm.chat(
                    messages
                )

                output.append(
                    response["message"]["content"]
                )
        
        return "\n".join(output)
    
    async def chat_loop(self):

        while True:

            q = input("> ")

            if q == "quit":
                break

            print(
                await self.process_query(q)
            )
    
    async def cleanup(self):

        await self.exit_stack.aclose()

        if hasattr(self.llm, "close"):
            await self.llm.close()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()

    try:
        await client.connect_to_server(sys.argv[1])
    
        await client.chat_loop()

    finally:
        await client.cleanup()

if __name__ == "__main__":
    
    import sys
    asyncio.run(main())