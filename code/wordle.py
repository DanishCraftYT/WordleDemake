from wordleCode import WordleGame, tk

class Wordle():
    wordle_game = None
    main_menu = None
    game_modes_lb = None
    def __init__(self): # initializes a lot of stuff.
        # Main Menu Setup #
        self.main_menu = tk.Tk()
        self.main_menu.title("Wordle!")
        self.main_menu.geometry("200x200")

        tk.Label(self.main_menu, text="Wordle!").pack()
        tk.Button(self.main_menu, text="Play", command=self.play_wordle).pack()
        tk.Label(self.main_menu, text="Game Modes (default: Normal):").pack()
        self.game_modes_lb = tk.Listbox(self.main_menu, height=3)
        self.game_modes_lb.insert(0, "Normal")
        self.game_modes_lb.insert(1, "Speed")
        self.game_modes_lb.insert(2, "Hard")
        self.game_modes_lb.pack()
        tk.Button(self.main_menu, text="Quit", command=self.quit_wordle).pack()
        
        self.main_menu.mainloop()

    def play_wordle(self) -> None: # play wordle main menu.
        self.wordle_game = WordleGame(self.main_menu, self.game_modes_lb)

    def quit_wordle(self) -> None: # quit wordle main menu.
        self.main_menu.quit()


if __name__ == "__main__":
    wordle = Wordle()
