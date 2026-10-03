import tkinter as tk

root = tk.Tk()
root.title("Restaurant Billing System")
root.mainloop()

from ui.main_window import MainWindow

app = MainWindow()
app.run()
self.menu_frame = tk.Frame(self.root)
self.menu_frame.pack(side=tk.LEFT)

self.bill_frame = tk.Frame(self.root)
self.bill_frame.pack(side=tk.RIGHT) 
 