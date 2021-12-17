"""A color pair of foreground and background colors."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .spaces import Color


@dataclass
class ColorPair:
    """A color pair of foreground and background colors."""

    foreground: Optional[Color] = None
    background: Optional[Color] = None


# TODO: maybe this should become hashes in color and color pair?
def encode(
    value: Optional[Color | ColorPair],
) -> Optional[Text | tuple[Optional[Text], Optional[Text]]]:
    """Encode a color or color pair into optional strings to use as dictionary key."""
    if value is None:
        return None

    if isinstance(value, Color):
        return hex(value)

    if isinstance(value, ColorPair):
        return (
            hex(value.foreground) if value.foreground else None,
            hex(value.background) if value.background else None,
        )

    raise TypeError(f"Unsupported type: {type(value)}")
