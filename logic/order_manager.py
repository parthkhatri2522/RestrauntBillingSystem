orders = {}

def add_item(item):
    orders[item] = orders.get(item, 0) + 1

def remove_item(item):
    if item in orders:
        orders[item] -= 1
        if orders[item] <= 0:
            del orders[item]