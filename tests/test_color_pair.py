"""Tests for color pairs."""

from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given

from ochre import ColorPair
from ochre.spaces import RGB, Hex

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


@given(
    rf=between_0_and_1,
    gf=between_0_and_1,
    bf=between_0_and_1,
    rb=between_0_and_1,
    gb=between_0_and_1,
    bb=between_0_and_1,
)
def test_color_pairs_are_immutable(
    rf: float, gf: float, bf: float, rb: float, gb: float, bb: float
):
    """Test that color pairs are immutable."""
    foreground = RGB(rf, gf, bf)
    background = RGB(rb, gb, bb)
    color_pair = ColorPair(foreground, background)

    with pytest.raises(FrozenInstanceError):
        color_pair.foreground = background

    with pytest.raises(FrozenInstanceError):
        color_pair.background = foreground


@given(
    rf=between_0_and_1,
    gf=between_0_and_1,
    bf=between_0_and_1,
    rb=between_0_and_1,
    gb=between_0_and_1,
    bb=between_0_and_1,
)
def test_color_pairs_can_be_used_as_dict_keys(
    rf: float, gf: float, bf: float, rb: float, gb: float, bb: float
):
    """Test that color pairs can be used as dict keys."""
    foreground = RGB(rf, gf, bf)
    background = RGB(rb, gb, bb)
    color_pair = ColorPair(foreground, background)

    assert color_pair in {color_pair: None}


@pytest.mark.parametrize(
    "pair,contrast_ratio",
    [
        (ColorPair(Hex("#000000"), Hex("#000000")), 1.0),
        (ColorPair(Hex("#000000"), Hex("#ffffff")), 21.0),
        (ColorPair(Hex("#0000ff"), Hex("#00ff00")), 6.26),
        (ColorPair(Hex("#0000ff"), Hex("#ff0000")), 2.14),
        (ColorPair(Hex("#00ff00"), Hex("#0000ff")), 6.26),
        (ColorPair(Hex("#00ff00"), Hex("#ff0000")), 2.91),
        (ColorPair(Hex("#ff0000"), Hex("#0000ff")), 2.14),
        (ColorPair(Hex("#ff0000"), Hex("#00ff00")), 2.91),
        (ColorPair(Hex("#ffffff"), Hex("#000000")), 21.0),
        (ColorPair(Hex("#ffffff"), Hex("#ffffff")), 1.0),
    ],
)
def test_contrast_ratio(pair: ColorPair, contrast_ratio: float) -> None:
    """Test contrast ratio calculation."""
    assert pair.contrast_ratio == pytest.approx(contrast_ratio, 0.005)
