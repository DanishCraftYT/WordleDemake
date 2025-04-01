import tkinter as tk
from functools import partial
from randomWord import RandomWord
from threadTimer import ThreadTimer

# IMPORTANT NOTE: USING thread_event.set() WILL NOT RESET THE TIMER IF IT HAS ENDED.

class WordleGame():
    # Words #
    wordle_word = "" # the word the user has to guess.
    user_word = "" # the word the user has guessed.

    # TK Stuff #
    wordle_word_label = None # the label that is displayed when the game is over. it displays the word the player had to guess.
    wordle_game_win = None # contains the Wordle Game Window.
    err_label = None # error label in case Wordle throws a error.
    restart_btn = None # restart button.
    buttons = None # contains the keyboard key buttons.
    guess_labels = None # contains the labels that display the words the user uses to guess with.

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
        # sets the default value for the buttons & guess_labels here to avoid the instances of this class from sharing the same instance of these varibles.
        self.buttons = {} # {<key letter>, <buttons>}.
        self.guess_labels = [[], [], [], [], [], []] # [[<row 1>], [<row 2>], [<row 3>], [<row 4>], [<row 5>], [<row 6>]].

        # sets Wordle Game Mode #
        if game_modes_lb.curselection(): # checks if user selected a mode.
            self.game_mode = game_modes_lb.get(game_modes_lb.curselection()[0])

        # gets wordle word #
        self.wordle_word = RandomWord.get_word()
        if self.wordle_word == "":
            raise Exception("couldn't get random word for Wordle!")

        # Wordle Setup #
        self.wordle_game_win = tk.Toplevel(main_menu)
        self.wordle_game_win.title("Wordle Game!")
        self.wordle_game_win.geometry("400x400")

        if self.game_mode == "Speed":
            def on_wordle_win_destroyed():
                self.round = 5 # round has to be equal to 5 to stop the timer.
                self.timer.thread_event.set() # stops timer.
                self.wordle_game_win.destroy()
            self.wordle_game_win.protocol("WM_DELETE_WINDOW", on_wordle_win_destroyed)

        # guess labels #
        text_pos = [130, 30]
        text_increment = 30
        textrow_increment = 30
        for i in range(0, 6): # loops through each row.
            for j in range(0, 5): # loops through each column.
                self.guess_labels[i].append(tk.Label(self.wordle_game_win, text="#"))
                self.guess_labels[i][j].place(x=text_pos[0], y=text_pos[1])
                text_pos[0] += text_increment
                continue
            text_pos[0] = 130
            text_pos[1] += textrow_increment
            continue
        
        # keyboard #
        key_pos = [50, 225] # contains the position of the keys.
        keyrow_increment = 30 # how much space there should be between each key row.
        key_increment = 30 # how much space there should be between each key.

        for letter in "qwertyuiop": # handles the first row of keys.
            self.buttons[letter] = tk.Button(self.wordle_game_win, text=letter, command=partial(self.key_pressed, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue
        
        key_pos = [50, key_pos[1]+keyrow_increment]

        for letter in "asdfghjkl": # handles the second row of keys.
            self.buttons[letter] = tk.Button(self.wordle_game_win, text=letter, command=partial(self.key_pressed, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue

        tk.Button(self.wordle_game_win, text="Enter", command=partial(self.key_pressed, "Enter")).place(x=key_pos[0], y=key_pos[1])
        tk.Button(self.wordle_game_win, text="Backspace", command=partial(self.key_pressed, "Backspace")).place(x=50, y=key_pos[1]+keyrow_increment)

        key_pos = [125, key_pos[1]+keyrow_increment]

        for letter in "zxcvbnm": # handles the third row of keys.
            self.buttons[letter] = tk.Button(self.wordle_game_win, text=letter, command=partial(self.key_pressed, letter))
            self.buttons[letter].place(x=key_pos[0], y=key_pos[1])
            key_pos[0] += key_increment
            continue

        # err_label #
        self.err_label = tk.Label(self.wordle_game_win)
        self.err_label.place(x=115, y=5)

        # restart button #
        self.restart_btn = tk.Button(self.wordle_game_win, text="Restart!", command=self.restart)
        self.restart_btn.place(x=160, y=325)

        # wordle_word_label #
        self.wordle_word_label = tk.Label(self.wordle_game_win)
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
                self.guess_labels[self.round][self.guess_labels_col].configure(text="#")
        else: # handles all other keys.
            if len(self.user_word) != 5 and not self.disable_typing:
                self.user_word += key
                self.guess_labels[self.round][self.guess_labels_col].configure(text=key)
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
                self.buttons[letter[0]].configure(bg="#00FF04")
                self.guess_labels[self.round][i].configure(bg="#00FF04")
                if self.game_mode == "Hard":
                    self.correct_letters += letter[0]
            elif letter[0] in self.wordle_word: # yellow words.
                if self.buttons[letter[0]]["background"] != "#00FF04":
                    self.buttons[letter[0]].configure(bg="#FFCF33")
                    if self.game_mode == "Hard":
                        self.correct_letters += letter[0]
                self.guess_labels[self.round][i].configure(bg="#FFCF33")
            else: # gray words.
                if self.buttons[letter[0]]["background"] != "#00FF04" and self.buttons[letter[0]]["background"] != "#FFCF33":
                    self.buttons[letter[0]].configure(bg="#71867C")
                self.guess_labels[self.round][i].configure(bg="#71867C")
            continue

    def restart(self) -> None: # restarts Wordle.
        self.round = 0
        self.guess_labels_col = 0
        self.wordle_word = RandomWord.get_word()
        self.user_word = ""
        self.wordle_word_label.configure(text="")
        self.disable_typing = False

        # guess labels #
        for row in range(0, 6): # loops through each row.
            for col in range(0, 5): # loops through each column.
                self.guess_labels[row][col].configure(text="#", bg="#f0f0f0")
                continue
            continue

        # keyboard buttons #
        for button in self.buttons.values():
            button.configure(bg="#f0f0f0")
            continue
        
        # speed mode #
        if self.game_mode == "Speed":
            if self.timer.thread_event.is_set(): # checks if the timer has been destroyed before creating a new one.
                self.timer = ThreadTimer(self.timer_time, self.on_timer_end)
            else:
                self.timer.thread_event.set() # resets the timer.
