"""Objects representing colors in different color spaces."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Optional, Text

from . import colorsys, web


class Color(ABC):
    """Abstract base class for color spaces."""

    @property
    @abstractmethod
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
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

    @abstractmethod
    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        raise NotImplementedError()

    def __index__(self) -> int:
        """Return the index of the color as an hexadecimal integer."""
        return self.hex.integer

    def __eq__(self, other: Color) -> bool:
        """Return True if the colors are equal."""
        return _dist_rgb(self, other) < 7e-3


class Hex(Color):
    """A color represented by a hexadecimal integer."""

    integer: int

    def __init__(self, value: int | Text) -> None:
        """Initialize a hexadecimal color."""
        if isinstance(value, Text):
            value = int(value.lstrip("#"), 16)
        self.integer = value

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self.rgb.web_color

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        r = (self.integer >> 16) & 0xFF
        g = (self.integer >> 8) & 0xFF
        b = self.integer & 0xFF
        return RGB(r / 255, g / 255, b / 255)

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self.rgb.hcl

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"Hex({self.integer:X})"


class WebColor(Color):
    """A color represented by a name."""

    name: Text

    def __init__(self, name: Text) -> None:
        """Initialize a color by name."""
        self.name = name

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return Hex(web.colors[self.name])

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self.hex.rgb

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self.hex.hcl

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"WebColor({self.name!r})"


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
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        minimal_name: Optional[Text] = None
        minimal_distance = math.inf

        for name, hexstr in web.colors.items():
            distance = _dist_rgb(self, Hex(hexstr))
            if distance < minimal_distance:
                minimal_name = name
                minimal_distance = distance
        assert minimal_name is not None
        return WebColor(minimal_name)

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return HCL(*colorsys.rgb_to_hcl(self.red, self.green, self.blue))

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"RGB({self.red}, {self.green}, {self.blue})"


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
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self.rgb.web_color

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"HCL({self.hue}, {self.chroma}, {self.luminance})"


def _dist_rgb(color1: Color, color2: Color) -> float:
    """Return the distance between two RGB colors."""
    rgb1 = color1.rgb
    rgb2 = color2.rgb
    return math.sqrt(
        (rgb1.red - rgb2.red) ** 2
        + (rgb1.green - rgb2.green) ** 2
        + (rgb1.blue - rgb2.blue) ** 2
    )
