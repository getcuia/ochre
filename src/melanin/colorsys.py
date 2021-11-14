"""Simple color conversions.

This module is a drop-in replacement for the
[standard `colorsys` module](https://docs.python.org/3/library/colorsys.html).

It provides extra functionality to the standard `colorsys` module, but also re-exports
its contents for convenience.

Examples
--------
>>> from melanin import colorsys

This module provides some conversions, among which are:

1. RGB-XYZ:

>>> colorsys.rgb_to_xyz(0.2, 0.4, 0.4)  # doctest: +NUMBER
(0.09, 0.11, 0.14)
>>> colorsys.xyz_to_rgb(0.09, 0.11, 0.14)  # doctest: +NUMBER
(0.2, 0.4, 0.4)

2. RGB-LUV:

>>> colorsys.rgb_to_luv(0.2, 0.4, 0.4)  # doctest: +NUMBER
(0.4, -0.2, 0.0)
>>> colorsys.luv_to_rgb(0.4, -0.2, 0.0)  # doctest: +NUMBER
(0.2, 0.4, 0.4)

3. RGB-LCH:

>>> colorsys.rgb_to_lch(0.2, 0.4, 0.4)  # doctest: +NUMBER
(0.4, 0.2, 3.4)
>>> colorsys.lch_to_rgb(0.4, 0.2, 3.4)  # doctest: +NUMBER
(0.2, 0.4, 0.4)

For convenience, the module also re-exports the standard coversions from `colorsys`:

>>> colorsys.rgb_to_hsv(0.2, 0.4, 0.4)
(0.5, 0.5, 0.4)
>>> colorsys.hsv_to_rgb(0.5, 0.5, 0.4)
(0.2, 0.4, 0.4)
"""


from __future__ import annotations

import math
from colorsys import (
    hls_to_rgb,
    hsv_to_rgb,
    rgb_to_hls,
    rgb_to_hsv,
    rgb_to_yiq,
    yiq_to_rgb,
)

__all__ = [
    # Implemented in this module
    "lch_to_rgb",
    "luv_to_rgb",
    "rgb_to_lch",
    "rgb_to_luv",
    "rgb_to_xyz",
    "xyz_to_rgb",
    # Re-exported from colorsys
    "hls_to_rgb",
    "hsv_to_rgb",
    "rgb_to_hls",
    "rgb_to_hsv",
    "rgb_to_yiq",
    "yiq_to_rgb",
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
    r = 3.2406254 * x - 1.537208 * y - 0.4986286 * z
    g = -0.9689307 * x + 1.8757561 * y + 0.0415175 * z
    b = 0.0557101 * x - 0.2040211 * y + 1.0569959 * z

    if r > 0.0031308:
        r = 1.055 * (r ** (1 / 2.4)) - 0.055
    else:
        r = 12.92 * r
    if g > 0.0031308:
        g = 1.055 * (g ** (1 / 2.4)) - 0.055
    else:
        g = 12.92 * g
    if b > 0.0031308:
        b = 1.055 * (b ** (1 / 2.4)) - 0.055
    else:
        b = 12.92 * b

    return r, g, b


def luv_to_rgb(ell: float, u: float, v: float) -> tuple[float, float, float]:
    """Convert the color from LUV coordinates to RGB coordinates."""
    return xyz_to_rgb(*luv_to_xyz(ell, u, v))


def rgb_to_luv(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert the color from RGB coordinates to LUV coordinates."""
    return xyz_to_luv(*rgb_to_xyz(r, g, b))


def lch_to_rgb(ell: float, c: float, h: float) -> tuple[float, float, float]:
    """Convert the color from LCH coordinates to RGB coordinates."""
    return luv_to_rgb(*lch_to_luv(ell, c, h))


def rgb_to_lch(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert the color from RGB coordinates to LCH coordinates."""
    return luv_to_lch(*rgb_to_luv(r, g, b))


def xyz_to_luv(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Convert the color from XYZ coordinates to LUV coordinates."""
    u, v = _xyz_to_uv(x, y, z)

    if y > EPSILON:
        ell = 116 * y ** (1 / 3) - 16
    else:
        ell = KAPPA * y
    u, v = 13 * ell * (u - REF_UV_D65_2[0]), 13 * ell * (v - REF_UV_D65_2[1])

    return ell / 100, u / 100, v / 100


def luv_to_xyz(ell: float, u: float, v: float) -> tuple[float, float, float]:
    """Convert the color from LUV coordinates to XYZ coordinates."""
    if ell == 0:
        return 0, 0, 0

    ell, u, v = 100 * ell, 100 * u, 100 * v
    u, v = _luv_to_uv(ell, u, v)

    four_v = 4 * v
    if ell > 8:
        y = ((ell + 16) / 116) ** 3
    else:
        y = ell / KAPPA
    x, z = 9 * y * u / four_v, y * (12 - 3 * u - 20 * v) / four_v

    return x, y, z


def luv_to_lch(ell: float, u: float, v: float) -> tuple[float, float, float]:
    """Convert the color from LUV coordinates to LCH coordinates."""
    h = math.atan2(v, u)
    c = math.hypot(v, u)
    h = h + math.tau if h < 0 else h
    return ell, c, h


def lch_to_luv(ell: float, c: float, h: float) -> tuple[float, float, float]:
    """Convert the color from LCH coordinates to LUV coordinates."""
    u = c * math.cos(h)
    v = c * math.sin(h)
    return ell, u, v


def _xyz_to_uv(x: float, y: float, z: float) -> tuple[float, float]:
    """Convert the color from XYZ coordinates to uv chromaticity coordinates."""
    if x == y == 0:
        return 0, 0
    d = x + 15 * y + 3 * z
    return 4 * x / d, 9 * y / d


def _luv_to_uv(ell: float, u: float, v: float) -> tuple[float, float]:
    """Convert the color from LUV coordinates to uv chromaticity coordinates."""
    d = 13 * ell
    return u / d + REF_UV_D65_2[0], v / d + REF_UV_D65_2[1]


EPSILON = (6 / 29) ** 3
KAPPA = (29 / 3) ** 3


REF_XYZ_D65_2 = 0.95047, 1.00000, 1.08883
REF_UV_D65_2 = _xyz_to_uv(*REF_XYZ_D65_2)
