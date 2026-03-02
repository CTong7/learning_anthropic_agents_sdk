from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

import asyncio
'''
# learn: in this instance, we use 2 seperate query statements, both of these start 2 seperate conversations

# learn: the second query doesn't know what the first query asked
'''
options = ClaudeAgentOptions(
    model = "haiku"
)

async def main():
    
    async for message in query(prompt = " whats the weather in london today?",options = options):
        if isinstance(message,AssistantMessage):

            for block in message.content:
                if isinstance(block,TextBlock):
                    print(f"AI answer 1: {block.text}")
    
    async for message in query(prompt = "what was my first message in this conversation?",options = options):

        if isinstance(message,AssistantMessage):

            for block in message.content:
                if isinstance(block,TextBlock):
                    print(f"AI answer 2: {block.text}")



if __name__=="__main__":
    asyncio.run(main())