"""Facilities for working with colors."""


__version__ = "0.1.0"


__all__ = ["Ansi256", "Color", "HCL", "Hex", "RGB", "WebColor"]


import math

from .spaces import HCL, RGB, Ansi256, Color, Hex, WebColor


def dist(a: Color, b: Color) -> float:
    """Compute the distance between two colors in the HCL color space."""
    a, b = a.hcl, b.hcl
    return math.hypot(a.hue - b.hue, a.chroma - b.chroma, a.luminance - b.luminance)
