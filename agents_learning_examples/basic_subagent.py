from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, ToolUseBlock, query, AgentDefinition

import asyncio

'''
your agent can spawn and invoke subagents
- to create new context windows
- handle well defined tasks
- run multiple sub agents in parallel
- create agents with specialized instructions

# learn: 3 main ways to use agents:
1. pass the agents parameter in Claude AgentOptions

2. define subagents via markdown files inside of .claude/agents/ folder

3. built in sub agents - claude can invoke the built-in general-purpose sub agent any time using the TASK TOOL
- the task tool naturally spawns sub agents

#learn: subagents NOT main agents take the class of AgentDefinition() class
- takes 4 args
- 2 mandatory are description and prompt
- 2 optional are model and tools
'''

# agents: dict[str, AgentDefinition] | None = None
'''
the arg is a dictionary of string or 
'''

# Step 1: define a SUB AGENT using Agent Definition
#! the main agent is defined only using claude agent options
# but SUB-agents use Agent Definition class

code_reviewer_agent = AgentDefinition(
    description = "Expert code review specialist. Use for quality, security and maintainability reviews",
    prompt = """
    You are a code review specialist with expertise in security, performance and best practices.
    When reviewing code:
    - Identify security vulnerabilities
    - Check for performance issues
    - Verify adherence to coding standards
    - Suggest specific improvements

    Be thorough but concise in your feedback.
    """ ,
    tools = ["Read","Grep","Glob"], #providing read only tools
    model = "sonnet" # override default model for this subagent, otherwise it takes the parent

)

lover_boy_agent = AgentDefinition(
    description = " You are a certified lover boy. Use when I need love and need affirmation.",
    prompt = """
    You are a certified lover boy.

    When I'm feeling down. Give me words of encouragement to build my confidence, remind me of my inherit worth as a human being and make me feel loved.

    """,
    model = "haiku"
)

# this is the prompt verbatim that gets sent to claude api
print(repr(code_reviewer_agent.prompt))


# step 2: pass sub-agent into claude agent options as a dictionary of {"agent_name": AgentDefinition}
options = ClaudeAgentOptions(
    agents = {"code-reviewer":code_reviewer_agent, "lover-boy":lover_boy_agent}, #learn: this syntax for passing sub agents to main agent
    # learn: name your agents using dashes
    model = "sonnet",
    allowed_tools = ["Read","Grep", "Glob","Task"] #! learn: the TASK TOOL IS MANDATORY TO PASS IN FOR THE ORCHESTRATOR TO SPAWN SUBAGENTS

)


async def main():

    async for message in query(
        prompt = "I'm feeling a bit down because of dating and feeling pressure and needing female validation.",
        options = options
        ):


        if isinstance(message,AssistantMessage):
            for block in message.content:
                if isinstance(block,TextBlock):
                    print(f"agent: {block.text}")

                elif isinstance(block,ToolUseBlock):
                    print(f"Tool Call: {block.name}")


if __name__=="__main__":
    asyncio.run(main())