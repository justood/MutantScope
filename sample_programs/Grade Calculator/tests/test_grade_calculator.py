"""
Test Suite — Case Study 1: Grade & Discount Calculator
=======================================================
Designed to demonstrate the gap between code coverage and mutation score.

Run with pytest:
    pytest test_grade_discount_calculator.py -v --tb=short

For mutation testing (requires mutmut):
    mutmut run --paths-to-mutate grade_discount_calculator.py
    mutmut results
"""

import pytest
from grade_calculator import (
    calculate_letter_grade,
    calculate_gpa,
    calculate_weighted_average,
    is_passing,
    calculate_grade_points,
    calculate_cumulative_gpa,
)


# ═══════════════════════════════════════════════════════════════════
# SECTION A — calculate_letter_grade
# ═══════════════════════════════════════════════════════════════════

class TestCalculateLetterGrade:
    """Tests for the letter-grade conversion function."""

    # ── happy-path centre-of-tier scores ──────────────────────────
    def test_score_95_is_A(self):
        assert calculate_letter_grade(95) == "A"

    def test_score_85_is_B(self):
        assert calculate_letter_grade(85) == "B"

    def test_score_75_is_C(self):
        assert calculate_letter_grade(75) == "C"

    def test_score_65_is_D(self):
        assert calculate_letter_grade(65) == "D"

    def test_score_50_is_F(self):
        assert calculate_letter_grade(50) == "F"

    def test_score_0_is_F(self):
        assert calculate_letter_grade(0) == "F"

    def test_score_100_is_A(self):
        assert calculate_letter_grade(100) == "A"

    # ── exact boundary scores (mutation-critical) ──────────────────
    def test_boundary_90_is_A(self):
        """Exact A boundary — mutation >= vs > kills this."""
        assert calculate_letter_grade(90) == "A"

    def test_boundary_89_is_B(self):
        """One below A boundary — must be B, not A."""
        assert calculate_letter_grade(89) == "B"

    def test_boundary_80_is_B(self):
        assert calculate_letter_grade(80) == "B"

    def test_boundary_79_is_C(self):
        assert calculate_letter_grade(79) == "C"

    def test_boundary_70_is_C(self):
        assert calculate_letter_grade(70) == "C"

    def test_boundary_69_is_D(self):
        assert calculate_letter_grade(69) == "D"

    def test_boundary_60_is_D(self):
        assert calculate_letter_grade(60) == "D"

    def test_boundary_59_is_F(self):
        assert calculate_letter_grade(59) == "F"

    # ── invalid inputs ─────────────────────────────────────────────
    def test_negative_score_raises(self):
        with pytest.raises(ValueError):
            calculate_letter_grade(-1)

    def test_score_above_100_raises(self):
        with pytest.raises(ValueError):
            calculate_letter_grade(101)

    def test_score_minus_0_point_1_raises(self):
        with pytest.raises(ValueError):
            calculate_letter_grade(-0.1)

    # ── floating-point scores ──────────────────────────────────────
    def test_score_89_point_9_is_B(self):
        assert calculate_letter_grade(89.9) == "B"

    def test_score_90_point_0_is_A(self):
        assert calculate_letter_grade(90.0) == "A"

    def test_score_59_point_9_is_F(self):
        assert calculate_letter_grade(59.9) == "F"

    def test_score_60_point_0_is_D(self):
        assert calculate_letter_grade(60.0) == "D"


# ═══════════════════════════════════════════════════════════════════
# SECTION B — calculate_gpa
# ═══════════════════════════════════════════════════════════════════

class TestCalculateGpa:

    def test_score_95_gives_4_0(self):
        assert calculate_gpa(95) == 4.0

    def test_score_85_gives_3_0(self):
        assert calculate_gpa(85) == 3.0

    def test_score_75_gives_2_0(self):
        assert calculate_gpa(75) == 2.0

    def test_score_65_gives_1_0(self):
        assert calculate_gpa(65) == 1.0

    def test_score_55_gives_0_0(self):
        assert calculate_gpa(55) == 0.0

    # boundary
    def test_boundary_90_gives_4_0(self):
        assert calculate_gpa(90) == 4.0

    def test_boundary_89_gives_3_0(self):
        assert calculate_gpa(89) == 3.0

    def test_boundary_80_gives_3_0(self):
        assert calculate_gpa(80) == 3.0

    def test_boundary_79_gives_2_0(self):
        assert calculate_gpa(79) == 2.0

    def test_boundary_70_gives_2_0(self):
        assert calculate_gpa(70) == 2.0

    def test_boundary_69_gives_1_0(self):
        assert calculate_gpa(69) == 1.0

    def test_boundary_60_gives_1_0(self):
        assert calculate_gpa(60) == 1.0

    def test_boundary_59_gives_0_0(self):
        assert calculate_gpa(59) == 0.0

    def test_score_0_gives_0_0(self):
        assert calculate_gpa(0) == 0.0

    def test_invalid_negative_raises(self):
        with pytest.raises(ValueError):
            calculate_gpa(-5)

    def test_invalid_over_100_raises(self):
        with pytest.raises(ValueError):
            calculate_gpa(105)


