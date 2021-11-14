"""
Drop-in replacement for the [standard `colorsys` module](https://docs.python.org/3/library/colorsys.html).

This module provides extra functionality to the standard `colorsys` module, but also
re-exports its contents for convenience.

Examples
--------
>>> from melanin import colorsys

This module provides conversions between RGB and XYZ coordinates:

>>> colorsys.rgb_to_xyz(0.2, 0.4, 0.4)
(1.0, 0.1, 0.1)
>>> colorsys.xyz_to_rgb(1.0, 0.1, 0.1)
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
    "hls_to_rgb",
    "hsv_to_rgb",
    "rgb_to_hls",
    "rgb_to_hsv",
    "rgb_to_yiq",
    "yiq_to_rgb",
]


def rgb_to_xyz(r, g, b) -> tuple[float, float, float]:
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
