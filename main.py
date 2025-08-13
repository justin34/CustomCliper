import asyncio
import time
import tkinter as tk
from tkinter import ttk
import sv_ttk
from ObsIntegration.ObsControler import ObsController
from screens.HomeScreen.home_screen import HomeScreen
from screens.SettingsScreen.settings_screen import SettingsScreen
from screens.AboutScreen.about_screen import AboutScreen
from ObsIntegration.ObsSubproccessController import ObsProcessController
import json
import os

class ConnectionForm(tk.Toplevel):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("OBS Connection Setup")
        self.geometry("600x450")
        self.on_submit = on_submit

        # Set background color to match the main window
        self.configure(bg="#1f1f1f")

        # Form fields
        tk.Label(self, text="Host:", bg="#8cdcfe", font=("JetBrains Mono", 12)).pack(pady=5)
        self.host_entry = tk.Entry(self, relief="flat", font=("JetBrains Mono", 12))
        self.host_entry.pack(pady=5, ipady=5, ipadx=5)
        self.host_entry.configure(highlightbackground="black", highlightthickness=1, bd=0)

        tk.Label(self, text="Port:", bg="#8cdcfe", font=("JetBrains Mono", 12)).pack(pady=5)
        self.port_entry = tk.Entry(self, relief="flat", font=("JetBrains Mono", 12))
        self.port_entry.pack(pady=5, ipady=5, ipadx=5)
        self.port_entry.configure(highlightbackground="black", highlightthickness=1, bd=0)

        tk.Label(self, text="Password:", bg="#8cdcfe", font=("JetBrains Mono", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", relief="flat", font=("JetBrains Mono", 12))
        self.password_entry.pack(pady=5, ipady=5, ipadx=5)
        self.password_entry.configure(highlightbackground="black", highlightthickness=1, bd=0)

        tk.Label(self, text="Monitor ID:", bg="#8cdcfe", font=("JetBrains Mono", 12)).pack(pady=5)
        self.monitor_id_entry = tk.Entry(self, relief="flat", font=("JetBrains Mono", 12))
        self.monitor_id_entry.pack(pady=5, ipady=5, ipadx=5)
        self.monitor_id_entry.configure(highlightbackground="black", highlightthickness=1, bd=0)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.submit, relief="flat", font=("JetBrains Mono", 12))
        submit_button.pack(pady=10, ipady=5, ipadx=10)
        submit_button.configure(bg="#add8e6", fg="black", activebackground="#87ceeb", activeforeground="white", bd=0)

    def submit(self):
        # Collect form data
        connection_info = {
            "host": self.host_entry.get(),
            "port": int(self.port_entry.get()),
            "password": self.password_entry.get(),
            "monitor_id": self.monitor_id_entry.get()
        }
        self.on_submit(connection_info)
        self.destroy()

# Main application window
class MainWindow(tk.Tk):
    CACHE_FILE = "obs_connection_cache.json"

    def __init__(self):
        super().__init__()

        self.title("Custon Cliper")
        self.geometry("1200x900")
        self.config(bg="white")

        # Load OBS connection info from cache
        self.obs_connection_info = self.load_cache()
        print(f"Loaded OBS connection info: {self.obs_connection_info}")

        if not self.obs_connection_info:
            # Show connection form if cache is empty
            self.wait_for_connection_form()

        self.obs_subprocess_controller = ObsProcessController(
            obs_path="C:/Program Files/obs-studio/bin/64bit/obs64.exe"
        )
        self.obs_subprocess_controller.start_obs()

        self.obs_controller = ObsController(
            file_store_location="C:/Users/Jabri/Documents/CustomClip/ObsIntegration/",
            host=self.obs_connection_info["host"],
            port=self.obs_connection_info["port"],
            password=self.obs_connection_info["password"],
            monitor_id=self.obs_connection_info["monitor_id"]
        )

        # Apply modern theme colors
        self.configure_styles()

        # Create a Notebook widget (for tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Add tabs/screens
        home_screen = HomeScreen(notebook, obs_controller=self.obs_controller)
        settings_screen = SettingsScreen(notebook)
        about_screen = AboutScreen(notebook)

        notebook.add(home_screen, text="Home")
        notebook.add(settings_screen, text="Settings")
        notebook.add(about_screen, text="About")

        # Bind the close event to stop OBS
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        style = ttk.Style()

        # Define the main theme
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black", font=("JetBrains Mono", 14))

        # Tab styles
        style.configure("TNotebook.Tab", padding=[10, 5], font=("JetBrains Mono", 12))
        style.map("TNotebook.Tab", background=[("selected", "#add8e6")], foreground=[("selected", "black")])

    def load_cache(self):
        """Load OBS connection info from a local cache file."""
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Cache file is corrupted. Using default values.")
        return {}

    def save_cache(self):
        """Save OBS connection info to a local cache file."""
        with open(self.CACHE_FILE, "w") as f:
            json.dump(self.obs_connection_info, f)

    def wait_for_connection_form(self):
        """Show the connection form and wait for user input."""
        def on_submit(connection_info):
            self.obs_connection_info = connection_info
            self.save_cache()

        form = ConnectionForm(self, on_submit)
        self.wait_window(form)

    def on_close(self):
        # Save OBS connection info to cache
        self.save_cache()

        # Stop OBS when the app closes
        print("Closing application...")
        self.obs_controller.stopReplayBuffer()
        self.obs_controller.disconnect()
        time.sleep(2)
        self.obs_subprocess_controller.stop_obs()
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    sv_ttk.set_theme("dark")  # Apply a modern theme
    app.mainloop()