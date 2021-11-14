import pytest

from melanin import Color, __version__


def test_version():
    assert __version__ == "0.1.0"


def test_color():
    color = Color.frombytes(127.5, 127.5, 127.5)

    assert color.red == 0.5
    assert color.green == 0.5
    assert color.blue == 0.5

    assert color.lightness == pytest.approx(0.533889647411143)
    assert color.chroma == pytest.approx(0.000069760072978905, abs=3e-5)
    assert color.hue == 4.76440374867805
