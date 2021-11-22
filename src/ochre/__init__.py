"""Facilities for working with colors."""


__version__ = "0.1.1"


__all__ = ["Ansi256", "Color", "HCL", "Hex", "RGB", "WebColor"]


from .spaces import HCL, RGB, Ansi256, Color, Hex, WebColor
