"""Facilities for working with colors."""


__version__ = "0.1.0"


__all__ = ["HCL", "Hex", "RGB", "WebColor", "Color", "Ansi256"]


from .spaces import HCL, RGB, Ansi256, Color, Hex, WebColor
