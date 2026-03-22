import tkinter as tk
from data_manager import DataManager

class Shop:
    def __init__(self, parent, buy_bench_cb):
        self.win = tk.Toplevel(parent)
        self.win.title("Shop")
        self.win.geometry("250x150")
        self.buy_bench_cb = buy_bench_cb
        
        self.data = DataManager.load_data()
        self.coin_label = tk.Label(self.win, text=f"Coins: {self.data['coins']}")
        self.coin_label.pack(pady=10)
        
        tk.Button(self.win, text="Buy Bench (50c)", command=self.buy_item).pack()

    def buy_item(self):
        if self.data['coins'] >= 50:
            self.data['coins'] -= 50
            DataManager.save_data(self.data)
            self.coin_label.config(text=f"Coins: {self.data['coins']}")
            self.buy_bench_cb()
