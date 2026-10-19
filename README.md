# Restaurant Billing System

A desktop billing application built using Python and Tkinter, featuring a categorized Indian restaurant menu.

## Quick start (interactive checklist)

- [ ] Install Python 3.9 or newer with Tkinter support.
- [ ] Open a terminal in this project directory.
- [ ] Run `python main.py` (Windows also supports `py main.py`).
- [ ] Click **+** next to a food item.
- [ ] Review the live bill and click **Generate Bill**.
- [ ] Click **Save Bill** and find the receipt in `bills/`.

## Features

- Starters, breakfast, vegetarian and non-vegetarian mains, rice, breads, beverages and desserts
- Quantity increment/decrement and live subtotal
- Configurable example GST rate (5%) and grand total
- Final bill popup, saved UTF-8 text receipts, clear confirmation
- Scrollable menu, in-app Help/FAQ, About window, and inline comments

## Folder guide

- `main.py`: application entry point
- `ui/main_window.py`: interface, popups, scrolling
- `data/menu_data.py`: category-wise items and sample prices
- `logic/order_manager.py`: order quantities
- `logic/billing.py`: totals and tax calculations
- `utils/helpers.py`: menu price lookup and currency formatting
- `docs/USER_MANUAL.md`: step-by-step usage
- `docs/FAQ.md`: common questions
- `bills/`: generated receipts

## Troubleshooting

**Blank window:** Ensure `main.py` calls `MainWindow().run()` and `ui/main_window.py` contains the complete class.

**ModuleNotFoundError:** Run `python main.py` from the project root, not from inside `ui/`.

**Tkinter missing:** Install a Python distribution with Tk support.

## Tax note

The 5% GST rate is a demonstration assumption for an academic project. Real restaurant GST treatment varies; confirm applicable rates before commercial use.

## Dependencies

No external Python packages are required for a standard Python installation with Tkinter.
