import tkinter as tk
from tkinter import ttk
import sv_ttk
from screens.HomeScreen.home_screen import HomeScreen
from screens.SettingsScreen.settings_screen import SettingsScreen
from screens.AboutScreen.about_screen import AboutScreen

# Main application window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Custon Cliper")
        self.geometry("800x600")
        self.config(bg="white")

        # Apply modern theme colors
        self.configure_styles()

        # Create a Notebook widget (for tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Add tabs/screens
        home_screen = HomeScreen(notebook)
        settings_screen = SettingsScreen(notebook)
        about_screen = AboutScreen(notebook)

        notebook.add(home_screen, text="Home")
        notebook.add(settings_screen, text="Settings")
        notebook.add(about_screen, text="About")

    def configure_styles(self):
        style = ttk.Style()

        # Define the main theme
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black", font=("JetBrains Mono", 14))

        # Tab styles
        style.configure("TNotebook.Tab", padding=[10, 5], font=("JetBrains Mono", 12))
        style.map("TNotebook.Tab", background=[("selected", "#add8e6")], foreground=[("selected", "black")])

if __name__ == "__main__":
    app = MainWindow()
    sv_ttk.set_theme("dark")  # Apply a modern theme
    app.mainloop()