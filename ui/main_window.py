"""Tkinter restaurant billing application — modern themed UI."""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

from data.menu_data import menu
from logic.order_manager import orders, add_item, remove_item, clear_order
from logic.billing import calculate_subtotal, calculate_gst, calculate_grand_total
from utils.helpers import get_price, format_money

C = {
    "bg": "#EEF1F6",
    "surface": "#FFFFFF",
    "alt": "#F7F9FC",
    "ink": "#0F172A",
    "muted": "#64748B",
    "line": "#E2E8F0",
    "brand": "#0F766E",
    "brand_dk": "#115E59",
    "accent": "#F59E0B",
    "accent_dk": "#D97706",
    "danger": "#DC2626",
    "dark": "#0B1220",
    "dark2": "#111827",
    "on_dark": "#E5E7EB",
}
SANS = "Segoe UI"
MONO = "Consolas"


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurant Billing System")
        self.root.geometry("1180x760")
        self.root.minsize(860, 560)
        self.root.configure(bg=C["bg"])
        self.qty_labels = {}
        self._make_header()
        self._make_layout()
        self._make_menu()
        self._make_bill()
        self._make_actions()
        self.update_bill()
        self._tick()

    # ---------- building blocks ----------

    def _btn(self, parent, text, command=None, kind="ghost"):
        styles = {
            "primary": (C["accent"], "#1F1300", C["accent_dk"], "#1F1300", None),
            "brand": (C["brand"], "white", C["brand_dk"], "white", None),
            "ghost": (C["surface"], C["ink"], C["line"], C["ink"], C["line"]),
            "quiet": ("#F1F5F9", "#475569", "#E2E8F0", "#334155", C["line"]),
            "danger": (C["surface"], C["danger"], "#FEE2E2", C["danger"], "#FECACA"),
            "dark": (C["dark2"], C["on_dark"], "#1F2937", "#FFFFFF", "#374151"),
        }
        bg, fg, hbg, hfg, border = styles[kind]
        btn = tk.Button(
            parent, text=text, command=command, relief="flat", bd=0,
            highlightthickness=1 if border else 0, highlightbackground=border or bg,
            cursor="hand2", font=(SANS, 10, "bold"),
            padx=16, pady=6, bg=bg, fg=fg, activebackground=hbg, activeforeground=hfg,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hbg, fg=hfg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))
        return btn

    def _make_header(self):
        header = tk.Frame(self.root, bg=C["ink"], height=78)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)

        logo = tk.Frame(header, bg=C["accent"], width=44, height=44)
        logo.pack(side=tk.LEFT, padx=(20, 12), pady=17)
        logo.pack_propagate(False)
        tk.Label(logo, text="R", font=(SANS, 20, "bold"), bg=C["accent"], fg=C["ink"]).pack(expand=True)

        titles = tk.Frame(header, bg=C["ink"])
        titles.pack(side=tk.LEFT, pady=12)
        tk.Label(titles, text="Restaurant Billing System", font=(SANS, 17, "bold"),
                 bg=C["ink"], fg="#FFFFFF", anchor="w").pack(anchor="w")
        tk.Label(titles, text="Point of Sale  •  Billing Counter", font=(SANS, 9),
                 bg=C["ink"], fg="#94A3B8", anchor="w").pack(anchor="w")

        self.clock = tk.Label(header, font=(SANS, 10), bg=C["ink"], fg=C["on_dark"])
        self.clock.pack(side=tk.RIGHT, padx=24)

        tk.Frame(self.root, bg=C["accent"], height=3).grid(row=1, column=0, columnspan=2, sticky="ew")

    def _make_layout(self):
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=1)

        self.menu_card = tk.Frame(self.root, bg=C["surface"], highlightthickness=1,
                                  highlightbackground=C["line"], padx=14, pady=14)
        self.menu_card.grid(row=2, column=0, sticky="nsew", padx=(16, 8), pady=16)

        self.bill_card = tk.Frame(self.root, bg=C["surface"], highlightthickness=1,
                                  highlightbackground=C["line"], padx=14, pady=14)
        self.bill_card.grid(row=2, column=1, sticky="nsew", padx=(8, 16), pady=16)

        wrap = tk.Frame(self.root, bg=C["bg"])
        wrap.grid(row=3, column=0, columnspan=2, sticky="ew")
        tk.Frame(wrap, bg=C["line"], height=1).pack(fill=tk.X)
        self.actions = tk.Frame(wrap, bg=C["bg"], pady=10)
        self.actions.pack(fill=tk.X, padx=16)

        self.menu_canvas = tk.Canvas(self.menu_card, bg=C["surface"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.menu_card, orient="vertical", command=self.menu_canvas.yview,
                                 troughcolor=C["surface"], bg=C["line"], relief="flat", width=10)
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.menu_frame = tk.Frame(self.menu_canvas, bg=C["surface"])
        self.menu_window = self.menu_canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        self.menu_frame.bind("<Configure>", lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all")))
        self.menu_canvas.bind("<Configure>", lambda e: self.menu_canvas.itemconfigure(self.menu_window, width=e.width))
        self.menu_canvas.bind("<Enter>", self._bind_wheel)
        self.menu_canvas.bind("<Leave>", self._unbind_wheel)

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

    # ---------- menu panel ----------

    def _make_menu(self):
        top = tk.Frame(self.menu_frame, bg=C["surface"])
        top.pack(fill=tk.X, pady=(0, 4))
        tk.Label(top, text="MENU", font=(SANS, 16, "bold"), bg=C["surface"], fg=C["ink"]).pack(anchor="w")
        tk.Label(top, text="Tap + to add a dish, − to remove it", font=(SANS, 9),
                 bg=C["surface"], fg=C["muted"]).pack(anchor="w")

        for category, items in menu.items():
            head = tk.Frame(self.menu_frame, bg=C["alt"], padx=10, pady=6)
            head.pack(fill=tk.X, pady=(16, 4))
            tk.Frame(head, bg=C["accent"], width=4).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            tk.Label(head, text=category.upper(), font=(SANS, 11, "bold"),
                     bg=C["alt"], fg=C["brand"]).pack(side=tk.LEFT)

            for name, price in items.items():
                row = tk.Frame(self.menu_frame, bg=C["surface"], padx=8, pady=5)
                row.pack(fill=tk.X)
                tk.Label(row, text=name, font=(SANS, 10), bg=C["surface"],
                         fg=C["ink"], anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
                tk.Label(row, text=format_money(price), font=(SANS, 10, "bold"),
                         bg=C["surface"], fg=C["brand"], width=10, anchor="e").pack(side=tk.LEFT)

                qty = tk.Label(row, text="", font=(SANS, 9, "bold"), bg=C["surface"],
                               fg=C["brand"], width=3)
                qty.pack(side=tk.LEFT, padx=(4, 8))
                self.qty_labels[name] = qty

                self._btn(row, "−", lambda n=name: self._change_order(n, False), "quiet").pack(side=tk.LEFT, padx=2)
                self._btn(row, "+", lambda n=name: self._change_order(n, True), "brand").pack(side=tk.LEFT, padx=2)
                tk.Frame(self.menu_frame, bg=C["line"], height=1).pack(fill=tk.X)

    # ---------- bill panel ----------

    def _make_bill(self):
        head = tk.Frame(self.bill_card, bg=C["surface"])
        head.pack(fill=tk.X, pady=(0, 8))
        tk.Label(head, text="CURRENT BILL", font=(SANS, 16, "bold"),
                 bg=C["surface"], fg=C["ink"]).pack(side=tk.LEFT)
        self.count_badge = tk.Label(head, text="0 items", font=(SANS, 9, "bold"),
                                    bg=C["alt"], fg=C["muted"], padx=8, pady=2)
        self.count_badge.pack(side=tk.RIGHT)

        self.bill_text = tk.Text(self.bill_card, font=(MONO, 10), wrap=tk.WORD, padx=12, pady=12,
                                 bg=C["dark"], fg=C["on_dark"], insertbackground=C["on_dark"],
                                 relief="flat", highlightthickness=1, highlightbackground="#1F2937",
                                 selectbackground=C["brand"], spacing1=2, spacing3=2)
        self.bill_text.pack(fill=tk.BOTH, expand=True)
        self.bill_text.tag_configure("head", foreground=C["accent"], font=(MONO, 11, "bold"))
        self.bill_text.tag_configure("muted", foreground="#94A3B8")
        self.bill_text.tag_configure("total", foreground="#5EEAD4", font=(MONO, 11, "bold"))

        band = tk.Frame(self.bill_card, bg=C["brand_dk"], padx=14, pady=10)
        band.pack(fill=tk.X, pady=(10, 0))
        left = tk.Frame(band, bg=C["brand_dk"])
        left.pack(side=tk.LEFT)
        tk.Label(left, text="Subtotal", font=(SANS, 9), bg=C["brand_dk"], fg="#A7F3D0").pack(anchor="w")
        self.lbl_sub = tk.Label(left, text="₹0.00", font=(SANS, 10, "bold"), bg=C["brand_dk"], fg="white")
        self.lbl_sub.pack(anchor="w")
        tk.Label(left, text="GST 5%", font=(SANS, 9), bg=C["brand_dk"], fg="#A7F3D0").pack(anchor="w", pady=(4, 0))
        self.lbl_gst = tk.Label(left, text="₹0.00", font=(SANS, 10, "bold"), bg=C["brand_dk"], fg="white")
        self.lbl_gst.pack(anchor="w")

        right = tk.Frame(band, bg=C["brand_dk"])
        right.pack(side=tk.RIGHT)
        tk.Label(right, text="GRAND TOTAL", font=(SANS, 9, "bold"), bg=C["brand_dk"],
                 fg="#A7F3D0").pack(anchor="e")
        self.lbl_total = tk.Label(right, text="₹0.00", font=(SANS, 22, "bold"),
                                  bg=C["brand_dk"], fg=C["accent"])
        self.lbl_total.pack(anchor="e")

    def _make_actions(self):
        left = tk.Frame(self.actions, bg=C["bg"])
        left.pack(side=tk.LEFT)
        self._btn(left, "Help / FAQ", self.show_help, "ghost").pack(side=tk.LEFT, padx=(0, 6))
        self._btn(left, "About", self.show_about, "ghost").pack(side=tk.LEFT)

        right = tk.Frame(self.actions, bg=C["bg"])
        right.pack(side=tk.RIGHT)
        self._btn(right, "Clear Order", self.clear_order, "danger").pack(side=tk.RIGHT, padx=(6, 0))
        self._btn(right, "Save Bill", self.save_bill, "brand").pack(side=tk.RIGHT, padx=(6, 0))
        self._btn(right, "Generate Bill", self.generate_bill, "primary").pack(side=tk.RIGHT, padx=(6, 0))

    # ---------- behaviour ----------

    def _change_order(self, name, increase):
        if increase:
            add_item(name)
        else:
            remove_item(name)
        self.update_bill()

    def update_bill(self):
        self.bill_text.configure(state=tk.NORMAL)
        self.bill_text.delete("1.0", tk.END)
        self.bill_text.insert(tk.END, "  RESTAURANT BILL\n", "head")
        self.bill_text.insert(tk.END, "  " + "—" * 30 + "\n\n", "muted")
        if not orders:
            self.bill_text.insert(tk.END, "  No items selected yet.\n  Click + on any dish to start the order.", "muted")
        else:
            self._bill_body()
        self.bill_text.configure(state=tk.DISABLED)

        self.count_badge.configure(
            text=f"{len(orders)} items" if len(orders) != 1 else "1 item",
            bg=C["brand"] if orders else C["alt"],
            fg="white" if orders else C["muted"],
        )
        subtotal = calculate_subtotal(orders)
        self.lbl_sub.configure(text=format_money(subtotal))
        self.lbl_gst.configure(text=format_money(calculate_gst(subtotal)))
        self.lbl_total.configure(text=format_money(calculate_grand_total(orders)))

        for name, label in self.qty_labels.items():
            qty = orders.get(name, 0)
            label.configure(text=f"x{qty}" if qty else "")

    def _bill_body(self):
        for name, qty in orders.items():
            price = get_price(name)
            self.bill_text.insert(tk.END, f"  {name}\n")
            self.bill_text.insert(
                tk.END, f"    {qty} x {format_money(price)} = {format_money(qty * price)}\n",
            )
        subtotal = calculate_subtotal(orders)
        self.bill_text.insert(tk.END, "\n  " + "—" * 30 + "\n", "muted")
        self.bill_text.insert(tk.END, f"  Subtotal:    {format_money(subtotal)}\n")
        self.bill_text.insert(tk.END, f"  GST (5%):    {format_money(calculate_gst(subtotal))}\n")
        self.bill_text.insert(
            tk.END, f"  Grand Total: {format_money(calculate_grand_total(orders))}\n", "total"
        )

    def _final_bill(self):
        now = datetime.now()
        return ("=" * 32 + "\n      RESTAURANT BILL\n" + "=" * 32 +
                f"\nDate: {now:%d-%m-%Y}\nTime: {now:%H:%M:%S}\n\n" + self._plain_bill() + "\n")

    def _plain_bill(self):
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

    def _popup(self, title, width, height):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(f"{width}x{height}")
        popup.configure(bg=C["bg"])
        bar = tk.Frame(popup, bg=C["ink"], height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text=title, font=(SANS, 13, "bold"), bg=C["ink"], fg="white").pack(
            side=tk.LEFT, padx=16)
        self._btn(bar, "✕", popup.destroy, "dark").pack(side=tk.RIGHT, padx=12, pady=10)
        return popup

    def generate_bill(self):
        if not orders:
            messagebox.showwarning("Empty Order", "Add at least one item first.", parent=self.root)
            return
        popup = self._popup("Final Bill", 470, 540)
        display = tk.Text(popup, font=(MONO, 10), padx=14, pady=14, bg=C["dark"],
                          fg=C["on_dark"], relief="flat", highlightthickness=0)
        display.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
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
        popup = self._popup("Help / FAQ", 570, 440)
        help_text = (
            "HELP / FREQUENTLY ASKED QUESTIONS\n\n"
            "Q: How do I add food?\nA: Click + next to the item.\n\n"
            "Q: How do I remove food?\nA: Click − next to the item.\n\n"
            "Q: How is the total calculated?\nA: Quantity × price, plus demo 5% GST.\n\n"
            "Q: Can I mix categories?\nA: Yes, select from any menu category.\n\n"
            "Q: How do I save a bill?\nA: Click Save Bill; a text file is created in bills/.\n\n"
            "Q: Where is the user manual?\nA: See docs/USER_MANUAL.md.\n"
        )
        display = tk.Text(popup, wrap=tk.WORD, font=(SANS, 11), padx=16, pady=16,
                          bg=C["surface"], fg=C["ink"], relief="flat", highlightthickness=0)
        display.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
        display.insert(tk.END, help_text)
        display.configure(state=tk.DISABLED)

    def show_about(self):
        popup = self._popup("About", 440, 280)
        tk.Label(popup, text="Restaurant Billing System", font=(SANS, 17, "bold"),
                 bg=C["bg"], fg=C["ink"]).pack(pady=(26, 10))
        tk.Label(popup, text="Version 1.0\nPython + Tkinter\n\nAcademic restaurant billing project",
                 font=(SANS, 11), bg=C["bg"], fg=C["muted"], justify=tk.CENTER).pack(pady=10)
        self._btn(popup, "Close", popup.destroy, "brand").pack(pady=14)

    def _tick(self):
        now = datetime.now()
        self.clock.configure(text=now.strftime("%A, %d %B %Y   •   %H:%M:%S"))
        self.root.after(1000, self._tick)

    def run(self):
        self.root.mainloop()
