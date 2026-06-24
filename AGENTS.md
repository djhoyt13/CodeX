# AGENTS.md

## Purpose

This repository is a teaching project that demonstrates four distinct agent concepts:

1. Runtime system instructions in `prompts/system_prompt.md`.
2. Codex repository guidance in this `AGENTS.md` file.
3. Reusable Codex workflows in `.agents/skills/`.
4. Runtime function tools in `src/tools.py`.

Keep those concepts separate when changing the project.

## Working agreements

- Use Python 3.11 or newer.
- Prefer small, readable functions with type hints and docstrings.
- Do not place API keys or secrets in source files.
- Run `python -m pytest` after changing Python code.
- Update `README.md` when behavior or setup changes.
- Keep the starter agent intentionally simple and instructional.

## Validation

Before proposing completion:

1. Run the unit tests.
2. Confirm `python -m src.main --help` succeeds.
3. Explain which files demonstrate system prompts, AGENTS.md guidance, skills, and tools.

## Skills

Use the `agent-project-review` skill when reviewing or extending the demo agent.