import tkinter as tk
from functools import partial

class KeyboardTK:
    buttons = None # contains the keyboard key buttons.
    def __init__(self, gameWin: tk.Tk, callback: callable):
        self.gameWin = gameWin
        self.buttons = {} # {<key letter>, <buttons>}.

        # keyboard #
        key_pos = [50, 225] # contains the position of the keys.
        keyrow_increment = 30 # how much space there should be between each key row.
        key_increment = 30 # how much space there should be between each key.

        for letter in "qwertyuiop": # handles the first row of keys.
            self.buttons[letter] = tk.Button(gameWin, text=letter, command=partial(callback, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue
        
        key_pos = [50, key_pos[1]+keyrow_increment]

        for letter in "asdfghjkl": # handles the second row of keys.
            self.buttons[letter] = tk.Button(gameWin, text=letter, command=partial(callback, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue

        tk.Button(gameWin, text="Enter", command=partial(callback, "Enter")).place(x=key_pos[0], y=key_pos[1])
        tk.Button(gameWin, text="Backspace", command=partial(callback, "Backspace")).place(x=50, y=key_pos[1]+keyrow_increment)

        key_pos = [125, key_pos[1]+keyrow_increment]

        for letter in "zxcvbnm": # handles the third row of keys.
            self.buttons[letter] = tk.Button(gameWin, text=letter, command=partial(callback, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue
    
    def set_key_bg_color(self, key: str, bg_color: str) -> bool: # changes the background color of the specified key.
        if key in self.buttons:
            self.buttons[key].configure(bg=bg_color)
            return True
        return False
    
    def get_key_bg_color(self, key: str) -> str:
        return self.buttons[key].cget("bg")
