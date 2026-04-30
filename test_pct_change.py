import math
import pytest
from decimal import Decimal
from fractions import Fraction

from pct_change import pct_change


# ── Happy-path / normal behaviour ─────────────────────────────────────────────

class TestNormalCases:
    def test_positive_increase(self):
        assert pct_change(110, 100) == pytest.approx(0.10)

    def test_positive_decrease(self):
        assert pct_change(90, 100) == pytest.approx(-0.10)

    def test_no_change(self):
        assert pct_change(100, 100) == 0.0

    def test_double(self):
        assert pct_change(200, 100) == pytest.approx(1.0)

    def test_negative_to_negative(self):
        assert pct_change(-50, -100) == pytest.approx(-0.50)

    def test_negative_prior_positive_curr(self):
        assert pct_change(50, -100) == pytest.approx(-1.50)

    def test_positive_prior_negative_curr(self):
        assert pct_change(-50, 100) == pytest.approx(-1.50)

    def test_fractional_values(self):
        assert pct_change(0.15, 0.10) == pytest.approx(0.50)

    def test_very_small_floats(self):
        result = pct_change(1e-300, 1e-300)
        assert result == pytest.approx(0.0)

    def test_very_large_floats(self):
        result = pct_change(1e308, 5e307)
        assert result == pytest.approx(1.0)


# ── Compatible numeric types ──────────────────────────────────────────────────

class TestNumericTypes:
    def test_int_inputs(self):
        assert pct_change(3, 2) == pytest.approx(0.5)

    def test_mixed_int_float(self):
        assert pct_change(1.5, 1) == pytest.approx(0.5)

    def test_bool_accepted_as_int_subclass(self):
        # bool is a subclass of int in Python
        assert pct_change(True, True) == 0.0

    def test_decimal_inputs(self):
        result = pct_change(Decimal("1.1"), Decimal("1.0"))
        assert float(result) == pytest.approx(0.1)

    def test_fraction_inputs(self):
        result = pct_change(Fraction(3, 2), Fraction(1, 1))
        assert float(result) == pytest.approx(0.5)


# ── Zero as prior (ZeroDivisionError) ────────────────────────────────────────

class TestZeroPrior:
    def test_zero_prior_nonzero_curr_raises(self):
        with pytest.raises(ZeroDivisionError):
            pct_change(100, 0)

    def test_zero_prior_negative_curr_raises(self):
        with pytest.raises(ZeroDivisionError):
            pct_change(-1, 0)

    def test_zero_prior_small_curr_raises(self):
        with pytest.raises(ZeroDivisionError):
            pct_change(1e-300, 0)

    def test_both_zero_returns_zero(self):
        assert pct_change(0, 0) == 0.0

    def test_zero_curr_nonzero_prior(self):
        assert pct_change(0, 100) == pytest.approx(-1.0)


# ── NaN inputs ────────────────────────────────────────────────────────────────

class TestNaN:
    def test_nan_curr(self):
        with pytest.raises(ValueError, match="curr must not be NaN"):
            pct_change(float("nan"), 1)

    def test_nan_prior(self):
        with pytest.raises(ValueError, match="prior must not be NaN"):
            pct_change(1, float("nan"))

    def test_both_nan(self):
        with pytest.raises(ValueError):
            pct_change(float("nan"), float("nan"))


# ── Infinity inputs ──────────────────────────────────────────────────────────

class TestInfinity:
    def test_inf_curr(self):
        with pytest.raises(ValueError, match="curr must be finite"):
            pct_change(float("inf"), 1)

    def test_neg_inf_curr(self):
        with pytest.raises(ValueError, match="curr must be finite"):
            pct_change(float("-inf"), 1)

    def test_inf_prior(self):
        with pytest.raises(ValueError, match="prior must be finite"):
            pct_change(1, float("inf"))

    def test_both_inf(self):
        with pytest.raises(ValueError):
            pct_change(float("inf"), float("inf"))


# ── Wrong types (TypeError) ──────────────────────────────────────────────────

class TestBadTypes:
    def test_string_curr(self):
        with pytest.raises(TypeError, match="curr must be a real number"):
            pct_change("100", 50)

    def test_string_prior(self):
        with pytest.raises(TypeError, match="prior must be a real number"):
            pct_change(100, "50")

    def test_none_curr(self):
        with pytest.raises(TypeError):
            pct_change(None, 1)

    def test_none_prior(self):
        with pytest.raises(TypeError):
            pct_change(1, None)

    def test_complex_curr(self):
        with pytest.raises(TypeError, match="curr must be a real number"):
            pct_change(1 + 2j, 1)

    def test_complex_prior(self):
        with pytest.raises(TypeError, match="prior must be a real number"):
            pct_change(1, 1 + 2j)

    def test_list_input(self):
        with pytest.raises(TypeError):
            pct_change([100], 50)

    def test_dict_input(self):
        with pytest.raises(TypeError):
            pct_change(100, {"v": 50})

    def test_no_arguments(self):
        with pytest.raises(TypeError):
            pct_change()

    def test_one_argument(self):
        with pytest.raises(TypeError):
            pct_change(100)


# ── Floating-point edge cases ────────────────────────────────────────────────

class TestFloatingPointEdges:
    def test_subnormal_prior(self):
        """Subnormal (denormalized) float as prior should not crash."""
        tiny = 5e-324  # smallest positive subnormal
        result = pct_change(tiny * 2, tiny)
        assert result == pytest.approx(1.0)

    def test_negative_zero_prior(self):
        """−0.0 == 0.0 in Python, so this should trigger the zero-prior path."""
        assert pct_change(0.0, -0.0) == 0.0

    def test_negative_zero_curr(self):
        # -0.0 as curr: (-0.0 - 1.0) / 1.0 == -1.0
        assert pct_change(-0.0, 1.0) == pytest.approx(-1.0)

    def test_result_sign_negative_prior(self):
        result = pct_change(-80, -100)
        assert result == pytest.approx(-0.20)
        assert result < 0  # price improved (less negative), but fraction is negative

    def test_large_magnitude_difference(self):
        """curr ≫ prior — no overflow when result is representable."""
        result = pct_change(1e200, 1)
        assert result == pytest.approx(1e200)

    def test_overflow_raises(self):
        """When the ratio itself overflows IEEE 754 double, raise OverflowError."""
        with pytest.raises(OverflowError):
            pct_change(1e308, 1e-308)
