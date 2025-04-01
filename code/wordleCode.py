import tkinter as tk
from keyboardTK import KeyboardTK
from WordleGameGUI import WordleGameGUI
from LabelGrid import LabelGrid
from randomWord import RandomWord
from threadTimer import ThreadTimer

# IMPORTANT NOTE: USING thread_event.set() WILL NOT RESET THE TIMER IF IT HAS ENDED.

class WordleGame:
    # Words #
    wordle_word = "" # the word the user has to guess.
    user_word = "" # the word the user has guessed.
    random_word = None # contains the RandomWord class.

    # Tkinter Keyboard #
    keyboard_tk = None # contains the KeyboardTK class.

    # Wordle Game Window #
    wordle_game_win = None # contains the WordleGameGUI class.

    # guess labels #
    label_grid = None # contains the LabelGrid class.

    # TK Stuff #
    wordle_word_label = None # the label that is displayed when the game is over. it displays the word the player had to guess.
    err_label = None # error label in case Wordle throws a error.
    restart_btn = None # restart button.

    # counters #
    guess_labels_col = 0 # determines what guess label column we are editing.
    round = 0 # determines what round we are on. it goes from 0 - 5. also used to determine what guess label row we are editing.

    # Game Mode #
    game_mode = "Normal" # determines the game mode for Wordle.

    # Speed Mode #
    timer = None # contains the threadTimer class.
    timer_time = 10 # the amount of time that passes before the timer callback is called.
    disable_typing = False # disables typing after timer has ended until the game is restarted.

    # hard mode #
    correct_letters = "" # contains yellow & green letters.
    def __init__(self, main_menu : tk.Tk, game_modes_lb : tk.Listbox):
        # sets Wordle Game Mode #
        if game_modes_lb.curselection(): # checks if user selected a mode.
            self.game_mode = game_modes_lb.get(game_modes_lb.curselection()[0])

        # gets wordle word #
        self.random_word = RandomWord() # creates instance of RandomWord class.
        self.wordle_word = self.random_word.get_word() # gets a random 5 letter word.
        if self.wordle_word == "":
            raise Exception("couldn't get random word for Wordle!")

        # Wordle Setup #
        self.wordle_game_win = WordleGameGUI(main_menu, "Wordle Game!", "400x400") # creates instance of WordleGameGUI class.

        if self.game_mode == "Speed":
            def on_wordle_win_destroyed():
                self.round = 5 # round has to be equal to 5 to stop the timer.
                self.timer.thread_event.set() # stops timer.
                self.wordle_game_win.wordle_game_win.destroy()
            self.wordle_game_win.wordle_game_win.protocol("WM_DELETE_WINDOW", on_wordle_win_destroyed)

        # guess labels #
        self.label_grid = LabelGrid(self.wordle_game_win.wordle_game_win) # creates instance of LabelGrid class.
        
        self.keyboard_tk = KeyboardTK(self.wordle_game_win.wordle_game_win, self.key_pressed)

        # err_label #
        self.err_label = tk.Label(self.wordle_game_win.wordle_game_win)
        self.err_label.place(x=115, y=5)

        # restart button #
        self.restart_btn = tk.Button(self.wordle_game_win.wordle_game_win, text="Restart!", command=self.restart)
        self.restart_btn.place(x=160, y=325)

        # wordle_word_label #
        self.wordle_word_label = tk.Label(self.wordle_game_win.wordle_game_win)
        self.wordle_word_label.place(x=130, y=360)

        # handles game modes #
        if self.game_mode == "Speed":
            self.timer = ThreadTimer(self.timer_time, self.on_timer_end)

        # main loop #
        self.wordle_game_win.mainloop()

    def key_pressed(self, key) -> None: # handles key presses.
        self.err_label.configure(text="") # removes any errors Wordle may have thrown.

        if key == "Enter": # handles the Enter key.
            if len(self.user_word) == 5:
                if self.game_mode == "Hard":
                    for letter in self.correct_letters:
                        if letter not in self.user_word:
                            self.err_label.configure(text=f"{letter} is not in the guessed word")
                            return None
                        continue
                if self.round == 5 or self.check_user_word():
                    self.timer.thread_event.set() # destroys the timer.
                    self.color_stuff()
                    self.wordle_word_label.configure(text=f"Correct Word: {self.wordle_word}")
                else:
                    self.new_round()
            else:
                self.err_label.configure(text="please provide a 5 letter word!")
        elif key == "Backspace": # handles the Backspace key.
            if len(self.user_word) != 0:
                self.user_word = self.user_word[:-1]
                self.guess_labels_col -= 1
                self.label_grid.labels[self.round][self.guess_labels_col].configure(text="#")
        else: # handles all other keys.
            if len(self.user_word) != 5 and not self.disable_typing:
                self.user_word += key
                self.label_grid.labels[self.round][self.guess_labels_col].configure(text=key)
                self.guess_labels_col += 1

    def on_timer_end(self, exit_flag : int=0) -> None: # ThreadTimer callback.
        if exit_flag == -1:
            if self.round != 6:
                self.timer = ThreadTimer(self.timer_time, self.on_timer_end)
            return None
        elif self.round == 5:
            self.color_stuff()
            self.wordle_word_label.configure(text=f"Correct Word: {self.wordle_word}")
            self.disable_typing = True
        else:
            self.timer.thread_event.set() # sets event so the new_round() function knows to create a new timer.
            self.new_round()

    def check_user_word(self) -> bool: # checks if the user word is valid.
        if self.user_word == self.wordle_word:
            return True
        return False
    
    def new_round(self) -> None: # starts a new round.
        self.color_stuff()
        self.round += 1
        self.guess_labels_col = 0
        self.user_word = ""
        if self.game_mode == "Speed":
            if self.timer.thread_event.is_set(): # checks if the timer has been destroyed before creating a new one.
                self.timer = ThreadTimer(self.timer_time, self.on_timer_end)
            else:
                self.timer.thread_event.set() # resets the timer.

    def color_stuff(self) -> None: # colors keyboard buttons & guess labels.
        for i, letter in enumerate(zip(self.user_word, self.wordle_word)):
            if letter[0] == letter[1]: # green words.
                self.keyboard_tk.set_key_bg_color(letter[0], "#00FF04")
                self.label_grid.labels[self.round][i].configure(bg="#00FF04")
                if self.game_mode == "Hard":
                    self.correct_letters += letter[0]
            elif letter[0] in self.wordle_word: # yellow words.
                if self.keyboard_tk.get_key_bg_color(letter[0]) != "#00FF04":
                    self.keyboard_tk.set_key_bg_color(letter[0], "#FFCF33")
                    if self.game_mode == "Hard":
                        self.correct_letters += letter[0]
                self.label_grid.labels[self.round][i].configure(bg="#FFCF33")
            else: # gray words.
                if self.keyboard_tk.get_key_bg_color(letter[0]) != "#00FF04" and self.keyboard_tk.get_key_bg_color(letter[0]) != "#FFCF33":
                    self.keyboard_tk.set_key_bg_color(letter[0], "#71867C")
                self.label_grid.labels[self.round][i].configure(bg="#71867C")
            continue

    def restart(self) -> None: # restarts Wordle.
        self.round = 0
        self.guess_labels_col = 0
        self.wordle_word = self.random_word.get_word()
        self.user_word = ""
        self.wordle_word_label.configure(text="")
        self.disable_typing = False

        # guess labels #
        for row in range(0, 6): # loops through each row.
            for col in range(0, 5): # loops through each column.
                self.label_grid.labels[row][col].configure(text="#", bg="#f0f0f0")
                continue
            continue

        # keyboard buttons #
        for key in self.keyboard_tk.buttons.keys():
            self.keyboard_tk.set_key_bg_color(key, "#f0f0f0")
            continue
        
        # speed mode #
        if self.game_mode == "Speed":
            if self.timer.thread_event.is_set(): # checks if the timer has been destroyed before creating a new one.
                self.timer = ThreadTimer(self.timer_time, self.on_timer_end)
            else:
                self.timer.thread_event.set() # resets the timer.
