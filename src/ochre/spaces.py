"""Objects representing colors in different color spaces."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Iterable, Text, TypeVar

from . import ansi256, colorsys, web

C = TypeVar("C", bound="Color")


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
        return colorsys.hex_to_hex(self.hex.hex_code)

    def __eq__(self, other: object) -> bool:
        """Return True if the colors are almost equal in RGB space."""
        if not isinstance(other, Color):
            raise TypeError(f"{other!r} is not a Color")
        self_rgb = self.rgb
        other_rgb = other.rgb
        return (
            math.hypot(
                self_rgb.red - other_rgb.red,
                self_rgb.green - other_rgb.green,
                self_rgb.blue - other_rgb.blue,
            )
            < self.EQUALITY_THRESHOLD
        )

    def distance(self, other: Color) -> float:
        """Return the distance between colors in the HCL color space."""
        self_hcl = self.hcl
        other_hcl = other.hcl
        return math.hypot(
            self_hcl.hue - other_hcl.hue,
            self_hcl.chroma - other_hcl.chroma,
            self_hcl.luminance - other_hcl.luminance,
        )

    def closest(self, colors: Iterable[C]) -> C:
        """Find the color in the given list that is closest to this color."""
        return min(colors, key=self.distance)


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
        return f"RGB(red={self.red!r}, green={self.green!r}, blue={self.blue!r})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return Hex(colorsys.rgb_to_hex(self.red, self.green, self.blue))

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self.closest(map(WebColor, web.colors.keys()))

    @property
    def ansi256(self) -> Ansi256:
        """Return the color as an Ansi256 object."""
        return self.closest(map(Ansi256, range(len(ansi256.colors))))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return HCL(*colorsys.rgb_to_hcl(self.red, self.green, self.blue))


class Hex(Color):
    """A color represented by a hexadecimal integer."""

    hex_code: int | Text

    def __init__(self, hex_code: int | Text) -> None:
        """Initialize a hexadecimal color."""
        self.hex_code = hex_code

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        if isinstance(self.hex_code, int):
            return f"Hex({self.hex_code:X})"
        return f"Hex({self.hex_code!r})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hex_to_rgb(self.hex_code))

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return self


class WebColor(Color):
    """A color represented by a name."""

    name: Text

    def __init__(self, name: Text) -> None:
        """Initialize a color by name."""
        if name not in web.colors:
            raise ValueError(f"{name!r} is not a valid color name")
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
        return Hex(colorsys.web_color_to_hex(self.name))

    @property
    def web_color(self) -> WebColor:
        """Return the color as a WebColor object."""
        return self


class Ansi256(Color):
    """A color represented by an integer between 0 and 255."""

    code: int

    def __init__(self, code: int) -> None:
        """Initialize an ANSI color."""
        self.code = code

    def __repr__(self) -> Text:
        """Return a string representation of the color."""
        return f"Ansi256({self.code!r})"

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return self.hex.rgb

    @property
    def hex(self) -> Hex:
        """Return the color as an Hex object."""
        return Hex(colorsys.ansi256_to_hex(self.code))

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
        return (
            f"HCL(hue={self.hue!r}, "
            "chroma={self.chroma!r}, "
            "luminance={self.luminance!r})"
        )

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self
