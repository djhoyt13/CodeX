import pytest

from src.tools import safe_calculate


def test_safe_calculate_handles_arithmetic() -> None:
    assert safe_calculate("(12 * 4) + 3") == 51


def test_safe_calculate_handles_unary_values() -> None:
    assert safe_calculate("-5 + 2") == -3


def test_safe_calculate_rejects_function_calls() -> None:
    with pytest.raises(ValueError, match="Only basic arithmetic"):
        safe_calculate("__import__('os').system('echo unsafe')")
