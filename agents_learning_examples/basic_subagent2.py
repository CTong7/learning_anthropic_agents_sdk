
from claude_agent_sdk import AgentDefinition, AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock, query

import asyncio

'''
steps:
1. define agent
2. pass into agent options
3. define task tool to spawn agent
4. updates ystem prompt to spawn that agent
'''

agent_smith = AgentDefinition(
    # learn: description should specify when this agent is used
    description = "Creates Agent Smith to engage in matrix role play. Used when matrix role play is necessary.",
    prompt="You are agent smith from the movie trilogy the Matrix. You are an agent from the matrix and you respond like you're from the movie.",
    model = "haiku"
)

options = ClaudeAgentOptions(
    agents = {"agent-smith": agent_smith},
    allowed_tools=["Task"],
    system_prompt= " You are a helpful assistant. Use agent-smith agent when doing matrix role play.", #todo: add specific instruction ot use,
    model = "sonnet"

)

async def main():
    
    async for message in query(prompt = "i challenge you to a fight. prepare to die.", options = options):

        if isinstance(message,AssistantMessage):

            for block in message.content:
                if isinstance(block,ToolUseBlock):
                    print(f"Tool Call: {block.name}")

        
        elif isinstance(message,ResultMessage):

            print(f"Agent: {message.result}")
            




if __name__=="__main__":

    asyncio.run(main())