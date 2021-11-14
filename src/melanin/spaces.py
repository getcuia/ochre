"""Objects representing colors in different color spaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Text

from . import colorsys


class Color(ABC):
    """Abstract base class for color spaces."""

    @property
    @abstractmethod
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        raise NotImplementedError()

    def __index__(self) -> int:
        """Return the index of the color as an hexadecimal integer."""
        return self.hex.value


class Hex(Color):
    """A color represented by a hexadecimal integer."""

    value: int

    def __init__(self, value: int | Text) -> None:
        """Initialize a hexadecimal color."""
        if isinstance(value, Text):
            value = int(value.lstrip("#"), 16)
        self.value = value

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        r = (self.value >> 16) & 0xFF
        g = (self.value >> 8) & 0xFF
        b = self.value & 0xFF
        return RGB(r / 255, g / 255, b / 255)

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self.rgb.hcl


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
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        r = int(self.red * 255)
        g = int(self.green * 255)
        b = int(self.blue * 255)
        return Hex((r << 16) + (g << 8) + b)

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return HCL(*colorsys.rgb_to_hcl(self.red, self.green, self.blue))


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

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self.rgb.hex

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self
