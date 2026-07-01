---
name: add-runtime-tool
description: Add a new @function_tool to the demo agent while preserving separation between runtime prompt, AGENTS.md, skills, and tools.
---

# Add Runtime Tool

Use when adding a new tool to the starter agent.

1. Read `AGENTS.md` and inspect `src/tools.py`.
2. Add deterministic logic plus a `@function_tool` wrapper.
3. Register the tool in `src/main.py`.
4. Add a matching rule in `prompts/system_prompt.md`.
5. Add pytest coverage for the pure function.
6. Run `python -m pytest` and `python -m src.main --help`.
7. Do not put Codex workflow steps in the system prompt.