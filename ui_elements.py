import tkinter as tk
from data_manager import DataManager

class CornerMenu:
    def __init__(self, parent, open_shop_cb, open_diary_cb):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.wm_attributes("-transparentcolor", "black")
        self.win.geometry("50x50+10+10")

        self.icon = DataManager.safe_load("assets/settings_logo.png")
        if self.icon:
            btn = tk.Button(self.win, image=self.icon, bg="black", bd=0, command=open_shop_cb)
            btn.image = self.icon
        else:
            btn = tk.Button(self.win, text="⚙", command=open_shop_cb)
        btn.pack()

class DiaryWindow:
    def __init__(self, parent):
        data = DataManager.load_data()
        self.win = tk.Toplevel(parent)
        self.win.title("Pet Diary")
        self.win.geometry("300x200")
        
        tk.Label(self.win, text=data['pet_name'], font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.win, text=data['bio'], wraplength=250).pack(pady=10)
        tk.Button(self.win, text="Close", command=self.win.destroy).pack()
