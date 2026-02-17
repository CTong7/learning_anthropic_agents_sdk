'''
recap of anthropic claude agent sdk

2 main ways ot use agents sdk
1. normal query()
2. use client .query()

- main difference is that normal query() doesn't allow you to pass in custom tools 
- you need the sdk client in order to pass in custom tools on mcp server
- both query() return the exact same thing and can use the same parsing logic
- 3 main types of messages that are important: usermessage,assistantmessage,resultmessage
- only user and asisstnat have .content attriburtes
- 3 main types of blocks: textblock, tooluseblock, toolcallblock
'''

from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, query, ClaudeSDKClient
import asyncio

async def basic():

    # query returns an iterator of message items
    async for message in query(prompt ="Is it true that claude agents sdk is built on top of claude code? if so what happens under the hood?"):

        if isinstance(message, AssistantMessage):

            for block in message.content:

                if isinstance(block,TextBlock):
                    print(block.text)

async def medium():

    # you have to create a sdk client object so use parenteheses ()
    async with ClaudeSDKClient() as client:

        await client.query("is the claude agent sdk built on top of claude code? refer to the official documentation to find an answer. if you don't know say you don't know.")

        async for message in client.receive_response():

            if isinstance(message,AssistantMessage):
                for block in message.content:
                    if isinstance(block,ToolUseBlock):
                        print(f"Tool name: {block.name} and input is: {block.input}")

            elif isinstance(message,UserMessage):
                for block in message.content:
                    if isinstance(block,ToolResultBlock):
                        print(f"Tool output is {block.content}")

            elif isinstance(message,ResultMessage):
                print(f"final output: {message.result}")



if __name__=="__main__":

    asyncio.run(medium())