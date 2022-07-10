"""A color pair of foreground and background colors."""


from dataclasses import dataclass
from typing import Optional

from .spaces import Color


@dataclass(frozen=True)
class ColorPair:
    """A color pair of foreground and background colors."""

    foreground: Optional[Color] = None
    background: Optional[Color] = None

    @property
    def contrast_ratio(self) -> float:
        """Return the contrast ratio of the color pair as defined in WCAG 2.1."""
        if self.foreground is None or self.background is None:
            raise ValueError(
                "Color pair must have both foreground and background colors set."
            )

        l1 = self.foreground.relative_luminance
        l2 = self.background.relative_luminance

        if l1 < l2:
            l1, l2 = l2, l1

        return (l1 + 0.05) / (l2 + 0.05)
