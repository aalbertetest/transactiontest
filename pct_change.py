import math
from decimal import Decimal
from numbers import Real


def _is_real_number(val):
    return isinstance(val, (Real, Decimal))


def pct_change(curr, prior):
    """Return the fractional change from *prior* to *curr*.

    Raises
    ------
    TypeError
        If either argument is not a real number (str, None, complex, …).
    ValueError
        If either argument is NaN or infinite.
    ZeroDivisionError
        If *prior* is zero and *curr* is nonzero.
    OverflowError
        If the result overflows to infinity.
    """
    for name, val in (("curr", curr), ("prior", prior)):
        if not _is_real_number(val):
            raise TypeError(
                f"{name} must be a real number, got {type(val).__name__}"
            )
        if math.isnan(val):
            raise ValueError(f"{name} must not be NaN")
        if math.isinf(val):
            raise ValueError(f"{name} must be finite")

    if prior == 0:
        if curr == 0:
            return 0.0
        raise ZeroDivisionError(
            "prior must not be zero when curr is nonzero"
        )

    result = (curr - prior) / prior

    if isinstance(result, float) and math.isinf(result):
        raise OverflowError("result overflows to infinity")

    return result
