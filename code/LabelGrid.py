import tkinter as tk

class LabelGrid:
    labels = None # contains the labels that display the words the user uses to guess with.
    def __init__(self, wordle_game_win: tk.Toplevel) -> None:
        self.labels = [[], [], [], [], [], []] # [[<row 1>], [<row 2>], [<row 3>], [<row 4>], [<row 5>], [<row 6>]].

        text_pos = [130, 30]
        text_increment = 30
        textrow_increment = 30
        for i in range(0, 6): # loops through each row.
            for j in range(0, 5): # loops through each column.
                self.labels[i].append(tk.Label(wordle_game_win, text="#"))
                self.labels[i][j].place(x=text_pos[0], y=text_pos[1])
                text_pos[0] += text_increment
                continue
            text_pos[0] = 130
            text_pos[1] += textrow_increment
            continue
