"""Run: python -m unittest discover -s tests -v"""
import unittest
from decimal import Decimal
from logic.billing import calculate_subtotal, calculate_gst, calculate_grand_total
from utils.helpers import get_price


class BillingTests(unittest.TestCase):
    def test_price_lookup(self):
        self.assertEqual(get_price("Paneer Tikka"), 220)

    def test_subtotal(self):
        self.assertEqual(calculate_subtotal({"Paneer Tikka": 2}), Decimal("440"))

    def test_tax(self):
        self.assertEqual(calculate_gst(Decimal("440")), Decimal("22.00"))

    def test_grand_total(self):
        self.assertEqual(calculate_grand_total({"Paneer Tikka": 2}), Decimal("462.00"))

    def test_empty_order(self):
        self.assertEqual(calculate_grand_total({}), Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()