# ═══════════════════════════════════════════════════════════════════
# SECTION C — calculate_weighted_average
# ═══════════════════════════════════════════════════════════════════

class TestCalculateWeightedAverage:

    def test_equal_weights(self):
        result = calculate_weighted_average([80, 90], [0.5, 0.5])
        assert result == pytest.approx(85.0)

    def test_unequal_weights(self):
        result = calculate_weighted_average([70, 90], [0.3, 0.7])
        assert result == pytest.approx(84.0)

    def test_single_score(self):
        result = calculate_weighted_average([75], [1.0])
        assert result == pytest.approx(75.0)

    def test_three_components(self):
        result = calculate_weighted_average([60, 70, 80], [0.2, 0.3, 0.5])
        assert result == pytest.approx(73.0)

    def test_weights_not_summing_to_1_raises(self):
        with pytest.raises(ValueError):
            calculate_weighted_average([80, 90], [0.5, 0.6])

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError):
            calculate_weighted_average([80, 90], [0.5])

    def test_empty_inputs_raises(self):
        with pytest.raises(ValueError):
            calculate_weighted_average([], [])

    def test_score_out_of_range_raises(self):
        with pytest.raises(ValueError):
            calculate_weighted_average([105, 80], [0.5, 0.5])

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError):
            calculate_weighted_average([80, 90], [-0.5, 1.5])

    def test_all_zeros(self):
        result = calculate_weighted_average([0, 0], [0.5, 0.5])
        assert result == pytest.approx(0.0)

    def test_all_hundreds(self):
        result = calculate_weighted_average([100, 100, 100], [0.2, 0.3, 0.5])
        assert result == pytest.approx(100.0)


# ═══════════════════════════════════════════════════════════════════
# SECTION D — is_passing
# ═══════════════════════════════════════════════════════════════════

class TestIsPassing:

    def test_clearly_passing(self):
        assert is_passing(75) is True

    def test_clearly_failing(self):
        assert is_passing(50) is False

    def test_exact_default_threshold(self):
        """60 is the default threshold — must be True (>=, not >)."""
        assert is_passing(60) is True

    def test_one_below_default_threshold(self):
        assert is_passing(59) is False

    def test_one_above_default_threshold(self):
        assert is_passing(61) is True

    def test_custom_threshold_passes(self):
        assert is_passing(70, passing_threshold=70) is True

    def test_custom_threshold_fails(self):
        assert is_passing(69, passing_threshold=70) is False

    def test_zero_score_fails(self):
        assert is_passing(0) is False

    def test_hundred_score_passes(self):
        assert is_passing(100) is True

    def test_invalid_score_raises(self):
        with pytest.raises(ValueError):
            is_passing(-1)


# ═══════════════════════════════════════════════════════════════════
# SECTION E — calculate_grade_points & calculate_cumulative_gpa
# ═══════════════════════════════════════════════════════════════════

class TestCalculateGradePoints:

    def test_A_3_credits(self):
        assert calculate_grade_points("A", 3) == pytest.approx(12.0)

    def test_B_3_credits(self):
        assert calculate_grade_points("B", 3) == pytest.approx(9.0)

    def test_C_4_credits(self):
        assert calculate_grade_points("C", 4) == pytest.approx(8.0)

    def test_D_2_credits(self):
        assert calculate_grade_points("D", 2) == pytest.approx(2.0)

    def test_F_3_credits(self):
        assert calculate_grade_points("F", 3) == pytest.approx(0.0)

    def test_invalid_grade_raises(self):
        with pytest.raises(ValueError):
            calculate_grade_points("E", 3)

    def test_zero_credit_hours_raises(self):
        with pytest.raises(ValueError):
            calculate_grade_points("A", 0)

    def test_negative_credit_hours_raises(self):
        with pytest.raises(ValueError):
            calculate_grade_points("B", -1)


class TestCalculateCumulativeGpa:

    def test_single_A_course(self):
        assert calculate_cumulative_gpa([("A", 3)]) == pytest.approx(4.0)

    def test_mixed_grades(self):
        # (A×3 + B×3) / 6 = (12+9)/6 = 3.5
        assert calculate_cumulative_gpa([("A", 3), ("B", 3)]) == pytest.approx(3.5)

    def test_all_F_gives_0(self):
        courses = [("F", 3), ("F", 4), ("F", 2)]
        assert calculate_cumulative_gpa(courses) == pytest.approx(0.0)

    def test_empty_list_gives_0(self):
        assert calculate_cumulative_gpa([]) == pytest.approx(0.0)

    def test_weighted_by_credit_hours(self):
        # A×1, F×3  → (4+0)/4 = 1.0
        assert calculate_cumulative_gpa([("A", 1), ("F", 3)]) == pytest.approx(1.0)

    def test_perfect_gpa(self):
        courses = [("A", 3), ("A", 4), ("A", 3)]
        assert calculate_cumulative_gpa(courses) == pytest.approx(4.0)

    def test_five_varied_courses(self):
        courses = [("A", 3), ("B", 3), ("C", 4), ("D", 2), ("F", 1)]
        # (12 + 9 + 8 + 2 + 0) / 13 = 31/13 ≈ 2.3846
        assert calculate_cumulative_gpa(courses) == pytest.approx(31 / 13)