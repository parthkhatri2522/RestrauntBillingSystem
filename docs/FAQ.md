# Frequently Asked Questions

**How do I add an item?** Click + next to the dish.

**How do I remove an item?** Click −. At quantity zero, it disappears.

**Can I order across categories?** Yes.

**How is the bill calculated?** The subtotal is the sum of quantity times unit price; the demo adds 5% GST.

**What happens when the order is empty?** Generate and Save show a warning.

**Where are receipts saved?** In `bills/` as UTF-8 text files.

**Can I change the menu?** Yes, edit `data/menu_data.py`.

**Can I change the GST rate?** Yes, edit `GST_RATE` in `logic/billing.py`. Confirm real-world tax rules separately.

**Does the app require internet?** No.

**Why is my screen blank?** Check that `main.py` only starts `MainWindow` and that the UI file creates its widgets.
