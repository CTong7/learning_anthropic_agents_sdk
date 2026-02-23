from claude_agent_sdk import AssistantMessage, ResultMessage, ToolUseBlock, query, ClaudeAgentOptions
import asyncio

'''
In order to enable agents to use skills you need to set 3 parameters

1. set allowed_tools = Skill
2. set the setting_sources to allow claude to access file systes
- SettingSource = Literal["user", "project", "local"]
- only 3 values for settingSource
- it controls which filesystem the sdk loads
- if you don't set this value, NO FILESYSTEM SETTINGS ARE LOADED, which keeps the sdk isolated
- these 3 values point to different SETTINGS.JSON files

3. cwd is the directory of the skills folder

'''
options = ClaudeAgentOptions(
    allowed_tools = ["Skill"],
    cwd = ".claude/skills/",
    setting_sources=["local"]


)

async def main():
    
    async for message in query(prompt = "What is the total monthly spend in this bank account statement?",options = options):

        if isinstance(message, AssistantMessage):

            for block in message.content:
                if isinstance(block,ToolUseBlock):
                    print(f"Calling TOOL: {block.name}")

        elif isinstance(message,ResultMessage):

            print(f"AI Answer: {message.result}")
            

if __name__=="__main__":
    asyncio.run(main())