"""Objects representing colors in different color spaces."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Text, TypeVar

from . import colorsys, web


class Color(ABC):
    """Abstract base class for color spaces."""

    EQUALITY_THRESHOLD = 7e-3

    @abstractmethod
    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        raise NotImplementedError()

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self.rgb.hex

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self.rgb.web_color

    @property
    def ansi256(self) -> Ansi256:
        """Return the color as an Ansi256 object."""
        return self.rgb.ansi256

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self.rgb.hcl

    def __index__(self) -> int:
        """Return the index of the color as an hexadecimal integer."""
        return self.hex.integer

    def __eq__(self, other) -> bool:
        """Return True if the colors are equal."""
        return _dist_rgb(self.rgb, other.rgb) < self.EQUALITY_THRESHOLD


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

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"RGB({self.red}, {self.green}, {self.blue})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self

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
        return _closest_color_rgb(self, map(WebColor, web.colors.keys()))

    @property
    def ansi256(self) -> Ansi256:
        """Return the color as an Ansi256 object."""
        return _closest_color_rgb(self, map(Ansi256, range(256)))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return HCL(*colorsys.rgb_to_hcl(self.red, self.green, self.blue))


class Hex(Color):
    """A color represented by a hexadecimal integer."""

    integer: int

    def __init__(self, value: int | Text) -> None:
        """Initialize a hexadecimal color."""
        if isinstance(value, Text):
            value = int(value.lstrip("#"), 16)
        self.integer = value

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"Hex({self.integer:X})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        r = (self.integer >> 16) & 0xFF
        g = (self.integer >> 8) & 0xFF
        b = self.integer & 0xFF
        return RGB(r / 255, g / 255, b / 255)

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self


class WebColor(Color):
    """A color represented by a name."""

    name: Text

    def __init__(self, name: Text) -> None:
        """Initialize a color by name."""
        self.name = name

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"WebColor({self.name!r})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self.hex.rgb

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return Hex(web.colors[self.name])

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self.hex.hcl


class Ansi256(Color):
    """A color represented by an integer between 0 and 255."""

    code: int

    ANSI8 = [
        WebColor("black"),  # 0
        WebColor("maroon"),  # 1
        WebColor("green"),  # 2
        WebColor("olive"),  # 3
        WebColor("navy"),  # 4
        WebColor("purple"),  # 5
        WebColor("teal"),  # 6
        WebColor("silver"),  # 7
        WebColor("grey"),  # 8
        WebColor("red"),  # 9
        WebColor("lime"),  # 10
        WebColor("yellow"),  # 11
        WebColor("blue"),  # 12
        WebColor("fuchsia"),  # 13
        WebColor("aqua"),  # 14
        WebColor("white"),  # 15
    ]

    def __init__(self, code: int) -> None:
        """Initialize an ANSI color."""
        self.code = code

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"Ansi256({self.code})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        if self.code < 16:
            return self.ANSI8[self.code].rgb
        if self.code < 232:
            red_i = (self.code - 16) // 36
            green_i = ((self.code - 16) % 36) // 6
            blue_i = (self.code - 16) % 6

            red = 55 + red_i * 40 if red_i > 0 else 0
            green = 55 + green_i * 40 if green_i > 0 else 0
            blue = 55 + blue_i * 40 if blue_i > 0 else 0

            return RGB(red / 255, green / 255, blue / 255)
        if self.code < 256:
            value = (self.code - 232) * 10 + 8
            return RGB(value / 255, value / 255, value / 255)
        raise ValueError(f"Invalid ANSI code {self.code}")

    @property
    def ansi256(self) -> Ansi256:
        """Return the color as an Ansi256 object."""
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

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"HCL({self.hue}, {self.chroma}, {self.luminance})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self


def _dist_rgb(color1: RGB, color2: RGB) -> float:
    """Return the distance between two RGB colors."""
    return math.sqrt(
        (color1.red - color2.red) ** 2
        + (color1.green - color2.green) ** 2
        + (color1.blue - color2.blue) ** 2
    )


C = TypeVar("C", bound=Color)


def _closest_color_rgb(color: RGB, colors: Iterable[C]) -> C:
    """Return the closest color to the given color."""
    minimal_color: Optional[C] = None
    minimal_distance = math.inf

    for other in colors:
        distance = _dist_rgb(color, other.rgb)
        if distance < minimal_distance:
            minimal_color = other
            minimal_distance = distance

    assert minimal_color is not None
    return minimal_color

    # return min(colors, key=lambda c: _dist_rgb(color, c))
