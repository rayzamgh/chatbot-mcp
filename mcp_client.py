#!/usr/bin/env python3
import asyncio
import os
import sys
from typing import Dict
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # loads ANTHROPIC_API_KEY from .env

class MemoryChatbot:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.tool_map: Dict[str, ClientSession] = {}
        self.tool_defs = []

    async def connect_to_server(self, server_uri: str):
        """
        Spawn one MCP server process over stdio, register its tools.
        Supports:
          - Local script: .py / .js / .ts
          - Docker image: docker://<image[:tag]>
        """
        #–– decide how to launch it
        if server_uri.startswith("docker://"):
            image = server_uri[len("docker://"):]
            cmd, args = "docker", ["run", "-i", "--rm", image]
        elif server_uri.endswith(".py"):
            cmd, args = "python", [server_uri]
        elif server_uri.endswith(".js"):
            cmd, args = "node", [server_uri]
        elif server_uri.endswith(".ts"):
            cmd, args = "npx", ["ts-node", server_uri]
        else:
            raise ValueError(
                "Server URI must be docker://<image> or end in .py/.js/.ts"
            )

        params = StdioServerParameters(command=cmd, args=args, env=None)
        stdio, write = await self.exit_stack.enter_async_context(stdio_client(params))
        session = await self.exit_stack.enter_async_context(
            ClientSession(stdio, write)
        )
        await session.initialize()

        # register tools
        resp = await session.list_tools()
        for t in resp.tools:
            if t.name in self.tool_map:
                print(f"⚠️ Skipping duplicate tool '{t.name}'")
            else:
                self.tool_map[t.name] = session
                self.tool_defs.append({
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema
                })

        print(f"🔌 Connected to {server_uri}; tools: {[t['name'] for t in self.tool_defs]}")

    async def process_query(self, query: str) -> str:
        claude_resp = self.anthropic.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1000,
            messages=[{"role": "user", "content": query}],
            tools=self.tool_defs
        )
        final = []
        for chunk in claude_resp.content:
            if chunk.type == "text":
                final.append(chunk.text)

            elif chunk.type == "tool_use":
                print("======chunk.text & content_str======")
                print(chunk)
                session = self.tool_map[chunk.name]
                result = await session.call_tool(chunk.name, chunk.input)

                # === extract a plain string ===
                if isinstance(result.content, str):
                    content_str = result.content
                elif hasattr(result.content, "text"):
                    content_str = result.content.text
                else:
                    content_str = str(result.content)

                print(f"content_str {content_str}")

                # 1) show locally
                final.append(f"[{chunk.name} → {content_str}]")

                # 2) feed back just the tool_result
                follow_up = self.anthropic.messages.create(
                model="claude-3-7-sonnet-latest",
                max_tokens=1000,
                messages=[
                    # Re-send the tool invocation as an assistant message
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": chunk.name,
                                "id": chunk.id,
                                "input": chunk.input
                            }
                        ]
                    },
                    # Then send the result as a user message
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": chunk.id,
                                "content": content_str
                            }
                        ]
                    }
                ],
                tools=self.tool_defs
            )


                # 3) collect any new text Claude emits
                for fchunk in follow_up.content:
                    if fchunk.type == "text":
                        final.append(fchunk.text)


        return "\n".join(final).strip()

    async def chat_loop(self):
        print("💭 Enter your questions (type `quit` to exit):")
        while True:
            q = input("> ").strip()
            if q.lower() in ("quit", "exit"):
                break
            try:
                print("\n" + (await self.process_query(q)) + "\n")
            except Exception as e:
                print(f"⚠️ Error: {e}\n")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    # pull in all MCP_… vars
    mcp_envs = {k:v for k,v in os.environ.items() if k.startswith("MCP_")}
    if not mcp_envs:
        print("Please set MCP_… env vars, e.g.:")
        print("  export MCP_MEMORY_SERVER=docker://my-mcp-memory:latest")
        sys.exit(1)

    client = MemoryChatbot()
    try:
        for name, uri in mcp_envs.items():
            print(f"▶️  {name} → {uri}")
            await client.connect_to_server(uri)
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

# remember me, im the user, Rayza Mahendra im 180cm tall