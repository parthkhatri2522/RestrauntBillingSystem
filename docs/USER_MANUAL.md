# User Manual

## Start

Open a terminal in the project folder and run `python main.py`.

## Menu

Browse categories on the left using the scrollbar or mouse wheel. Click **+** to increase a dish quantity and **−** to decrease it. You can mix categories in one order.

## Current bill

The right panel displays the item, quantity, price, subtotal, example 5% GST, and grand total. The display updates whenever you change the order.

## Final bill

Click **Generate Bill** to open a detailed receipt with date and time. An empty order triggers a warning.

## Save bill

Click **Save Bill** to write a UTF-8 `.txt` receipt into `bills/`. Each receipt uses a timestamped filename.

## Clear order

Click **Clear Order** and confirm to remove all items.

## Help and About

Use **Help / FAQ** for instructions, and **About** for version information.

## Change menu

Edit `data/menu_data.py` to add categories, dishes, or prices. Keep each dish name unique across categories.

## Change demo GST

Edit `GST_RATE` in `logic/billing.py`. The default 5% is for demonstration only.
