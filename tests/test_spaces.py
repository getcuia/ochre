"""Test suite for RGB and HCL color spaces."""

from typing import Text

import pytest
from hypothesis import given

from melanin import RGB, Ansi256, Color, Hex, WebColor

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
    "rgb,hex_string",
    [
        (RGB(0, 0, 0), "0x0"),
        (RGB(0, 0, 1), "0xff"),
        (RGB(0, 1, 0), "0xff00"),
        (RGB(1, 0, 0), "0xff0000"),
        (RGB(1, 1, 1), "0xffffff"),
    ],
)
def test_hex_representation(rgb: RGB, hex_string: Text) -> None:
    """Test conversion to hexadecimal."""
    assert hex(rgb) == hex_string


@pytest.mark.parametrize(
    "hex_string,rgb",
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
def test_hex_parsing(hex_string: Text, rgb: RGB) -> None:
    """Test conversion to hexadecimal."""
    assert Hex(hex_string).rgb == rgb


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


@pytest.mark.parametrize(
    "webcolor",
    [
        WebColor("white"),
        WebColor("silver"),
        WebColor("gray"),
        WebColor("black"),
        WebColor("red"),
        WebColor("maroon"),
        WebColor("yellow"),
        WebColor("olive"),
        WebColor("lime"),
        WebColor("green"),
        WebColor("aqua"),
        WebColor("teal"),
        WebColor("blue"),
        WebColor("navy"),
        WebColor("fuchsia"),
        WebColor("purple"),
    ],
)
def test_name_color(webcolor) -> None:
    """Test the name color."""
    assert webcolor.hex.web_color == webcolor
    assert webcolor.rgb.web_color == webcolor
    assert webcolor.hcl.web_color == webcolor


@pytest.mark.parametrize(
    "i,color",
    [
        (0, Hex("#000000")),
        (1, Hex("#800000")),
        (2, Hex("#008000")),
        (3, Hex("#808000")),
        (4, Hex("#000080")),
        (5, Hex("#800080")),
        (6, Hex("#008080")),
        (7, Hex("#c0c0c0")),
        (8, Hex("#808080")),
        (9, Hex("#ff0000")),
        (10, Hex("#00ff00")),
        (11, Hex("#ffff00")),
        (12, Hex("#0000ff")),
        (13, Hex("#ff00ff")),
        (14, Hex("#00ffff")),
        (15, Hex("#ffffff")),
        (50, Hex("#00ffd7")),
        (100, Hex("#878700")),
        (150, Hex("#afd787")),
        (200, Hex("#ff00d7")),
        (250, Hex("#bcbcbc")),
    ],
)
def test_ansi256(i: int, color: Color) -> None:
    """Test correctness of ANSI 256 colors."""
    assert Ansi256(i) == color
