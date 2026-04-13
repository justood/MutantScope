# ═══════════════════════════════════════════════════════════════════
# SECTION F — Discount functions
# ═══════════════════════════════════════════════════════════════════

import pytest
from discount_calculator import (
    get_membership_discount,
    get_quantity_discount,
    get_seasonal_discount,
    calculate_total_discount,
    apply_coupon,
    is_eligible_for_loyalty_bonus,
    calculate_loyalty_discount,
)


class TestGetMembershipDiscount:

    def test_bronze(self):
        assert get_membership_discount("bronze") == pytest.approx(0.05)

    def test_silver(self):
        assert get_membership_discount("silver") == pytest.approx(0.10)

    def test_gold(self):
        assert get_membership_discount("gold") == pytest.approx(0.15)

    def test_platinum(self):
        assert get_membership_discount("platinum") == pytest.approx(0.20)

    def test_case_insensitive(self):
        assert get_membership_discount("GOLD") == pytest.approx(0.15)
        assert get_membership_discount("Silver") == pytest.approx(0.10)

    def test_invalid_level_raises(self):
        with pytest.raises(ValueError):
            get_membership_discount("diamond")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            get_membership_discount("")


class TestGetQuantityDiscount:

    # centre-of-tier values
    def test_200_units_gives_20_percent(self):
        assert get_quantity_discount(200) == pytest.approx(0.20)

    def test_75_units_gives_15_percent(self):
        assert get_quantity_discount(75) == pytest.approx(0.15)

    def test_30_units_gives_10_percent(self):
        assert get_quantity_discount(30) == pytest.approx(0.10)

    def test_15_units_gives_5_percent(self):
        assert get_quantity_discount(15) == pytest.approx(0.05)

    def test_5_units_gives_0_percent(self):
        assert get_quantity_discount(5) == pytest.approx(0.00)

    # exact boundaries (mutation-critical)
    def test_boundary_100_gives_20_percent(self):
        assert get_quantity_discount(100) == pytest.approx(0.20)

    def test_boundary_99_gives_15_percent(self):
        assert get_quantity_discount(99) == pytest.approx(0.15)

    def test_boundary_50_gives_15_percent(self):
        assert get_quantity_discount(50) == pytest.approx(0.15)

    def test_boundary_49_gives_10_percent(self):
        assert get_quantity_discount(49) == pytest.approx(0.10)

    def test_boundary_20_gives_10_percent(self):
        assert get_quantity_discount(20) == pytest.approx(0.10)

    def test_boundary_19_gives_5_percent(self):
        assert get_quantity_discount(19) == pytest.approx(0.05)

    def test_boundary_10_gives_5_percent(self):
        assert get_quantity_discount(10) == pytest.approx(0.05)

    def test_boundary_9_gives_0_percent(self):
        assert get_quantity_discount(9) == pytest.approx(0.00)

    def test_boundary_1_gives_0_percent(self):
        assert get_quantity_discount(1) == pytest.approx(0.00)

    def test_zero_quantity_raises(self):
        with pytest.raises(ValueError):
            get_quantity_discount(0)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            get_quantity_discount(-5)


class TestGetSeasonalDiscount:

    def test_summer(self):
        assert get_seasonal_discount("summer") == pytest.approx(0.08)

    def test_winter(self):
        assert get_seasonal_discount("winter") == pytest.approx(0.12)

    def test_spring(self):
        assert get_seasonal_discount("spring") == pytest.approx(0.05)

    def test_fall(self):
        assert get_seasonal_discount("fall") == pytest.approx(0.03)

    def test_none(self):
        assert get_seasonal_discount("none") == pytest.approx(0.00)

    def test_case_insensitive(self):
        assert get_seasonal_discount("SUMMER") == pytest.approx(0.08)

    def test_invalid_season_raises(self):
        with pytest.raises(ValueError):
            get_seasonal_discount("monsoon")


