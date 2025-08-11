import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
from screeninfo import get_monitors

class HomeScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text="🏠 Home Screen", font=("JetBrains Mono", 16))
        label.pack(padx=20, pady=10)

        # Dropdown for screen selection
        self.monitors = get_monitors()
        self.selected_screen = tk.IntVar(value=0)
        screen_names = [f"Screen {i+1}: {m.width}x{m.height}" for i, m in enumerate(self.monitors)]
        self.screen_dropdown = ttk.Combobox(self, values=screen_names, state="readonly")
        self.screen_dropdown.current(0)
        self.screen_dropdown.pack(pady=5)
        self.screen_dropdown.bind("<<ComboboxSelected>>", self.change_screen)

        # Canvas for screen mirror
        self.canvas = tk.Label(self)
        self.canvas.pack(padx=20, pady=10, expand=True)

        # Recording controls
        self.record_button = ttk.Button(self, text="Record", command=self.start_recording)
        self.pause_resume_button = ttk.Button(self, text="Pause", command=self.pause_resume_recording)
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_recording)
        self.record_button.pack(pady=10)
        self.pause_resume_button.pack_forget()
        self.stop_button.pack_forget()
        self.is_paused = False

        self.update_screen()

    def start_recording(self):
        self.record_button.pack_forget()
        self.pause_resume_button.config(text="Pause")
        self.pause_resume_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.is_paused = False

    def pause_resume_recording(self):
        if not self.is_paused:
            self.pause_resume_button.config(text="Resume")
            self.is_paused = True
        else:
            self.pause_resume_button.config(text="Pause")
            self.is_paused = False

    def stop_recording(self):
        self.pause_resume_button.pack_forget()
        self.stop_button.pack_forget()
        self.record_button.pack(pady=10)
        self.is_paused = False

    def change_screen(self, event=None):
        self.selected_screen.set(self.screen_dropdown.current())
        self.update_screen()

    def update_screen(self):
        monitor = self.monitors[self.selected_screen.get()]
        bbox = (monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height)
        screenshot = ImageGrab.grab(bbox)
        screenshot = screenshot.resize((800, 500))  # Resize for display
        self.photo = ImageTk.PhotoImage(screenshot)
        self.canvas.config(image=self.photo)
        self.after(150, self.update_screen)  # Refresh every 150ms