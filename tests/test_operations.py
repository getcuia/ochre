"""Test suite for operations on colors."""


from typing import Text

import pytest

from ochre import Color, Hex, WebColor


@pytest.mark.parametrize(
    "given,amount,expected", [(Hex("#D4F880"), 1.0, Hex("#a1c550"))]
)
def test_darken(given: Color, amount: float, expected: Color) -> None:
    """Test darkening of a color."""
    assert given.darken(amount).distance(expected) < 0.056

@pytest.mark.parametrize(
    "given,amount,expected", [(Hex("#ffc0cb"), 1.0, Hex("#ffb1c7"))]
)
def test_saturate(given: Color, amount: float, expected: Color) -> None:
    """Test saturation of a color."""
    assert given.saturate(amount).distance(expected) < 0.11
