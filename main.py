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

# Main application window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Custon Cliper")
        self.geometry("800x600")
        self.config(bg="white")

        self.obs_subprocess_controller = ObsProcessController(
            obs_path="C:/Program Files/obs-studio/bin/64bit/obs64.exe"
        )
        self.obs_subprocess_controller.start_obs()

        self.obs_controller = ObsController(file_store_location="C:/Users/Jabri/Documents/CustomClip/ObsIntegration/")

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

    def on_close(self):
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
    #obs_controller.stop_obs()