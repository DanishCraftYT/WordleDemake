import tkinter as tk

class WordleGameGUI:
    wordle_game_win: tk.Toplevel = None # contains the wordle game window.
    def __init__(self, root: tk.Tk, title: str, geometry: str):
        self.wordle_game_win = tk.Toplevel(root)
        self.wordle_game_win.title(title)
        self.wordle_game_win.geometry(geometry)
    
    def mainloop(self) -> None:
        self.wordle_game_win.mainloop()
