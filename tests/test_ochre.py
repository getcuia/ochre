"""Generic tests."""

from ochre import WebColor, __version__


def test_version():
    """Test version."""
    assert __version__ == "0.1.1"


def test_colors_are_iterable():
    """Test colors are iterable."""
    color = WebColor("cornflower blue")

    assert all(isinstance(c, float) for c in color)

    assert tuple(map(lambda c: int(255 * c), color)) == (100, 149, 237)
