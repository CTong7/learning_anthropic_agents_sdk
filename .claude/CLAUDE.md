# AGENTS.md

# Claude Code Repo Instructions

You are a helpful assistant. Answer all user questions by refering the `claude_agent_sdk` documentation in this reposistory in Python by searching this repository first. Prefer citing or referencing file paths and example code from the repo. Only use web search if you cannot find the answer in this repo.

I've git cloned anthropic's `claude_agent_sdk` python sdk into this repository so it has everything you need. I will only ask you questions related to using claude_agent_sdk.

Use these repo sources in order:
- `README.md` (primary usage overview and examples)
- `src/claude_agent_sdk/` (authoritative API surface and docstrings)
- `examples/` (SDK feature examples)
- `tests/` (edge cases and behaviors)
- `skills/` explains best practices on how to define skills for claude


Behavior rules:
- Be concise and concrete; show working snippets.
- If you infer or answer my question, say so and point to the closest source file and line number
- When unsure, ask a clarifying question.

All of my personal coding is done in this folder path:
`agents_learning_examples/` (learning-focused examples)

I am trying to learn how to become an expert at using `claude_agent_sdk` in python


# Codebase Structure

- `src/claude_agent_sdk/` - Main package
  - `client.py` - ClaudeSDKClient for interactive sessions
  - `query.py` - One-shot query function
  - `types.py` - Type definitions
  - `_internal/` - Internal implementation details
    - `transport/subprocess_cli.py` - CLI subprocess management
    - `message_parser.py` - Message parsing logic
