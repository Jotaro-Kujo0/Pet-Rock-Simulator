import json, os, sys
import tkinter as tk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DataManager:
    FILE = "pet_save.json"

    @staticmethod
    def load_data():
        if not os.path.exists(DataManager.FILE):
            return {"coins": 100, "inventory": [], "pet_name": "Ket", "bio": "A very sturdy friend."}
        with open(DataManager.FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data):
        with open(DataManager.FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def safe_load(path):
        full_path = resource_path(path)
        if os.path.exists(full_path):
            try:
                img = tk.PhotoImage(file=full_path)
                return img
            except: return None
        return None
