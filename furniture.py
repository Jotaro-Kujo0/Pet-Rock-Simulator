import tkinter as tk
from data_manager import DataManager

class Bench:
    def __init__(self, parent, x, y):
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.attributes('-topmost', False) # Bench sits behind pet
        
        self.x, self.y = x, y
        # Two interaction slots relative to bench position
        self.slots = [x + 15, x + 65]
        self.occupants = [None, None]

        self.img = DataManager.safe_load("assets/bench.png")
        if self.img:
            self.label = tk.Label(self.window, image=self.img, bg='black', bd=0)
            self.label.image = self.img
        else:
            self.label = tk.Label(self.window, text="[BENCH]", bg="#4a2c2a", fg="white", width=12)
        
        self.label.pack()
        self.window.geometry(f"+{int(x)}+{int(y)}")

    def find_free_slot(self, pet_x):
        """Checks if pet is dropped near a slot. Returns (index, x_coord)."""
        for i, slot_x in enumerate(self.slots):
            if abs(pet_x - slot_x) < 70 and self.occupants[i] is None:
                return i, slot_x
        return None, None
