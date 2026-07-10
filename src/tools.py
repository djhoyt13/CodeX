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


_MILES_TO_KM: Final = 1.60934

_UNIT_ALIASES: Final = {
    "mile": "miles",
    "miles": "miles",
    "mi": "miles",
    "km": "km",
    "kilometer": "km",
    "kilometers": "km",
    "kilometre": "km",
    "kilometres": "km",
}


def _normalize_unit(unit: str) -> str | None:
    """Map common unit names to canonical miles/km labels."""
    return _UNIT_ALIASES.get(unit.strip().lower())


def convert_units(value: float | str, from_unit: str, to_unit: str) -> float:
    """Convert between miles and kilometers."""
    from_canonical = _normalize_unit(from_unit)
    to_canonical = _normalize_unit(to_unit)
    if from_canonical is None or to_canonical is None:
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")

    numeric_value = float(value)
    if from_canonical == to_canonical:
        return numeric_value
    if from_canonical == "miles" and to_canonical == "km":
        return numeric_value * _MILES_TO_KM
    if from_canonical == "km" and to_canonical == "miles":
        return numeric_value / _MILES_TO_KM
    raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")


@function_tool
def convert(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a numeric value between miles and kilometers (supports aliases like mi and kilometers)."""
    try:
        return str(convert_units(value, from_unit, to_unit))
    except ValueError as exc:
        return f"Conversion error: {exc}"
