import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import hashlib

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.configure(bg='black')
        self.set_window_position(480, 270)  # Set window size and center it
        self.games = []
        self.data_file = "games.json"
        self.pin_hash = "202cb962ac59075b964b07152d234b70"  # md5 for '123'

        self.pin_entry = tk.Entry(self.root, show='*', justify='center', font=('Arial', 24))
        self.pin_entry.pack(pady=20)
        self.pin_entry.focus()
        self.pin_entry.bind('<KeyRelease>', self.check_pin)
        self.ui_initialized = False  # Flag to prevent multiple UI setups

    def set_window_position(self, width, height):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position x, y to center the window
        position_x = (screen_width // 2) - (width // 2)
        position_y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")

    def check_pin(self, event):
        pin = self.pin_entry.get()
        if len(pin) == 3:
            if self.hash_pin(pin) == self.pin_hash:
                self.pin_entry.pack_forget()  # Remove the PIN entry
                if not self.ui_initialized:
                    self.load_games()
                    self.setup_ui()
                    self.ui_initialized = True  # Set the flag to prevent multiple UI setups
            else:
                messagebox.showerror("Error", "Incorrect PIN")
                self.pin_entry.delete(0, 'end')

    def hash_pin(self, pin):
        return hashlib.md5(pin.encode()).hexdigest()

    def setup_ui(self):
        self.add_game_button = tk.Button(self.root, text="Add Game", command=self.add_game, bg='gray', fg='white')
        self.add_game_button.pack(pady=10)

        self.game_list_frame = tk.Frame(self.root, bg='black')
        self.game_list_frame.pack(pady=10)
        self.refresh_game_list()

    def add_game(self):
        game_path = filedialog.askopenfilename(title="Select Game Executable")
        if game_path:
            game_name = os.path.splitext(os.path.basename(game_path))[0]
            self.games.append({"name": game_name, "path": game_path})
            self.save_games()
            self.refresh_game_list()

    def refresh_game_list(self):
        for widget in self.game_list_frame.winfo_children():
            widget.destroy()

        for game in self.games:
            game_button = tk.Button(self.game_list_frame, text=game["name"], command=lambda path=game["path"]: self.launch_game(path), bg='gray', fg='white')
            game_button.pack(pady=5)

    def launch_game(self, path):
        if os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "Game path does not exist")

    def load_games(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.games = json.load(file)

    def save_games(self):
        with open(self.data_file, "w") as file:
            json.dump(self.games, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
