from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, SystemMessage, query, ClaudeAgentOptions
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
    allowed_tools = ["Skill","Bash"],
    model = "sonnet",
    cwd = "/Users/christong/Documents/learn_anthropic_agents_sdk", #learn: this should be path to project repo
    setting_sources=["project"], #learn: this points to settings.json, great for project specific settings
    # learn: in order for claude to access the .claude/skills folder you must set setting_sources = ["project"],
    # setting it to local or user will not give it access to the folder that you wnat
    system_prompt = """
    you are a helpful assistant.

    If the user asks any information regarding PDF files, use your PDF Skill to analyze the pdf file and then answer the user's  question .
    """,
    max_turns = 10  # Increase for skill-based workflows that need multiple turns


)

async def main():

    async for message in query(prompt = "What is my total monthly spending in this PDF file agents_learning_examples/2026-01-15_Statement.pdf? Please tell me the number.",options = options):

        if isinstance(message, SystemMessage):
            # Check if skills are loaded
            if message.subtype == "init":
                skills = message.data.get("skills", [])
                print(f"🔧 Available skills: {skills}\n")

        elif isinstance(message, AssistantMessage):

            for block in message.content:
                if isinstance(block,ToolUseBlock):
                    print(f"Calling TOOL: {block.name}")
                    if block.name == "Skill":
                        print(f"  → Skill being invoked: {block.input.get('skill', 'unknown')}")
                    elif block.name == "Bash":
                        print(f"  → Command: {block.input.get('command', 'unknown')}")

                elif isinstance(block,TextBlock):
                    print(f"Ai Answer: {block.text}")

        elif isinstance(message,UserMessage):
            for block in message.content:
                if isinstance(block,ToolResultBlock):
                    # print(f"Tool output: {block.content}",end="\n")
                    print(f"Supressing tool output to unblock terminal printing")

        elif isinstance(message,ResultMessage):

            print(f"AI Answer: {message.result}")
            

if __name__=="__main__":
    asyncio.run(main())