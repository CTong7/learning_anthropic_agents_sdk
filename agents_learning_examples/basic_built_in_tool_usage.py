from claude_agent_sdk import AssistantMessage, TextBlock, query, ClaudeAgentOptions
import asyncio

async def main():

    # learn: set the tools in ClaudeAgentOptions

    options = ClaudeAgentOptions(
        tools = ["Read","Write","Bash"],
        permission_mode="acceptEdits",
        model = "sonnet",
        max_turns = 5
    )

    async for message in query(prompt = "what are the main files inside of my agents_learning_examples folder?",options = options):
        print(message)
        print(f"This is the class of the message: {message}")
        if isinstance(message,AssistantMessage):
            
            # learn: loop through list of content blocks from message
            for block in message.content:

                if isinstance(block,TextBlock):
                    print(block.text)


if __name__== "__main__":
    asyncio.run(main())