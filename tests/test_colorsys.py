"""Tests for the extras in `melanin.colorsys`."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from melanin import colorsys

between_0_and_1 = st.floats(min_value=0, max_value=1)


@given(r=between_0_and_1, g=between_0_and_1, b=between_0_and_1)
def test_rgb_to_xyz_roundtrip(r: float, g: float, b: float) -> None:
    """Test that rgb_to_xyz and xyz_to_rgb are inverses."""
    x, y, z = colorsys.rgb_to_xyz(r, g, b)
    r2, g2, b2 = colorsys.xyz_to_rgb(x, y, z)
    assert (r2, g2, b2) == pytest.approx((r, g, b), rel=3e-10, abs=7e-7)
