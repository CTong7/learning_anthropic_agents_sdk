from claude_agent_sdk import AssistantMessage, TextBlock, query, ClaudeAgentOptions
import asyncio

async def main():

    user_query = " what are the most important classes I need to understand to use claude_agent_sdk?"
    
    # learn: define claude agent options
    options = ClaudeAgentOptions(
        system_prompt = "You are a helpful assistant. Answer all of my questions based on the anthropic claude agent python sdk documentation",
        max_turns=5,
        model = "claude-sonnet-4-5" #learn: syntax is claude-base_model_name -number-version

    )

    async for message in query(prompt = user_query,options = options):

        if isinstance(message,AssistantMessage):

            # 2nd for loop to loop trhoguh message content
            for block in message.content:
                if isinstance(block,TextBlock):
                    print(block.text)



if __name__=="__main__":
    asyncio.run(main())