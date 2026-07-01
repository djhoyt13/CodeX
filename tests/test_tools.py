import pytest

from src.tools import convert_units, safe_calculate


def test_safe_calculate_handles_arithmetic() -> None:
    assert safe_calculate("(12 * 4) + 3") == 51


def test_safe_calculate_handles_unary_values() -> None:
    assert safe_calculate("-5 + 2") == -3


def test_safe_calculate_rejects_function_calls() -> None:
    with pytest.raises(ValueError, match="Only basic arithmetic"):
        safe_calculate("__import__('os').system('echo unsafe')")


def test_convert_units_handles_miles_to_km() -> None:
    assert convert_units("100", "miles", "km") == pytest.approx(160.934)


def test_convert_units_handles_km_to_miles() -> None:
    assert convert_units("100", "km", "miles") == pytest.approx(62.1371, rel=1e-4)


def test_convert_units_accepts_unit_aliases() -> None:
    assert convert_units(5, "miles", "kilometers") == pytest.approx(8.0467, rel=1e-4)


def test_convert_units_rejects_unsupported_conversion() -> None:
    with pytest.raises(ValueError, match="Unsupported unit conversion"):
        convert_units("100", "miles", "feet")
