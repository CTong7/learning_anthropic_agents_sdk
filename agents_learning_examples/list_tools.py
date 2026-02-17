import anyio
from claude_agent_sdk import ClaudeAgentOptions, SystemMessage, query

async def main():
    options = ClaudeAgentOptions(
        tools={"type": "preset", "preset": "claude_code"},
        max_turns=1,
    )
    async for message in query(
        prompt="List available tools.",
        options=options,
    ):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            tools = message.data.get("tools", [])
            print("Tools:", tools)

anyio.run(main)
