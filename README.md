# First Agent Demo

A deliberately small Python project showing how four agent-building concepts fit together:

| Concept | File | Who reads it? | Purpose |
| --- | --- | --- | --- |
| Runtime system prompt | `prompts/system_prompt.md` | The agent model at runtime | Defines the agent's role, rules, and tool-use behavior. |
| Repository instructions | `AGENTS.md` | Codex | Tells Codex how to work safely and consistently in this repository. |
| Codex skill | `.agents/skills/agent-project-review/SKILL.md` | Codex, when selected or matched | Packages a reusable workflow for reviewing or extending the project. |
| Runtime tools | `src/tools.py` | The runtime agent through the Agents SDK | Gives the agent deterministic capabilities beyond text generation. |

`AGENTS.md` is plural and uppercase. It is not the same thing as the runtime agent's system prompt.

## How the agent loop works

1. `src/main.py` loads `prompts/system_prompt.md`.
2. It creates an `Agent` and registers two tools.
3. `Runner.run_sync(...)` sends the user request and instructions to the model.
4. The model either answers directly or requests a tool call.
5. The SDK executes the selected Python tool and returns its result to the model.
6. The model produces the final response.

The included tools are:

- `calculate`: safely evaluates basic arithmetic.
- `get_project_fact`: retrieves facts about the teaching project.

## Setup in Cursor

Open a terminal at the repository root and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Create an API key in the OpenAI platform, then set it in the terminal. Do not commit the key.

macOS or Linux:

```bash
export OPENAI_API_KEY="your-key-here"
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-key-here"
```

## Run the demonstrations

Force the arithmetic tool to be used:

```bash
python -m src.main "What is (17 * 6) + 9?"
```

Force the project-fact tool to be used:

```bash
python -m src.main "What is the difference between AGENTS.md and the system prompt in this project?"
```

Ask something that needs no tool:

```bash
python -m src.main "Give me a one-sentence definition of an AI agent."
```

## Test the deterministic logic

```bash
python -m pytest
```

The tests do not call the OpenAI API.

## Use the Codex skill

In the Codex IDE extension, start a new session from this repository so Codex reloads `AGENTS.md` and discovers the repository skill. Then either:

- Type `$` or use `/skills` and select `agent-project-review`, or
- Ask: `Use the agent-project-review skill to explain this repository.`

A useful first Codex task is:

```text
Use the agent-project-review skill to inspect this teaching project. Explain how the runtime system prompt, AGENTS.md, the skill, and the Python tools affect different parts of execution. Do not change any files.
```

## Suggested next experiment

Add a third runtime tool such as a local unit converter. Update the system prompt so the agent must use that tool for conversions, add deterministic tests, and use the Codex review skill to verify the separation of responsibilities.
