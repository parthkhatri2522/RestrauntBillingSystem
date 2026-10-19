"""Billing calculations. 5% GST is a demo setting, not tax advice."""
from decimal import Decimal, ROUND_HALF_UP
from utils.helpers import get_price

GST_RATE = Decimal("0.05")


def calculate_subtotal(current_orders):
    return sum((Decimal(get_price(item)) * qty for item, qty in current_orders.items()), Decimal("0"))


def calculate_gst(subtotal):
    return (Decimal(subtotal) * GST_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_grand_total(current_orders):
    subtotal = calculate_subtotal(current_orders)
    return subtotal + calculate_gst(subtotal)


def calculate_total(current_orders):
    """Compatibility helper for earlier project commits."""
    return calculate_subtotal(current_orders)
