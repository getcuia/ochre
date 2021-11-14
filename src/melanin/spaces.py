"""Objects representing colors in different color spaces."""

from __future__ import annotations


class Color:
    """A generic color."""


class RGB(Color):
    """An RGB color."""

    red: float
    green: float
    blue: float

    def __init__(self, red: float, green: float, blue: float) -> None:
        """Initialize an RGB color."""
        self.red = red
        self.green = green
        self.blue = blue


class HCL(Color):
    """An HCL color."""

    hue: float
    chroma: float
    luminance: float

    def __init__(self, hue: float, chroma: float, luminance: float) -> None:
        """Initialize an HCL color."""
        self.hue = hue
        self.chroma = chroma
        self.luminance = luminance
