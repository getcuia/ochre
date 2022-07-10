"""Objects representing colors in different color spaces."""


import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Iterator, Text, TypeVar, Union

from . import ansi256, colorsys, web

C = TypeVar("C", bound="Color")


class Color(ABC, Iterable[float]):
    """Abstract base class for color spaces."""

    @property
    @abstractmethod
    def rgb(self) -> "RGB":
        """Return the color as an RGB object."""
        raise NotImplementedError()

    @property
    def hex(self) -> "Hex":
        """Return the color as an Hex object."""
        return self.rgb.hex

    @property
    def web_color(self) -> "WebColor":
        """Return the color as a WebColor object."""
        return self.rgb.web_color

    @property
    def ansi256(self) -> "Ansi256":
        """Return the color as an Ansi256 object."""
        return self.rgb.ansi256

    @property
    def hcl(self) -> "HCL":
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

    def distance(self, other: "Color") -> float:
        """Return the distance between colors in the HCL color space."""
        self_hcl = self.hcl
        other_hcl = other.hcl

        # Hue wraps around at 360°, so we need to take the shortest distance.
        hue_diff = abs(self_hcl.hue - other_hcl.hue)
        hue_diff = min(hue_diff, 2 * math.pi - hue_diff)

        return math.hypot(
            hue_diff,
            self_hcl.chroma - other_hcl.chroma,
            self_hcl.luminance - other_hcl.luminance,
        )

    def closest(self, colors: Iterable[C]) -> C:
        """Find the color in the given list that is closest to this color."""
        return min(colors, key=self.distance)

    def with_chroma(self, chroma: float) -> "HCL":
        """Return a copy of the color with the given chroma."""
        self = self.hcl
        return HCL(self.hue, chroma, self.luminance)

    def with_luminance(self, luminance: float) -> "HCL":
        """Return a copy of the color with the given luminance."""
        self = self.hcl
        return HCL(self.hue, self.chroma, luminance)

    def darken(self, amount: float = 1.0) -> "HCL":
        """Return a color that is darker than this color."""
        self = self.hcl
        return self.with_luminance(self.luminance - amount * self.K_L)

    def saturate(self, amount: float = 1.0) -> "HCL":
        """Return a color that is more saturated than this color."""
        self = self.hcl
        return self.with_chroma(self.chroma + amount * self.K_C)

    @property
    def relative_luminance(self) -> float:
        """Return the relative luminance of the color as defined in WCAG 2.1."""

        def f(v):
            if v <= 0.03928:
                return v / 12.92
            return math.pow((v + 0.055) / 1.055, 2.4)

        self = self.rgb
        return 0.2126 * f(self.red) + 0.7152 * f(self.green) + 0.0722 * f(self.blue)


@dataclass(frozen=True, eq=False)
class RGB(Color):
    """
    An RGB color.

    Values are in the range `[0, 1]` and they are clamped to that range.
    """

    red: float
    green: float
    blue: float

    N_DIGITS = 2

    def __post_init__(self) -> None:
        """Clamp and round RGB channels."""
        object.__setattr__(self, "red", round(clip(self.red, 0, 1), self.N_DIGITS))
        object.__setattr__(self, "green", round(clip(self.green, 0, 1), self.N_DIGITS))
        object.__setattr__(self, "blue", round(clip(self.blue, 0, 1), self.N_DIGITS))

    @property
    def rgb(self) -> "RGB":
        """Return the color as an RGB object."""
        return self

    @property
    def hex(self) -> "Hex":
        """Return the color as an Hex object."""
        return Hex(colorsys.rgb_to_hex(self.red, self.green, self.blue))

    @property
    def web_color(self) -> "WebColor":
        """Return the color as a WebColor object."""
        return self.closest(map(WebColor, web.colors.keys()))

    @property
    def ansi256(self) -> "Ansi256":
        """Return the color as an Ansi256 object."""
        return self.closest(map(Ansi256, range(len(ansi256.colors))))

    @property
    def hcl(self) -> "HCL":
        """Return the color as an HCL object."""
        return HCL(*colorsys.rgb_to_hcl(self.red, self.green, self.blue))


@dataclass(frozen=True, eq=False)
class Hex(Color):
    """A color represented by a hexadecimal integer."""

    hex_code: Union[int, Text]

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
    def hex(self) -> "Hex":
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
    def web_color(self) -> "WebColor":
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
    def ansi256(self) -> "Ansi256":
        """Return the color as an Ansi256 object."""
        return self


@dataclass(frozen=True, eq=False)
class HCL(Color):
    """An HCL color."""

    hue: float
    chroma: float
    luminance: float

    # Proportionality constants for variations in luminance and chroma.
    K_L = 0.1801
    K_C = 0.0981

    @property
    def rgb(self) -> RGB:
        """Return the color as an RGB object."""
        return RGB(*colorsys.hcl_to_rgb(self.hue, self.chroma, self.luminance))

    @property
    def hcl(self) -> "HCL":
        """Return the color as an HCL object."""
        return self


def clip(value: float, min_value: float, max_value: float) -> float:
    """Clip a value to the given range."""
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value
