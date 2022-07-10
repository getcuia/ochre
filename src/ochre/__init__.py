"""Facilities for working with colors."""


__version__ = "0.5.0"


__all__ = ["Ansi256", "Color", "ColorPair", "HCL", "Hex", "RGB", "WebColor"]


from .color_pair import ColorPair
from .spaces import HCL, RGB, Ansi256, Color, Hex, WebColor
