"""Stuff that doesn't fit anywhere else."""


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """
    Clamp a value to a range.

    Examples
    --------
    >>> clamp(-0.5)
    0.0
    >>> clamp(0.5)
    0.5
    >>> clamp(1.5)
    1.0
    """
    return max(min_value, min(value, max_value))
