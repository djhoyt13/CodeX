---
name: agent-project-review
description: Review or extend this teaching agent while preserving the separation between runtime prompts, AGENTS.md guidance, Codex skills, and runtime tools.
---

# Agent Project Review

Use this workflow when asked to review, explain, or extend the starter agent.

1. Read `AGENTS.md` and `README.md` first.
2. Inspect `prompts/system_prompt.md` to understand runtime behavior.
3. Inspect `src/tools.py` before changing tool behavior.
4. Keep Codex-only instructions out of the runtime system prompt.
5. Keep runtime agent behavior out of `AGENTS.md` unless it is a coding convention.
6. Add or update tests for deterministic Python logic.
7. Run `python -m pytest`.
8. Summarize changes under these headings:
   - System prompt
   - AGENTS.md
   - Skill
   - Runtime tools
   - Tests
