"""Generic tests."""

import math

from ochre import WebColor, __version__


def test_version():
    """Test version."""
    assert __version__ == "0.3.0"


def test_colors_are_iterable():
    """Test colors are iterable."""
    color = WebColor("cornflower blue")

    assert all(isinstance(c, float) for c in color)

    assert (
        math.sqrt(sum(map(lambda c, cr: (255 * c - cr) ** 2, color, (100, 149, 237))))
        < 1.25
    )
