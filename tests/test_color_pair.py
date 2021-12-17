"""Tests for color pairs."""

from hypothesis import given

from ochre import ColorPair
from ochre.spaces import RGB

from .test_colorsys import between_0_and_1


@given(
    rf=between_0_and_1,
    gf=between_0_and_1,
    bf=between_0_and_1,
    rb=between_0_and_1,
    gb=between_0_and_1,
    bb=between_0_and_1,
)
def test_can_create_color_pairs(
    rf: float, gf: float, bf: float, rb: float, gb: float, bb: float
):
    """Test that color pairs can be created."""
    foreground = RGB(rf, gf, bf)
    background = RGB(rb, gb, bb)
    color_pair = ColorPair(foreground, background)

    assert color_pair.foreground == foreground
    assert color_pair.background == background
