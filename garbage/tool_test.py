from claude_agent_sdk import AssistantMessage, ResultMessage, ToolUseBlock, UserMessage, tool, ClaudeSDKClient, ClaudeAgentOptions,create_sdk_mcp_server
import asyncio

'''
in order to pass custom tools to agent sdk
1. create tool using tool decorator
2. create mcp server
3. pass server and tools to the options 
'''
# todo: the arg variable are always strings
@tool(name = "sum-tool",description ="Returns the sum of 2 values",input_schema={"a":int,"b":int})
async def new_tool(args):
    # learn: args is a dictionary!! input

    answer = args["a"]+args["b"]
    # learn: returns a dcitionary 
    # ! dictionary must have type:text or image, and hte output msut be under the "text" key, it literally slices the dictionary and access output["text"]
    return {
        "content": [
            {
                "type":"text",
                "text": str(answer) #learn: we need to return a string value not an int
            }
        ]

    }

# todo: the values in this server definition are NEVER used elsewhere, its just self reported shit
server = create_sdk_mcp_server(
    name="my-tools",
    version = "1.0.0",
    tools = [new_tool]
)

options = ClaudeAgentOptions(
    mcp_servers = {"mcp-server":server}, # pass in as dictionary
    allowed_tools = ["mcp__mcp-server__sum-tool"], #learn: syntax is mcp__[server-name]__[tool-name] , uses dunders
    # ! use allowed_tools NOt just tools otherise it won't have permission to use th te tool
    system_prompt= "You are a helpful asssitant. I've given you access to a set of mcp server tools."
)

async def main():
    
    async with ClaudeSDKClient(options=options) as client:

        await client.query(prompt = "what is the name of my mcp server? what tools does it have? what do the tools do")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block,ToolUseBlock):
                        print(f"Tool Call: {block.name}")

            elif isinstance(message,ResultMessage):
                print(f"AI answer: {message.result}")

        await client.query(prompt = "can you use the mcp server tool to return the sum of 999999999 and 1.458E9?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block,ToolUseBlock):
                        print(f"Tool Call: {block.name}")

            elif isinstance(message,ResultMessage):
                print(f"AI answer: {message.result}")


if __name__=="__main__":
    asyncio.run(main())