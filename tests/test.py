from claude_agent_sdk import ClaudeAgentOptions, query, AssistantMessage, TextBlock
import asyncio

options = ClaudeAgentOptions(
    model = "haiku",
    max_turns = 1

)

async def main():

    async for response in query(prompt = "How are you doing?", options = options):

        if isinstance(response,AssistantMessage):
            # learn: you can't loop the response, you need to access content attribute
            for block in response.content:
                if isinstance(block,TextBlock):
                    print(block.text)

if __name__=="__main__":
    asyncio.run(main())