"""Test suite for RGB and HCL color spaces."""

from typing import Text

import pytest
from hypothesis import given

from melanin import RGB, Hex, WebColor

from .test_colorsys import between_0_and_1


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_hcl_roundtrip(r: float, g: float, b: float) -> None:
    """Test roundtrip conversion from RGB to HCL and back."""
    rgb = RGB(r, g, b)
    assert rgb.hcl.rgb == rgb


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_hex_roundtrip(r: float, g: float, b: float) -> None:
    """Test roundtrip conversion from RGB to Hex and back."""
    rgb = RGB(r, g, b)
    assert rgb.hex.rgb == rgb


@pytest.mark.parametrize(
    "rgb,hexstr",
    [
        (RGB(0, 0, 0), "0x0"),
        (RGB(0, 0, 1), "0xff"),
        (RGB(0, 1, 0), "0xff00"),
        (RGB(1, 0, 0), "0xff0000"),
        (RGB(1, 1, 1), "0xffffff"),
    ],
)
def test_hex_representation(rgb: RGB, hexstr: Text) -> None:
    """Test conversion to hexadecimal."""
    assert hex(rgb) == hexstr


@pytest.mark.parametrize(
    "hexstr,rgb",
    [
        ("0x0", RGB(0, 0, 0)),
        ("0xff", RGB(0, 0, 1)),
        ("0xff00", RGB(0, 1, 0)),
        ("0xff0000", RGB(1, 0, 0)),
        ("0xffffff", RGB(1, 1, 1)),
        ("0", RGB(0, 0, 0)),
        ("ff", RGB(0, 0, 1)),
        ("ff00", RGB(0, 1, 0)),
        ("ff0000", RGB(1, 0, 0)),
        ("ffffff", RGB(1, 1, 1)),
        ("000000", RGB(0, 0, 0)),
        ("0000ff", RGB(0, 0, 1)),
        ("00ff00", RGB(0, 1, 0)),
        ("ff0000", RGB(1, 0, 0)),
        ("ffffff", RGB(1, 1, 1)),
        ("#000000", RGB(0, 0, 0)),
        ("#0000ff", RGB(0, 0, 1)),
        ("#00ff00", RGB(0, 1, 0)),
        ("#ff0000", RGB(1, 0, 0)),
        ("#ffffff", RGB(1, 1, 1)),
    ],
)
def test_hex_parsing(hexstr: Text, rgb: RGB) -> None:
    """Test conversion to hexadecimal."""
    assert Hex(hexstr).rgb == rgb


@pytest.mark.parametrize(
    "webcolor,rgb",
    [
        (WebColor("white"), RGB(1, 1, 1)),
        (WebColor("silver"), RGB(0.75, 0.75, 0.75)),
        (WebColor("gray"), RGB(0.5, 0.5, 0.5)),
        (WebColor("black"), RGB(0, 0, 0)),
        (WebColor("red"), RGB(1, 0, 0)),
        (WebColor("maroon"), RGB(0.5, 0, 0)),
        (WebColor("yellow"), RGB(1, 1, 0)),
        (WebColor("olive"), RGB(0.5, 0.5, 0)),
        (WebColor("lime"), RGB(0, 1, 0)),
        (WebColor("green"), RGB(0, 0.5, 0)),
        (WebColor("aqua"), RGB(0, 1, 1)),
        (WebColor("teal"), RGB(0, 0.5, 0.5)),
        (WebColor("blue"), RGB(0, 0, 1)),
        (WebColor("navy"), RGB(0, 0, 0.5)),
        (WebColor("fuchsia"), RGB(1, 0, 1)),
        (WebColor("purple"), RGB(0.5, 0, 0.5)),
    ],
)
def test_html_basic_colors(webcolor, rgb) -> None:
    """Test the sixteen basic HTML color names."""
    assert webcolor.rgb == rgb
