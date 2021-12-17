"""Objects representing colors in different color spaces."""

from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Iterator, Text, TypeVar

from . import ansi256, colorsys, web

C = TypeVar("C", bound="Color")


class Color(ABC, Iterable[float]):
    """Abstract base class for color spaces."""

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
        return hex(self) == hex(other)

    def __hash__(self) -> int:
        """Return the hash of the color."""
        return hash(hex(self))

    def __iter__(self) -> Iterator[float]:
        """Return an iterator over the color's RGB channels."""
        self_rgb = self.rgb
        yield self_rgb.red
        yield self_rgb.green
        yield self_rgb.blue

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


@dataclass(frozen=True, eq=False)
class RGB(Color):
    """An RGB color."""

    red: float
    green: float
    blue: float

    def __post_init__(self) -> None:
        """Round the RGB channels."""
        object.__setattr__(self, "red", round(self.red, 2))
        object.__setattr__(self, "green", round(self.green, 2))
        object.__setattr__(self, "blue", round(self.blue, 2))

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


@dataclass(frozen=True, eq=False)
class Hex(Color):
    """A color represented by a hexadecimal integer."""

    hex_code: int | Text

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


@dataclass(frozen=True, eq=False)
class WebColor(Color):
    """A color represented by a name."""

    name: Text

    NORM_PATTERN = re.compile(r"[\s\-_]+")

    def __post_init__(self) -> None:
        """Normalize the name of the color."""
        norm_name = self.NORM_PATTERN.sub("", self.name).lower()
        if norm_name not in web.colors:
            raise ValueError(f"{norm_name!r} ({self.name!r}) is not a valid color name")
        object.__setattr__(self, "name", norm_name)

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


@dataclass(frozen=True, eq=False)
class Ansi256(Color):
    """A color represented by an integer between 0 and 255."""

    code: int

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


@dataclass(frozen=True, eq=False)
class HCL(Color):
    """An HCL color."""

    hue: float
    chroma: float
    luminance: float

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> HCL:
        """Return the color as an HCL object."""
        return self
