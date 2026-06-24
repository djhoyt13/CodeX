"""Deterministic functions and agent-facing tools for the demo project."""

from __future__ import annotations

import ast
import operator
from typing import Final

from agents import function_tool

_BINARY_OPERATORS: Final = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: Final = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_calculate(expression: str) -> float | int:
    """Evaluate a small arithmetic expression without using ``eval``."""

    def evaluate(node: ast.AST) -> float | int:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return _BINARY_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is allowed.")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


@function_tool
def calculate(expression: str) -> str:
    """Calculate a basic arithmetic expression such as ``(12 * 4) + 3``."""
    try:
        return str(safe_calculate(expression))
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as exc:
        return f"Calculation error: {exc}"


_PROJECT_FACTS: Final = {
    "system prompt": "The runtime system prompt is stored in prompts/system_prompt.md and loaded by src/main.py.",
    "agents.md": "AGENTS.md gives Codex coding instructions for this repository; it is not the runtime agent's system prompt.",
    "skill": "The reusable Codex skill is .agents/skills/agent-project-review/SKILL.md.",
    "tools": "Runtime tools are Python functions decorated with @function_tool in src/tools.py.",
}


@function_tool
def get_project_fact(topic: str) -> str:
    """Return a fact about the demo's system prompt, AGENTS.md, skill, or tools."""
    normalized = topic.strip().lower()
    for key, fact in _PROJECT_FACTS.items():
        if key in normalized or normalized in key:
            return fact
    return "Available topics: system prompt, AGENTS.md, skill, and tools."
