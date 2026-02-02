'''
basic usage:
1. define agent using AgentDefintion
2. run an agent via query
'''

from claude_agent_sdk import query, ClaudeAgentOptions,AssistantMessage,TextBlock
import asyncio

# learn: query is the main agent runner/ sends request to claude api
# it returns an Async Iterator of response messages (__next__)
async def main():
    
    # ! for vs. async for --> for lets you iterate over a normal iterator, async for lets you iterate over an async iterable, awaiting each item as it becomes avaialble without blocking event loop
    # async for only works inside of an async def function
    async for message in query(prompt = "You are a helpful assistant for answering my questions based on claude_agent_sdk documentation in python"):

        if isinstance(message,AssistantMessage):
            
            #learn: if its a TextBlock, then we want to use block.text attribute
            for block in message.content:
                if isinstance(block,TextBlock):
                    print(block.text)



if __name__=="__main__":
    asyncio.run(main())