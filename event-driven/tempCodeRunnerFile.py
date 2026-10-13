import tkinter as tk
from tkinter import ttk
import math

class KonverterSuhu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Konverter Suhu - State Management Demo")
        self.window.geometry("500x400")
        self.window.configure(bg="lightblue")

        # Variabel kontrol
        self.celsius_var = tk.DoubleVar()
        self.fahrenheit_var = tk.DoubleVar()
        self.kelvin_var = tk.DoubleVar()
        self.rankine_var = tk.DoubleVar()

        # Flag untuk mencegah infinite loop saat update
        self.updating = False

        self.buat_interface()
        self.setup_traces()

    def buat_interface(self):
        # Judul
        title_label = tk.Label(
            self.window,
            text="KONVERTER SUHU UNIVERSAL",
            font=("Arial", 16, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

        # Frame utama
        main_frame = tk.Frame(self.window, bg="lightblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)