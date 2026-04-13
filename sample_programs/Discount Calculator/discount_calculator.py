# ──────────────────────────────────────────────
# SECTION 2: Discount Calculator
# ──────────────────────────────────────────────

MEMBERSHIP_LEVELS = {
    "bronze":   0.05,   # 5 %
    "silver":   0.10,   # 10 %
    "gold":     0.15,   # 15 %
    "platinum": 0.20,   # 20 %
}

QUANTITY_THRESHOLDS = [
    (100, 0.20),   # 100+ units → 20 %
    (50,  0.15),   # 50–99 units → 15 %
    (20,  0.10),   # 20–49 units → 10 %
    (10,  0.05),   # 10–19 units →  5 %
    (1,   0.00),   # 1–9 units   →  0 %
]

SEASONAL_DISCOUNTS = {
    "summer":   0.08,
    "winter":   0.12,
    "spring":   0.05,
    "fall":     0.03,
    "none":     0.00,
}


def get_membership_discount(membership_level: str) -> float:
    """Return the discount rate for a membership level (case-insensitive)."""
    level = membership_level.lower().strip()
    if level not in MEMBERSHIP_LEVELS:
        raise ValueError(
            f"Invalid membership level: '{membership_level}'. "
            f"Valid levels: {list(MEMBERSHIP_LEVELS.keys())}"
        )
    return MEMBERSHIP_LEVELS[level]


def get_quantity_discount(quantity: int) -> float:
    """
    Return the discount rate for a given purchase quantity.

    Mutation targets: threshold values (100, 50, 20, 10) and discount rates.
    """
    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got {quantity}")

    for threshold, rate in QUANTITY_THRESHOLDS:
        if quantity >= threshold:
            return rate

    return 0.0


def get_seasonal_discount(season: str) -> float:
    """Return the seasonal discount rate (case-insensitive)."""
    s = season.lower().strip()
    if s not in SEASONAL_DISCOUNTS:
        raise ValueError(
            f"Invalid season: '{season}'. "
            f"Valid seasons: {list(SEASONAL_DISCOUNTS.keys())}"
        )
    return SEASONAL_DISCOUNTS[s]


def calculate_total_discount(
    base_price: float,
    quantity: int,
    membership_level: str = "none",
    season: str = "none",
    coupon_discount: float = 0.0,
    max_discount_cap: float = 0.50,
) -> dict:
    """
    Calculate a full discount breakdown and final price.

    Discounts are stacked additively, then capped at max_discount_cap.

    Args:
        base_price:       Unit price before discounts.
        quantity:         Number of units purchased.
        membership_level: Membership tier name (or 'none').
        season:           Season name (or 'none').
        coupon_discount:  Additional flat discount rate from a coupon (0–1).
        max_discount_cap: Maximum combined discount allowed (default 50 %).

    Returns:
        dict with keys: unit_price, quantity, membership_discount,
        quantity_discount, seasonal_discount, coupon_discount,
        total_discount_rate, final_unit_price, total_price, savings.

    Mutation targets: additive stacking logic, cap comparison, savings calc.
    """
    if base_price < 0:
        raise ValueError("Base price cannot be negative")
    if coupon_discount < 0 or coupon_discount > 1:
        raise ValueError("Coupon discount must be between 0 and 1")
    if max_discount_cap < 0 or max_discount_cap > 1:
        raise ValueError("Max discount cap must be between 0 and 1")

    # Resolve each discount component
    mem_discount = (
        get_membership_discount(membership_level)
        if membership_level.lower() != "none"
        else 0.0
    )
    qty_discount = get_quantity_discount(quantity)
    sea_discount = get_seasonal_discount(season)

    # Stack additively, then apply cap
    total_rate = mem_discount + qty_discount + sea_discount + coupon_discount
    total_rate = min(total_rate, max_discount_cap)

    final_unit_price = base_price * (1 - total_rate)
    total_price = final_unit_price * quantity
    savings = (base_price * quantity) - total_price

    return {
        "unit_price":          base_price,
        "quantity":            quantity,
        "membership_discount": mem_discount,
        "quantity_discount":   qty_discount,
        "seasonal_discount":   sea_discount,
        "coupon_discount":     coupon_discount,
        "total_discount_rate": total_rate,
        "final_unit_price":    round(final_unit_price, 2),
        "total_price":         round(total_price, 2),
        "savings":             round(savings, 2),
    }


def apply_coupon(coupon_code: str) -> float:
    """
    Look up a coupon code and return its discount rate.

    Mutation targets: string comparison, return values.
    """
    valid_coupons = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
        "VIP30":  0.30,
        "STAFF":  0.40,
    }
    code = coupon_code.upper().strip()
    if code not in valid_coupons:
        raise ValueError(f"Invalid coupon code: '{coupon_code}'")
    return valid_coupons[code]


def is_eligible_for_loyalty_bonus(
    purchase_count: int,
    total_spent: float,
) -> bool:
    """
    Determine whether a customer qualifies for a loyalty bonus.

    Criteria (both must be met):
        - At least 10 prior purchases
        - Total lifetime spend >= $500

    Mutation targets: the AND operator, threshold values 10 and 500.
    """
    return purchase_count >= 10 and total_spent >= 500.0


def calculate_loyalty_discount(
    purchase_count: int,
    total_spent: float,
) -> float:
    """
    Return the loyalty discount rate based on purchase history.

    Tiers:
        purchase_count >= 50 AND total_spent >= 5000 → 0.15
        purchase_count >= 25 AND total_spent >= 2500 → 0.10
        purchase_count >= 10 AND total_spent >= 500  → 0.05
        otherwise                                    → 0.00

    Mutation targets: tier thresholds and AND conditions.
    """
    if purchase_count >= 50 and total_spent >= 5000:
        return 0.15
    elif purchase_count >= 25 and total_spent >= 2500:
        return 0.10
    elif purchase_count >= 10 and total_spent >= 500:
        return 0.05
    else:
        return 0.00
