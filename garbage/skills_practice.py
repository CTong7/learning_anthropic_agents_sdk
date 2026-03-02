from mcp.types import Result
from claude_agent_sdk import ClaudeAgentOptions, ToolUseBlock,query, AssistantMessage,ResultMessage,UserMessage
import asyncio

'''
to define a skill

1. pass in Skill and Bash into allowed_tools
also set the following params:
- cwd ie current working directory should point to repo root
- settings_sources = "project"
'''

options = ClaudeAgentOptions(

    cwd = "/Users/christong/Documents/learn_anthropic_agents_sdk",
    setting_sources=["project"],
    allowed_tools = ["Skill","Bash"]
)
async def main():
    
    async for message in query(prompt = "In my repo please find the .pdf file that contains my bank statement use your pdf skill to analyze it and tell me the monthly expenditure",options = options):

        if isinstance(message,AssistantMessage):

            for block in message.content:
                if isinstance(block,ToolUseBlock):
                    print(f"Tool called: {block.name}",end = "\n")

        elif isinstance(message,ResultMessage):

            print(f"Answer: {message.result}")

if __name__=="__main__":
    asyncio.run(main())