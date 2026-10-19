"""Tkinter restaurant billing application."""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

from data.menu_data import menu
from logic.order_manager import orders, add_item, remove_item, clear_order
from logic.billing import calculate_subtotal, calculate_gst, calculate_grand_total
from utils.helpers import get_price, format_money


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurant Billing System")
        self.root.geometry("1150x720")
        self.root.minsize(800, 540)
        self.root.configure(bg="#eef2f6")
        self._make_layout()
        self._make_menu()
        self._make_bill()
        self._make_actions()
        self.update_bill()

    def _make_layout(self):
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        left = tk.Frame(self.root, bg="white", padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        self.menu_canvas = tk.Canvas(left, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(left, orient="vertical", command=self.menu_canvas.yview)
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.menu_frame = tk.Frame(self.menu_canvas, bg="white")
        self.menu_window = self.menu_canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        self.menu_frame.bind("<Configure>", lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all")))
        self.menu_canvas.bind("<Configure>", lambda e: self.menu_canvas.itemconfigure(self.menu_window, width=e.width))
        self.menu_canvas.bind("<Enter>", self._bind_wheel)
        self.menu_canvas.bind("<Leave>", self._unbind_wheel)

        self.bill_frame = tk.Frame(self.root, bg="white", padx=12, pady=12)
        self.bill_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        self.actions = tk.Frame(self.root, bg="#eef2f6", pady=7)
        self.actions.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _bind_wheel(self, event):
        self.root.bind_all("<MouseWheel>", self._wheel)
        self.root.bind_all("<Button-4>", self._wheel)
        self.root.bind_all("<Button-5>", self._wheel)

    def _unbind_wheel(self, event):
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    def _wheel(self, event):
        if getattr(event, "num", None) == 4:
            steps = -1
        elif getattr(event, "num", None) == 5:
            steps = 1
        else:
            steps = -1 if event.delta > 0 else 1
        self.menu_canvas.yview_scroll(steps, "units")

    def _make_menu(self):
        tk.Label(self.menu_frame, text="INDIAN RESTAURANT MENU", font=("Arial", 18, "bold"), bg="white", fg="#183b56").pack(anchor="w", pady=(3, 12))
        for category, items in menu.items():
            tk.Label(self.menu_frame, text=category.upper(), font=("Arial", 12, "bold"), bg="white", fg="#08775c").pack(anchor="w", pady=(12, 4))
            for name, price in items.items():
                line = tk.Frame(self.menu_frame, bg="white")
                line.pack(fill=tk.X, pady=2)
                tk.Label(line, text=f"{name}  —  {format_money(price)}", font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
                tk.Button(line, text="+", width=3, command=lambda n=name: self._change_order(n, True)).pack(side=tk.LEFT, padx=2)
                tk.Button(line, text="−", width=3, command=lambda n=name: self._change_order(n, False)).pack(side=tk.LEFT, padx=2)

    def _make_bill(self):
        tk.Label(self.bill_frame, text="CURRENT BILL", font=("Arial", 18, "bold"), bg="white", fg="#183b56").pack(pady=(3, 12))
        self.bill_text = tk.Text(self.bill_frame, font=("Consolas", 10), wrap=tk.WORD, padx=10, pady=10)
        self.bill_text.pack(fill=tk.BOTH, expand=True)

    def _make_actions(self):
        for label, callback in [
            ("Generate Bill", self.generate_bill),
            ("Save Bill", self.save_bill),
            ("Clear Order", self.clear_order),
            ("Help / FAQ", self.show_help),
            ("About", self.show_about),
        ]:
            tk.Button(self.actions, text=label, command=callback, font=("Arial", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=6)

    def _change_order(self, name, increase):
        if increase:
            add_item(name)
        else:
            remove_item(name)
        self.update_bill()

    def update_bill(self):
        self.bill_text.configure(state=tk.NORMAL)
        self.bill_text.delete("1.0", tk.END)
        self.bill_text.insert(tk.END, "========= RESTAURANT BILL =========\n\n")
        if not orders:
            self.bill_text.insert(tk.END, "No items selected.\nClick + to add food items.")
        else:
            self.bill_text.insert(tk.END, self._bill_body())
        self.bill_text.configure(state=tk.DISABLED)

    def _bill_body(self):
        lines = []
        for name, qty in orders.items():
            price = get_price(name)
            lines.extend([name, f"  {qty} x {format_money(price)} = {format_money(qty * price)}", ""])
        subtotal = calculate_subtotal(orders)
        lines.extend([
            "-" * 32,
            f"Subtotal:    {format_money(subtotal)}",
            f"GST (5%):    {format_money(calculate_gst(subtotal))}",
            f"Grand Total: {format_money(calculate_grand_total(orders))}",
            "=" * 32,
        ])
        return "\n".join(lines)

    def _final_bill(self):
        now = datetime.now()
        return ("=" * 32 + "\n      RESTAURANT BILL\n" + "=" * 32 +
                f"\nDate: {now:%d-%m-%Y}\nTime: {now:%H:%M:%S}\n\n" + self._bill_body() + "\n")

    def generate_bill(self):
        if not orders:
            messagebox.showwarning("Empty Order", "Add at least one item first.", parent=self.root)
            return
        popup = tk.Toplevel(self.root)
        popup.title("Final Bill")
        popup.geometry("480x540")
        display = tk.Text(popup, font=("Consolas", 10), padx=12, pady=12)
        display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        display.insert(tk.END, self._final_bill())
        display.configure(state=tk.DISABLED)

    def save_bill(self):
        if not orders:
            messagebox.showwarning("Empty Order", "Add at least one item first.", parent=self.root)
            return
        directory = Path(__file__).resolve().parent.parent / "bills"
        try:
            directory.mkdir(parents=True, exist_ok=True)
            path = directory / datetime.now().strftime("bill_%Y%m%d_%H%M%S_%f.txt")
            path.write_text(self._final_bill(), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save Failed", str(exc), parent=self.root)
            return
        messagebox.showinfo("Bill Saved", f"Saved to:\n{path}", parent=self.root)

    def clear_order(self):
        if not orders:
            messagebox.showinfo("Clear Order", "The order is already empty.", parent=self.root)
        elif messagebox.askyesno("Clear Order", "Remove all items?", parent=self.root):
            clear_order()
            self.update_bill()

    def show_help(self):
        popup = tk.Toplevel(self.root)
        popup.title("Help / FAQ")
        popup.geometry("570x440")
        help_text = (
            "HELP / FREQUENTLY ASKED QUESTIONS\n\n"
            "Q: How do I add food?\nA: Click + next to the item.\n\n"
            "Q: How do I remove food?\nA: Click − next to the item.\n\n"
            "Q: How is the total calculated?\nA: Quantity × price, plus demo 5% GST.\n\n"
            "Q: Can I mix categories?\nA: Yes, select from any menu category.\n\n"
            "Q: How do I save a bill?\nA: Click Save Bill; a text file is created in bills/.\n\n"
            "Q: Where is the user manual?\nA: See docs/USER_MANUAL.md.\n"
        )
        display = tk.Text(popup, wrap=tk.WORD, font=("Arial", 11), padx=16, pady=16)
        display.pack(fill=tk.BOTH, expand=True)
        display.insert(tk.END, help_text)
        display.configure(state=tk.DISABLED)

    def show_about(self):
        popup = tk.Toplevel(self.root)
        popup.title("About")
        popup.geometry("440x270")
        tk.Label(popup, text="Restaurant Billing System", font=("Arial", 17, "bold")).pack(pady=(24, 10))
        tk.Label(popup, text="Version 1.0\nPython + Tkinter\n\nAcademic restaurant billing project", font=("Arial", 11), justify=tk.CENTER).pack(pady=10)
        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def run(self):
        self.root.mainloop()
