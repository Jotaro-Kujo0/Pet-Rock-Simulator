import tkinter as tk
import random
from data_manager import DataManager
from furniture import Bench
from ui_elements import CornerMenu, DiaryWindow
from shop import Shop

class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')

        # Screen & Gravity Setup
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.floor_y = self.screen_h - 120 
        
        self.x, self.y = int(self.screen_w * 0.8), self.floor_y
        self.dragging = False
        self.state = 0 
        self.frame_index = 0
        self.benches = []
        self.current_bench_slot = None

        # Load Sprites
        self.sprites = {
            'idle': [DataManager.safe_load(f"assets/idle{i}.png") for i in range(1, 5)],
            'walk_l': [DataManager.safe_load(f"assets/walkingleft{i}.png") for i in range(1, 5)],
            'walk_r': [DataManager.safe_load(f"assets/walkingright{i}.png") for i in range(1, 5)]
        }
        
        self.label = tk.Label(self.root, bg='black', bd=0)
        self.label.pack()

        # Components
        self.menu = CornerMenu(self.root, self.open_shop, self.open_diary)
        
        # Bindings
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Button-3>", lambda e: self.open_diary())

        # Loops
        self.update_behavior()
        self.animate()
        self.coin_loop()
        self.root.mainloop()

    def coin_loop(self):
        data = DataManager.load_data()
        data['coins'] += 10
        DataManager.save_data(data)
        self.root.after(600000, self.coin_loop)

    def update_behavior(self):
        # Only change state if NOT sitting on a bench
        if not self.dragging and self.state != "sitting":
            chance = random.randint(1, 26)
            if chance <= 12: self.state = 0 
            elif chance <= 15: self.state = 4 
            elif chance <= 18: self.state = 5 
            else: self.state = 0
        self.root.after(random.randint(3000, 5000), self.update_behavior)

    def animate(self):
        if not self.dragging:
            self.root.attributes('-topmost', True)
            
            # 1. Logic for sitting vs walking
            if self.state == "sitting":
                anim = self.sprites['idle']
                target_y = self.y # Lock to bench Y
            else:
                target_y = self.floor_y # Gravity
                if self.state == 4 and self.x > 0:
                    self.x -= 3
                    anim = self.sprites['walk_l']
                elif self.state == 5 and self.x < (self.screen_w - 100):
                    self.x += 3
                    anim = self.sprites['walk_r']
                else:
                    anim = self.sprites['idle']

            # 2. Cycle Frames
            frames = [f for f in anim if f is not None]
            if frames:
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.label.config(image=frames[self.frame_index])

            self.root.geometry(f"+{int(self.x)}+{int(target_y)}")

        self.root.after(150, self.animate)

    def start_drag(self, e):
        self.dragging = True
        if self.current_bench_slot:
            bench, idx = self.current_bench_slot
            bench.occupants[idx] = None
            self.current_bench_slot = None
            self.state = 0

    def on_drag(self, e):
        self.x, self.y = self.root.winfo_pointerxy()
        self.root.geometry(f"+{self.x-32}+{self.y-32}")

    def stop_drag(self, e):
        self.dragging = False
        found_bench = False
        for b in self.benches:
            idx, slot_x = b.find_free_slot(self.x)
            if idx is not None:
                self.x = slot_x
                self.y = b.y - 45 # Sit on bench
                self.state = "sitting"
                self.current_bench_slot = (b, idx)
                b.occupants[idx] = self
                found_bench = True
                break
        
        if not found_bench:
            self.state = 0
            self.y = self.floor_y

    def open_shop(self): Shop(self.root, self.spawn_bench)
    def open_diary(self): DiaryWindow(self.root)
    def spawn_bench(self):
        b = Bench(self.root, self.x, self.floor_y + 20)
        self.benches.append(b)
        self.root.lift()

if __name__ == "__main__":
    DesktopPet()
