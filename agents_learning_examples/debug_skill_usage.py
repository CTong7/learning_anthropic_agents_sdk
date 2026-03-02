from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, SystemMessage, query, ClaudeAgentOptions
import asyncio
import json

options = ClaudeAgentOptions(
    allowed_tools = ["Skill","Bash"],
    model = "sonnet",
    cwd = ".",
    setting_sources=["project"],
    system_prompt = """
    you are a helpful assistant.

    If the user asks any information regarding PDF files, use your PDF Skill to analyze the pdf file and then answer the user's question.
    """,
    max_turns = 10  # Increase to ensure we have enough turns
)

async def main():
    turn_count = 0

    async for message in query(
        # prompt = "What is my total monthly spending in this PDF file agents_learning_examples/2026-01-15_Statement.pdf? Please tell me the number.",
        prompt = "Show me the first 50 lines of this pdf file:  agents_learning_examples/2026-01-15_Statement.pdf? Based on the output is this a debit or credit card statement? What is the name of this bank account type?",
        options = options
    ):
        print(f"\n{'='*60}")
        print(f"MESSAGE TYPE: {type(message).__name__}")
        print(f"{'='*60}")

        if isinstance(message, SystemMessage):
            print(f"SystemMessage subtype: {message.subtype}")
            if message.subtype == "init":
                skills = message.data.get("skills", [])
                print(f"🔧 Available skills: {skills}")

            print(f"Data: {json.dumps(message.data, indent=2)}")

        elif isinstance(message, AssistantMessage):
            turn_count += 1
            print(f"🤖 Assistant Turn #{turn_count}")
            print(f"This is the Parent Tool Use ID: {message.parent_tool_use_id}")
            print(f"Number of content blocks: {len(message.content)}")

            for i, block in enumerate(message.content):
                print(f"\n  Block {i+1}: {type(block).__name__}")

                if isinstance(block, ToolUseBlock):
                    print(f"    Tool: {block.name}")
                    print(f"    Input: {json.dumps(block.input, indent=6)}")

                elif isinstance(block, TextBlock):
                    print(f"    Text: {block.text[:200]}...")  # First 200 chars
                    print(f"\n📝 ASSISTANT RESPONSE:\n{block.text}")

        elif isinstance(message, UserMessage):
            print(f"👤 User/Tool Response")
            print(f"This is the Parent Tool Use ID: {message.parent_tool_use_id}")
            print(f"Content type: {type(message.content)}")

            if isinstance(message.content, list):
                for i, block in enumerate(message.content):
                    print(f"\n  Block {i+1}: {type(block).__name__}")

                    if isinstance(block, ToolResultBlock):
                        content_preview = str(block.content)[:200]
                        print(f"    Tool result (first 200 chars): {content_preview}...")
                        print(f"    Full length: {len(str(block.content))} chars")

        elif isinstance(message, ResultMessage):
            print(f"✅ FINAL RESULT MESSAGE")
            print(f"Subtype: {message.subtype}")
            print(f"Is error: {message.is_error}")
            print(f"Num turns: {message.num_turns}")
            print(f"Duration: {message.duration_ms}ms")

            if message.result:
                print(f"\n🎯 FINAL ANSWER:\n{message.result}")
            else:
                print(f"\n⚠️  WARNING: Result is None!")
                print(f"Structured output: {message.structured_output}")

        else:
            print(f"⚠️  Unknown message type: {type(message)}")

if __name__=="__main__":
    asyncio.run(main())
