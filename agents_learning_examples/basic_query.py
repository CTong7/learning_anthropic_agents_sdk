from claude_agent_sdk import AssistantMessage, TextBlock, query, ClaudeAgentOptions

import asyncio

async def main():

    # step 1: define an async for loop to loop over iterator object returned from query
    async for message in query(prompt = "Tell me how to get started with claude agent teams swarms"):

        if isinstance(message,AssistantMessage):
            
            # step 2: define sync for loop to loop over the AssistantMessage Block
            for block in message.content:
                
                # step 3: look for a text block and print it out
                if isinstance(block,TextBlock):
                    print(block.text)


if __name__=="__main__":
    asyncio.run(main())