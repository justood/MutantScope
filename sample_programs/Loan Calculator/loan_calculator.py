def calculate_interest_rate(credit_score):
    """Return interest rate based on credit score"""
    if credit_score >= 750:
        return 0.03
    elif credit_score >= 700:
        return 0.04
    elif credit_score >= 650:
        return 0.05
    elif credit_score >= 600:
        return 0.07
    else:
        return 0.10


def loan_approval(income, debt, credit_score):
    """Determine if a loan should be approved"""
    debt_ratio = debt / income

    if credit_score < 600:
        return False

    if debt_ratio > 0.5:
        return False

    if income < 20000:
        return False

    return True


def monthly_payment(principal, years, credit_score):
    """Calculate monthly loan payment"""
    rate = calculate_interest_rate(credit_score)

    monthly_rate = rate / 12
    months = years * 12

    if monthly_rate == 0:
        return principal / months

    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)

    return round(payment, 2)


def risk_category(credit_score):
    """Categorize borrower risk"""
    if credit_score >= 750:
        return "low"
    elif credit_score >= 650:
        return "medium"
    elif credit_score >= 600:
        return "high"
    else:
        return "very_high"