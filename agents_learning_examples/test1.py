from claude_agent_sdk import query, ClaudeAgentOptions,AssistantMessage,TextBlock
import asyncio


async def main():

    async for result in query(prompt="how is the api key set in claude agents sdk? other than setting in env, what other other alternatives? can i pass into agent? or agent options?"):

        if isinstance(result, AssistantMessage):

            for block in result.content:

                if isinstance(block,TextBlock):
                    print(block.text)

if __name__=="__main__":
    asyncio.run(main())