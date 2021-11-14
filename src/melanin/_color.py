"""An object representing a color."""

from __future__ import annotations

from typing import NamedTuple


class Color(NamedTuple):
    """
    An RGB color.

    Each channel is represented by a float between zero and one.

    Examples
    --------
    >>> Color(0.5, 0.5, 0.5)
    Color(red=0.5, green=0.5, blue=0.5)
    """

    red: float
    """Amount of red in the color."""
    green: float
    """Amount of green in the color."""
    blue: float
    """Amount of blue in the color."""

    @staticmethod
    def frombytes(red: int, green: int, blue: int) -> Color:
        """
        Create a color from bytes.

        The input values are expected to be between 0 and 255.

        Examples
        --------
        >>> Color.frombytes(0, 255, 255)
        Color(red=0.0, green=1.0, blue=1.0)
        """
        return Color(clamp(red / 255), clamp(green / 255), clamp(blue / 255))

    def tobytes(self) -> tuple[int, int, int]:
        """
        Return the bytes for this color.

        The output values are between 0 and 255.

        Examples
        --------
        >>> Color(red=0.0, green=1.0, blue=1.0).tobytes()
        (0, 255, 255)
        >>> Color.frombytes(10, 20, 30).tobytes() == (10, 20, 30)
        True
        """
        return (int(255 * self.red), int(255 * self.green), int(255 * self.blue))

    @property
    def lightness(self) -> float:
        r"""
        Return the lightness of this color as per the CIE L\*u\*v\*/LCh color spaces.

        The lightness is a value between zero and one.

        Examples
        --------
        >>> Color(0, 0, 0).lightness
        0.0
        >>> Color.frombytes(23, 23, 23).lightness  # doctest: +NUMBER
        0.077396
        >>> c = Color.frombytes(0, 255, 0)
        >>> c.lightness  # doctest: +NUMBER
        0.877370
        """
        return self.toluv()[0]

    @property
    def chroma(self) -> float:
        """
        Return the chroma of this color as per the CIE LCh color space.

        The chroma is a value between zero and one.

        Examples
        --------
        >>> Color(0, 0, 0).chroma
        0.0
        >>> Color.frombytes(30, 60, 90).chroma  # doctest: +NUMBER
        0.2799813
        >>> Color.frombytes(255, 255, 255).chroma  # doctest: +NUMBER
        0.000171
        """
        return self.tolch()[1]

    @property
    def hue(self) -> float:
        """
        Return the hue of this color as per the CIE LCh color space.

        The hue is a value between 0 and 2π.

        Examples
        --------
        >>> Color(0, 0, 0).hue  # doctest: +NUMBER
        3.141593
        >>> Color.frombytes(30, 60, 90).hue  # doctest: +NUMBER
        4.296177
        >>> Color.frombytes(0, 255, 0).hue  # doctest: +NUMBER
        2.229197
        """
        return self.tolch()[2]

    def with_lightness(self, ell: float) -> Color:
        """
        Create a new color with the same chroma and hue but a new lightness.

        The lightness is a value between zero and one.

        Examples
        --------
        >>> Color.frombytes(0, 255, 0).with_lightness(0.5)  # doctest: +NUMBER
        Color(red=0.0, green=0.582453, blue=0.0)
        """
        _, u, v = self.toluv()
        return self.fromluv(ell, u, v)

    def with_chroma(self, c: float) -> Color:
        """
        Create a new color with the same hue and lightness but a new chroma.

        The chroma is a value between zero and one.

        Examples
        --------
        >>> Color.frombytes(0, 255, 0).with_chroma(0.5)  # doctest: +NUMBER
        Color(red=0.680477, green=0.922408, blue=0.680426)
        """
        ell, _, h = self.tolch()
        return self.fromlch(ell, c, h)

    def with_hue(self, h: float) -> Color:
        """
        Create a new color with the same chroma and lightness but a new hue.

        The hue is a value between 0 and 2π.

        Examples
        --------
        >>> Color.frombytes(0, 255, 0).with_hue(1.5)  # doctest: +NUMBER
        Color(red=0.900022, green=0.900897, blue=0.0)
        """
        ell, c, _ = self.tolch()
        return self.fromlch(ell, c, h)

    def islight(self) -> bool:
        """
        Return True if this color is light.

        A color is considered light if its lightness is greater than 0.5.

        Examples
        --------
        >>> Color(0, 0, 0).islight()
        False
        >>> Color(1, 1, 1).islight()
        True
        """
        return self.lightness > 0.5

    def isdark(self) -> bool:
        """
        Return True if this color is dark.

        A color is considered dark if it is not light.

        Examples
        --------
        >>> Color(0, 0, 0).isdark()
        True
        >>> Color(1, 1, 1).isdark()
        False
        """
        return not self.islight()
