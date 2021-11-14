"""Test suite for RGB and HCL color spaces."""

from typing import Text

import pytest
from hypothesis import given

from melanin import RGB

from .test_colorsys import between_0_and_1


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_hcl_roundtrip(r: float, g: float, b: float) -> None:
    """Test roundtrip conversion from RGB to HCL and back."""
    rgb = RGB(r, g, b)
    rgb2 = rgb.hcl.rgb
    assert (rgb.red, rgb.green, rgb.blue) == pytest.approx(
        (rgb2.red, rgb2.green, rgb2.blue), rel=1e-9, abs=1e-6
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
def test_hex(rgb: RGB, hexstr: Text) -> None:
    """Test conversion to hexadecimal."""
    assert hex(rgb) == hexstr
