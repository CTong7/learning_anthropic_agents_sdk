import asyncio


from claude_agent_sdk import AssistantMessage, ResultMessage, ToolResultBlock, UserMessage, tool, create_sdk_mcp_server, ClaudeAgentOptions, ClaudeSDKClient, ToolUseBlock

# step 1: define a tool using @tool decorator
'''
tools are defined as async in claude
- what is args keyword in python?
- why can we do args['name']?
    - is args a dictionary?
'''

@tool(name="greet", description = "Greet a user",input_schema={"name":str})
async def greet_user_tool(args):
    # returns a python dictionary
    return {
        "content": [
            {
                "type":"text",
                "text": f"Hello, {args['name']}!"
            }

        ]
    }


# step 2: create a sdk mcp server to host all tools
'''
- whats syntax for an mcp server?
- what is the version number for?
- do we use a single mcp server to host all the custom tools we define?
'''
server = create_sdk_mcp_server (
    name = "my-tools",
    version = "1.0.0",
    tools = [greet_user_tool]
)

# step 3: pass in the mcp server as an option to ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers ={"tools": server}, #learn: key "tools" is the name of the server
    allowed_tools = ["mcp__tools__greet"] #todo: what the fuck is this naming? ther is not tool anmed this?
)

# step 4: run the options using ClaudeSDKClient
'''
why the fuck is the claude sdk client being used over the basic async for message in query:
'''
async def main():
    async with ClaudeSDKClient(options = options) as client:
        # learn: this is when the mcp server is started by the client as a subprocess
        await client.query("Greet my friend Alice")

        # returns message object
        async for message in client.receive_response():
            
            # only usermessage or assistant message have a .content attribute
            #! assistant message is the message that contains the initial tool call
            if isinstance(message,AssistantMessage):
                for block in message.content:
                    if isinstance(block,ToolUseBlock):
                        print(f"Calling Tool: <{block.name}> with input: <{block.input}>")

            #! user message is the message that contains the tool output
            elif isinstance(message,UserMessage):
                for block in message.content:
                    if isinstance(block,ToolResultBlock):
                        print(f"This is the output of the tool: <{block.content}>")

                

            # Result mesage is the final result of the llm
            # learn: ResultMessage is guaranteed to be the last message a agent return since
            # receive_resposne() iterator stops yielding messages after ResultMessage
            elif isinstance(message,ResultMessage):
                print(message.result)

    # learn: the async context manager shuts down mcp server subprocess here


if __name__=="__main__":
    asyncio.run(main())