class TestCalculateTotalDiscount:

    def test_no_discounts(self):
        result = calculate_total_discount(100.0, 5)
        assert result["total_discount_rate"] == pytest.approx(0.0)
        assert result["total_price"] == pytest.approx(500.0)

    def test_membership_only(self):
        result = calculate_total_discount(100.0, 1, membership_level="gold")
        assert result["membership_discount"] == pytest.approx(0.15)
        assert result["total_discount_rate"] == pytest.approx(0.15)

    def test_quantity_discount_applied(self):
        result = calculate_total_discount(100.0, 50)
        assert result["quantity_discount"] == pytest.approx(0.15)

    def test_stacking_stays_below_cap(self):
        # platinum(0.20) + 100 units(0.20) + winter(0.12) = 0.52 → capped 0.50
        result = calculate_total_discount(
            100.0, 100, membership_level="platinum", season="winter"
        )
        assert result["total_discount_rate"] == pytest.approx(0.50)

    def test_cap_is_respected(self):
        result = calculate_total_discount(
            100.0, 100,
            membership_level="platinum",
            season="winter",
            coupon_discount=0.30,
        )
        assert result["total_discount_rate"] == pytest.approx(0.50)

    def test_savings_calculation(self):
        result = calculate_total_discount(100.0, 10, membership_level="silver")
        # qty=10 → 5%, silver → 10%, total=15%
        assert result["savings"] == pytest.approx(150.0)

    def test_negative_price_raises(self):
        with pytest.raises(ValueError):
            calculate_total_discount(-10.0, 5)

    def test_invalid_coupon_discount_raises(self):
        with pytest.raises(ValueError):
            calculate_total_discount(100.0, 5, coupon_discount=1.5)

    def test_zero_price(self):
        result = calculate_total_discount(0.0, 10, membership_level="gold")
        assert result["total_price"] == pytest.approx(0.0)

    def test_coupon_stacks_with_others(self):
        result = calculate_total_discount(
            100.0, 5, membership_level="bronze", coupon_discount=0.10
        )
        # bronze=5%, qty=0%, coupon=10% → total=15%
        assert result["total_discount_rate"] == pytest.approx(0.15)
        assert result["total_price"] == pytest.approx(425.0)

    def test_complete_order_breakdown(self):
        result = calculate_total_discount(
            200.0, 20, membership_level="silver", season="summer"
        )
        # silver=10%, qty=10%, summer=8% → 28%
        assert result["total_discount_rate"] == pytest.approx(0.28)
        assert result["final_unit_price"] == pytest.approx(144.0)
        assert result["total_price"] == pytest.approx(2880.0)
        assert result["savings"] == pytest.approx(1120.0)


class TestApplyCoupon:

    def test_SAVE10(self):
        assert apply_coupon("SAVE10") == pytest.approx(0.10)

    def test_SAVE20(self):
        assert apply_coupon("SAVE20") == pytest.approx(0.20)

    def test_VIP30(self):
        assert apply_coupon("VIP30") == pytest.approx(0.30)

    def test_STAFF(self):
        assert apply_coupon("STAFF") == pytest.approx(0.40)

    def test_case_insensitive(self):
        assert apply_coupon("save10") == pytest.approx(0.10)
        assert apply_coupon("Vip30") == pytest.approx(0.30)

    def test_invalid_code_raises(self):
        with pytest.raises(ValueError):
            apply_coupon("BOGUS")

    def test_whitespace_stripped(self):
        assert apply_coupon("  SAVE10  ") == pytest.approx(0.10)


class TestLoyaltyFunctions:

    # is_eligible_for_loyalty_bonus
    def test_both_criteria_met(self):
        assert is_eligible_for_loyalty_bonus(10, 500.0) is True

    def test_count_too_low(self):
        assert is_eligible_for_loyalty_bonus(9, 500.0) is False

    def test_spend_too_low(self):
        assert is_eligible_for_loyalty_bonus(10, 499.99) is False

    def test_neither_criteria_met(self):
        assert is_eligible_for_loyalty_bonus(5, 200.0) is False

    def test_exactly_10_purchases_500_spend(self):
        """Both thresholds exactly met — must be True (AND, >=)."""
        assert is_eligible_for_loyalty_bonus(10, 500.0) is True

    def test_one_above_each_threshold(self):
        assert is_eligible_for_loyalty_bonus(11, 501.0) is True

    # calculate_loyalty_discount
    def test_tier_platinum_loyalty(self):
        assert calculate_loyalty_discount(50, 5000) == pytest.approx(0.15)

    def test_tier_gold_loyalty(self):
        assert calculate_loyalty_discount(25, 2500) == pytest.approx(0.10)

    def test_tier_silver_loyalty(self):
        assert calculate_loyalty_discount(10, 500) == pytest.approx(0.05)

    def test_no_loyalty_discount(self):
        assert calculate_loyalty_discount(5, 200) == pytest.approx(0.00)

    def test_boundary_50_purchases_5000_spend(self):
        assert calculate_loyalty_discount(50, 5000) == pytest.approx(0.15)

    def test_boundary_49_purchases_5000_spend_drops_tier(self):
        assert calculate_loyalty_discount(49, 5000) == pytest.approx(0.10)

    def test_boundary_50_purchases_4999_spend_drops_tier(self):
        assert calculate_loyalty_discount(50, 4999) == pytest.approx(0.10)

    def test_high_count_low_spend_no_bonus(self):
        assert calculate_loyalty_discount(100, 100) == pytest.approx(0.00)
