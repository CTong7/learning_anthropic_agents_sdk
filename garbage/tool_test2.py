from claude_agent_sdk import AssistantMessage, ResultMessage, ToolUseBlock, create_sdk_mcp_server, query, ClaudeAgentOptions,tool,ClaudeSDKClient
import random

import asyncio

'''
passing in custom tools

1. define tool async

2. define mcp server (none of it is used)

3. pass mcp and allowed_tools to agent options

4. run it
'''
# learn: you can define the input schema of a tool in 3 different ways you can even make it take no args.
@tool(
    name="pdf-parser",
    description="Returns a dummy string. No input required; call with an empty object.",
    input_schema={},
)
async def parse_pdf_tool(args):
    answer = random.choice(["dummy-1", "dummy-2", "dummy-3"])
    return {
        "content":[
            {
                "type":"text",
                "text": answer
            }
        ]

    }

server = create_sdk_mcp_server(
    name = "mcp-server",
    version = "1.0.0",
    tools = [parse_pdf_tool]
)

options = ClaudeAgentOptions(
    allowed_tools =["mcp__mcp-server__pdf-parser"],
    mcp_servers={"mcp-server":server},
    model = "sonnet",
    system_prompt="""
    You are a helpful assistant.

    Whenever the user mentions the word pdf, call the pdf-parser tool immediately.
    Do not ask for a file path or any other inputs; call with an empty object.
    """
)


async def main():
    
    async with ClaudeSDKClient(options = options ) as client:

        await client.query("parse this pdf file")

        async for message in client.receive_response():

            if isinstance(message,AssistantMessage):
                for block in message.content:
                    if isinstance(block,ToolUseBlock):
                        print(f"Tool Use: {block.name}")

            elif isinstance(message,ResultMessage):
                print(f"AI ANSWER: {message.result}")



if __name__=="__main__":
    asyncio.run(main())
