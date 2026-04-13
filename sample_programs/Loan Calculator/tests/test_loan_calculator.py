import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from loan_calculator import (
    calculate_interest_rate,
    loan_approval,
    monthly_payment,
    risk_category,
)


class TestLoanCalculator(unittest.TestCase):

    def test_interest_rate_high(self):
        self.assertEqual(calculate_interest_rate(780), 0.03)

    def test_interest_rate_medium(self):
        self.assertEqual(calculate_interest_rate(710), 0.04)

    def test_interest_rate_low(self):
        self.assertEqual(calculate_interest_rate(620), 0.07)

    def test_interest_rate_bad(self):
        self.assertEqual(calculate_interest_rate(500), 0.10)

    def test_loan_approved(self):
        self.assertTrue(loan_approval(50000, 10000, 720))

    def test_loan_rejected_low_credit(self):
        self.assertFalse(loan_approval(50000, 10000, 550))

    def test_loan_rejected_debt(self):
        self.assertFalse(loan_approval(50000, 30000, 720))

    def test_loan_rejected_income(self):
        self.assertFalse(loan_approval(15000, 2000, 720))

    def test_payment_calculation(self):
        payment = monthly_payment(100000, 30, 750)
        self.assertTrue(payment > 0)

    def test_risk_low(self):
        self.assertEqual(risk_category(760), "low")

    def test_risk_medium(self):
        self.assertEqual(risk_category(680), "medium")

    def test_risk_high(self):
        self.assertEqual(risk_category(610), "high")

    def test_risk_very_high(self):
        self.assertEqual(risk_category(500), "very_high")


if __name__ == "__main__":
    unittest.main()