import tkinter as tk
from tkinter import ttk

class AboutScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text="ℹ️ About Screen", font=("JetBrains Mono", 16))
        label.pack(padx=20, pady=20, expand=True)