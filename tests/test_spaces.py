"""Test suite for RGB and HCL color spaces."""

from typing import Text

import pytest
from hypothesis import given

from melanin import RGB, Hex

from .test_colorsys import between_0_and_1


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_hcl_roundtrip(r: float, g: float, b: float) -> None:
    """Test roundtrip conversion from RGB to HCL and back."""
    rgb = RGB(r, g, b)
    rgb2 = rgb.hcl.rgb
    assert (rgb2.red, rgb2.green, rgb2.blue) == pytest.approx(
        (rgb.red, rgb.green, rgb.blue), rel=1e-9, abs=1e-6
    )


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_hex_roundtrip(r: float, g: float, b: float) -> None:
    """Test roundtrip conversion from RGB to Hex and back."""
    rgb = RGB(r, g, b)
    rgb2 = rgb.hex.rgb
    assert (rgb2.red, rgb2.green, rgb2.blue) == pytest.approx(
        (rgb.red, rgb.green, rgb.blue), rel=1e-9, abs=4e-3
    )


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
    ],
)
def test_hex_parsing(hexstr: Text, rgb: RGB) -> None:
    """Test conversion to hexadecimal."""
    rgb2 = Hex(hexstr).rgb
    assert (rgb2.red, rgb2.green, rgb2.blue) == pytest.approx(
        (rgb.red, rgb.green, rgb.blue), rel=1e-9, abs=1e-6
    )
