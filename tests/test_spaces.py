"""Test suite for RGB and HCL color spaces."""

from melanin import RGB


def test_hex():
    """Test conversion to hexadecimal."""
    assert hex(RGB(0, 0, 0)) == "0x0"
    assert hex(RGB(0, 0, 1)) == "0xff"
    assert hex(RGB(0, 1, 0)) == "0xff00"
    assert hex(RGB(1, 0, 0)) == "0xff0000"
    assert hex(RGB(1, 1, 1)) == "0xffffff"
