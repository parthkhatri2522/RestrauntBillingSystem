"""Helpers for menu lookups and currency formatting."""
from data.menu_data import menu


def get_price(item_name):
    """Find an item price, raising an error if the item is unknown."""
    for items in menu.values():
        if item_name in items:
            return items[item_name]
    raise KeyError(f"Unknown menu item: {item_name}")


def format_money(amount):
    return f"₹{amount:,.2f}"
