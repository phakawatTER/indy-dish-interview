import tkinter as tk
import tkmacosx as tkosx
import sys
from tkinter import messagebox
from minesweeper import Board

platform = sys.platform
if platform == "darwin":
    tk.Button = tkosx.Button


class MineSweeperFrame(tk.Frame):
    WIDTH = 450
    HEIGHT = 450
    """
    LEVEL 1 EASY
    LEVEL 2 MEDIUM
    LEVEL 3 HARD
    """

    def __init__(self, root, side=18, level=1, board: Board = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.side = side  # board size
        self.level = level  # game level
        self.app_name = "Minesweeper!"
        self.cells = []
        self.init_game()
        self.init_minesweeper_frame()

    def init_game(self):
        side = self.side  # size of each side of the board
        bombs = int((side**2)*(0.07*self.level))
        self.board = Board(side, side, bombs=bombs)
        self.board.print_board(reveal=True)

    def on_board_click(self, x, y, **kwargs):
        target = self.board.board[y][x]
        print(target.bomb_around, target.type)
        if self.board.on_board_click(y, x, **kwargs):
            self.reveal_cells(_all=True)  # reveal all cells
            messagebox.showinfo(self.app_name, "Game Over! You hit a bomb!")
        else:
            if self.board.is_win():
                messagebox.showinfo(self.app_name, "You have won the game!")
                self.reveal_cells(_all=True)
            else:
                self.reveal_cells()

    def reveal_cells(self, _all=False):
        for i in range(self.board.height):
            for j in range(self.board.width):
                cell = self.board.board[i][j]
                is_open = cell.open
                is_flagged = cell.flagged
                bomb_around = cell.bomb_around
                cell_type = cell.type
                if _all == False:
                    if is_open and not is_flagged:
                        if cell_type == "safe":
                            self.cells[i][j][0].set(
                                bomb_around if bomb_around > 0 else " ")
                            self.cells[i][j][1].set(
                                "green" if bomb_around > 0 else "yellow")
                        else:
                            self.cells[i][j][0].set("B")
                            self.cells[i][j][1].set(
                                "red")
                    elif is_open and is_flagged:
                        self.cells[i][j][0].set("F")
                        self.cells[i][j][1].set(
                            "orange")
                else:
                    if cell_type == "safe":
                        self.cells[i][j][0].set(
                            bomb_around if bomb_around > 0 else " ")
                        self.cells[i][j][1].set(
                            "green" if bomb_around > 0 else "yellow")
                    else:
                        self.cells[i][j][0].set("B")
                        self.cells[i][j][1].set("red")

    def init_minesweeper_frame(self):
        self.cells = []
        self.minesweeper_frame = tk.Frame(self, width=400)
        self.minesweeper_frame.pack(fill=tk.BOTH)
        for i in range(self.board.height):
            self.cells.append([])
            for j in range(self.board.width):
                _frame = tk.Frame(self.minesweeper_frame, width=20, height=20)
                _frame.propagate(False)
                _frame.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                textvar = tk.StringVar(self, value=" ")  # tk string variable
                colorvar = tk.StringVar(self, value="white")
                button = tk.Button(
                    _frame, bg=colorvar, textvariable=textvar, command=lambda x=i, y=j: self.on_board_click(y, x))
                button.pack(fill=tk.BOTH)
                self.cells[i].append([
                    textvar,
                    colorvar
                ])

    def reset_cells(self):
        for i in range(self.side):
            for j in range(self.side):
                self.cells[i][j][0].set(" ")
                self.cells[i][j][1].set("white")


class MainInterface(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.app_name = "Minesweeper!"
        self.resizable(False, False)
        self.title(self.app_name)
        self.__init_tk_vars()
        self.__init_game_counter_vars()
        self.__create_minesweeper()
        self.__add_header_frame()
        self.mainloop()

    def __init_game_counter_vars(self):
        self.__after_match_click_count = 0

    def __init_tk_vars(self):
        self.side = tk.StringVar(self, value=16, name="size")
        self.side.trace("w", self.__on_option_change)
        self.header = tk.Frame(self)
        self.header.pack(side=tk.TOP)
        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP)
        self.difficulity_choices = {"Easy": 1, "Medium": 2, "Hard": 3}
        self.difficulity = tk.StringVar(
            self, value="Medium", name="difficulity")
        self.difficulity.trace("w", self.__on_option_change)
        self.flags = tk.IntVar(self, value=0)
        self.user_rule = tk.IntVar(self, value=0)
        self.user_suck = tk.IntVar(self, value=0)

    def __create_minesweeper(self):
        try:
            self.MSFrame.destroy()
        except Exception as e:
            pass
        difficulity = self.difficulity_choices[self.difficulity.get()]
        side = int(self.side.get())
        self.MSFrame = MineSweeperFrame(self.mainframe, side, difficulity)
        self.MSFrame.pack()
        on_board_click = self.MSFrame.on_board_click

        def __on_board_click(*args):
            on_board_click(*args, is_flag=self.use_flag)
            win = self.MSFrame.board.is_win()
            print(win)
            game_over = self.MSFrame.board.game_over
            if game_over:
                if self.__after_match_click_count == 0:

                    if win:
                        print("YOU FUCKING WIN THE GAME")
                        curr = self.user_rule.get()
                        self.user_rule.set(curr+1)
                    else:
                        curr = self.user_suck.get()
                        self.user_suck.set(curr+1)
                self.__after_match_click_count += 1
            flag = self.MSFrame.board.get_flag_left()
            self.flags.set(flag)

        self.MSFrame.on_board_click = __on_board_click

    def __on_option_change(self, *args):
        name, _, _ = args
        if name == "size":
            self.__create_minesweeper()  # re-create minesweeper game
        else:
            self.MSFrame.level = self.difficulity_choices[self.difficulity.get(
            )]
            self.__reset()
        self.use_flag = False
        self.flags.set(self.MSFrame.board.get_flag_left())
        self.flag_text.set("Use Flag:False")

    def __add_difficulity_option(self):
        self.diff_select = tk.OptionMenu(
            self.header, self.difficulity, *self.difficulity_choices)
        self.diff_select.pack(side=tk.LEFT)

    def __add_boardsize_option(self):
        boardsizes = {16, 24, 32}
        self.boardsize_option = tk.OptionMenu(
            self.header, self.side, *boardsizes)
        self.boardsize_option.pack(side=tk.LEFT)

    def __add_flag(self):
        _flag = self.MSFrame.board.get_flag_left()
        self.flags.set(_flag)
        self.use_flag = False
        self.flag_text = tk.StringVar()
        self.flag_text.set("Use Flag:False")
        frame = tk.Frame(self.header)
        frame.pack(side=tk.LEFT)

        def toggle_flag():
            self.use_flag = not self.use_flag
            self.flag_text.set(
                "Use Flag:True" if self.use_flag else "Use Flag:False")
        tk.Label(frame, textvariable=self.flag_text).pack(side=tk.TOP)
        tk.Label(frame, textvariable=self.flags).pack(side=tk.LEFT)
        tk.Button(frame, text="On/Off",
                  command=toggle_flag).pack(side=tk.RIGHT)

    def __reset(self):
        self.MSFrame.reset_cells()
        self.MSFrame.init_game()  # reinit game
        self.__init_game_counter_vars()
        self.flags.set(self.MSFrame.board.flag)

    def __add_reset_button(self):

        tk.Button(self.header, text="Restart Game",
                  command=self.__reset).pack(side=tk.LEFT)

    def __add_user_stat(self):
        frame = tk.Frame(self.header)
        frame.pack(side=tk.BOTTOM)
        tk.Button(frame, text="Restart Game",
                  command=self.__reset).pack(side=tk.TOP)
        tk.Label(frame, text="You rule ").pack(side=tk.LEFT)
        tk.Label(frame, textvariable=self.user_rule).pack(side=tk.LEFT)
        tk.Label(frame, text="You suck ").pack(side=tk.LEFT)
        tk.Label(frame, textvariable=self.user_suck).pack(side=tk.LEFT)

    def __add_header_frame(self):
        self.__add_difficulity_option()  # add difficulity options to the frame
        self.__add_boardsize_option()  # board size option
        self.__add_flag()
        # self.__add_reset_button()
        self.__add_user_stat()
