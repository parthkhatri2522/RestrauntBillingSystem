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
tk.Label(self.menu_frame, text="Menu").pack()
tk.Label(self.bill_frame, text="Bill").pack()
self.bill_text = tk.Text(self.bill_frame)
self.bill_text.pack()