import tkinter as tk
import time
import random
from random import randint
import PyQt5 as qt

black = '#000000'
transparentcolor = '#00ffff'

tk.Menu().add_command(label="Exit", command=tk._exit)
tk.Menu().add_command(label="Settings", command=tk.OptionMenu, font=("Times New Roman", 16))



pet = tk.Tk()
pet.config(highlightbackground=black)
pet.overrideredirect(True) # Remove borders
pet.attributes('-topmost', True) # Always on top
pet.wm_attributes('-transparentcolor', transparentcolor) # Transparent background

# Load pet sprite (must have transparent background)
label = tk.Label(pet, bd=0, bg=black)
# Example: img = tk.PhotoImage(file='pet.gif', format='gif -index %i' % frame)
label.pack()
pet.mainloop()

idle_num =[]#idle frames

def decorate(func):
    print("Decorating...")
