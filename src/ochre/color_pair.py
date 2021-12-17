"""A color pair of foreground and background colors."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .spaces import Color


@dataclass(frozen=True)
class ColorPair:
    """A color pair of foreground and background colors."""

    foreground: Optional[Color] = None
    background: Optional[Color] = None
