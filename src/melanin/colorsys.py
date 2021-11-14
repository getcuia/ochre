"""
Drop-in replacement for the [standard `colorsys` module](https://docs.python.org/3/library/colorsys.html).

This module provides extra functionality to the standard `colorsys` module, but also
re-exports its contents for convenience.

Examples
--------
>>> from melanin import colorsys

This module provides conversions between RGB and XYZ coordinates:

>>> colorsys.rgb_to_xyz(0.2, 0.4, 0.4)  # doctest: +NUMBER
(0.09, 0.11, 0.14)
>>> colorsys.xyz_to_rgb(0.09, 0.11, 0.14)  # doctest: +NUMBER
(0.2, 0.4, 0.4)

The standard coversions are still available:

>>> colorsys.rgb_to_hsv(0.2, 0.4, 0.4)
(0.5, 0.5, 0.4)
>>> colorsys.hsv_to_rgb(0.5, 0.5, 0.4)
(0.2, 0.4, 0.4)
"""


from __future__ import annotations

from colorsys import (
    hls_to_rgb,
    hsv_to_rgb,
    rgb_to_hls,
    rgb_to_hsv,
    rgb_to_yiq,
    yiq_to_rgb,
)

__all__ = [
    # Re-exported from colorsys
    "hls_to_rgb",
    "hsv_to_rgb",
    "rgb_to_hls",
    "rgb_to_hsv",
    "rgb_to_yiq",
    "yiq_to_rgb",
    # New functions
    "rgb_to_xyz",
    "xyz_to_rgb",
]


def rgb_to_xyz(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert the color from RGB coordinates to XYZ coordinates."""
    if r > 0.04045:
        r = ((r + 0.055) / 1.055) ** 2.4
    else:
        r = r / 12.92
    if g > 0.04045:
        g = ((g + 0.055) / 1.055) ** 2.4
    else:
        g = g / 12.92
    if b > 0.04045:
        b = ((b + 0.055) / 1.055) ** 2.4
    else:
        b = b / 12.92

    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    return x, y, z


def xyz_to_rgb(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Convert the color from XYZ coordinates to RGB coordinates."""
    # We're using a higher precision matrix here see
    # <https://en.wikipedia.org/wiki/SRGB#sYCC_extended-gamut_transformation>
    red = 3.2406254 * x - 1.537208 * y - 0.4986286 * z
    green = -0.9689307 * x + 1.8757561 * y + 0.0415175 * z
    blue = 0.0557101 * x - 0.2040211 * y + 1.0569959 * z

    if red > 0.0031308:
        red = 1.055 * (red ** (1 / 2.4)) - 0.055
    else:
        red = 12.92 * red
    if green > 0.0031308:
        green = 1.055 * (green ** (1 / 2.4)) - 0.055
    else:
        green = 12.92 * green
    if blue > 0.0031308:
        blue = 1.055 * (blue ** (1 / 2.4)) - 0.055
    else:
        blue = 12.92 * blue

    return _clamp(red), _clamp(green), _clamp(blue)


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """
    Clamp a value to a range.

    Examples
    --------
    >>> _clamp(-0.5)
    0.0
    >>> _clamp(0.5)
    0.5
    >>> _clamp(1.5)
    1.0
    """
    return max(min_value, min(value, max_value))
