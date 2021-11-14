"""Objects representing colors in different color spaces."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Color(ABC):
    """Abstract base class for color spaces."""

    @property
    @abstractmethod
    def _rgb(self) -> RGB:
        """Return the color as an RGB object."""
        raise NotImplementedError()

    def __index__(self) -> int:
        """Return the index of the color as an hexadecimal integer."""
        rgb = self._rgb
        return int(255 * (0x10000 * rgb.red + 0x100 * rgb.green + rgb.blue))


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

    @property
    def _rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self


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
