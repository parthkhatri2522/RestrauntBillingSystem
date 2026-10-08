import tkinter as tk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurant Billing System")

    def run(self):
        self.root.mainloop()
        from data.menu_data import menu

from data.menu_data import menu

for category, items in menu.items():
    tk.Label(self.menu_frame, text=category, font=("Arial", 12, "bold")).pack(anchor="w")
    
    for item, price in items.items():
        tk.Label(self.menu_frame, text=f"  {item} - ₹{price}").pack(anchor="w")
        for category, items in menu.items():
    tk.Label(self.menu_frame, text=category, font=("Arial", 12, "bold")).pack(anchor="w")

    for item, price in items.items():
        frame = tk.Frame(self.menu_frame)
        frame.pack(anchor="w")

        tk.Label(frame, text=f"{item} - ₹{price}", width=20).pack(side=tk.LEFT)
        tk.Button(frame, text="+", command=lambda i=item: add_item(i)).pack(side=tk.LEFT)
        tk.Button(frame, text="-", command=lambda i=item: remove_item(i)).pack(side=tk.LEFT)

        total = calculate_total(orders)
self.bill_text.insert(tk.END, f"\nTotal: ₹{total}")

def update_bill(self):

    self.bill_text.delete("1.0", tk.END)

    self.bill_text.insert(
        tk.END,
        "========== BILL ==========\n\n"
    )

    for item, quantity in orders.items():

        price = get_price(item)
        amount = price * quantity

        self.bill_text.insert(
            tk.END,
            f"{item}\n"
            f"  {quantity} x ₹{price} = ₹{amount}\n\n"
        )

    total = calculate_total(orders)

    self.bill_text.insert(
        tk.END,
        "--------------------------\n"
    )

    self.bill_text.insert(
        tk.END,
        f"Total: ₹{total}\n"
    )

    self.bill_text.insert(
    tk.END,
    "\n==========================\n"
)

self.bill_text.insert(
    tk.END,
    f"Total: ₹{total}\n"
)

self.bill_text.insert(
    tk.END,
    "==========================\n"
)