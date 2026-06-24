"""Command-line entry point for the starter agent."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from agents import Agent, Runner
from dotenv import load_dotenv

from src.tools import calculate, get_project_fact

ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PROMPT_PATH = ROOT / "prompts" / "system_prompt.md"


def load_system_prompt() -> str:
    """Load the runtime system instructions from disk."""
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


def build_agent() -> Agent:
    """Construct the agent and register its available tools."""
    return Agent(
        name="Demo Guide",
        instructions=load_system_prompt(),
        tools=[calculate, get_project_fact],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a small OpenAI Agents SDK demonstration."
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Question for the agent. Omit it to use the interactive prompt.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and export the key "
            "in your terminal before running the demo."
        )

    user_input = " ".join(args.prompt).strip()
    if not user_input:
        user_input = input("Ask the demo agent: ").strip()
    if not user_input:
        raise SystemExit("A non-empty prompt is required.")

    result = Runner.run_sync(build_agent(), user_input)
    print("\nAgent response:\n")
    print(result.final_output)


if __name__ == "__main__":
    main()
