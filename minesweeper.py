import random as r


class Cell():
    def __init__(self, _type: str, _open: bool, flag: bool, bomb_around: int = 0):
        self.type = _type
        self.open = _open
        self.flagged = flag
        self.bomb_around = bomb_around

    def open_cell(self):
        self.open = True

    def close_cell(self):
        self.open = False


class Board():

    def __init__(self, width, height, bombs=5):
        self.width = width
        self.height = height
        self.board = []
        self.bombs = bombs
        self.bomb_coords = []
        self.__init_bomb()
        self.__init_board()  # init board
        self.flag = self.__cal_num_flag()
        self.game_over = False
        self.win = False

    def get_flag_left(self):
        return self.flag

    def is_win(self) -> bool:
        return self.__get_safe_left() == 0

    def is_over(self) -> bool:
        return self.game_over

    def __get_safe_left(self) -> int:
        safe_left = 0
        for i in range(self.height):
            for j in range(self.height):
                cell = self.board[i][j]
                if cell.type == "safe" and cell.open == False:
                    safe_left += 1
        return safe_left

    def print_board(self, reveal=False):
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                c = self.board[i][j]
                if not reveal:
                    if not c.open:
                        row += "x  "
                    elif c.open:
                        if c.type == "bomb":
                            row += "B  "
                        elif c.type == "safe":
                            row += str(c.bomb_around)+"  "
                else:
                    if c.type == "bomb":
                        row += "B  "
                    elif c.type == "safe":
                        row += str(c.bomb_around)+"  "
            print(row)

    def on_board_click(self, x, y, is_flag: bool = False) -> bool:
        if not is_flag and self.flag > 0 and not self.game_over and not self.win:
            if self.board[x][y].open == True:
                return False

            if self.board[x][y].type == "bomb":
                self.board[x][y].open_cell()  # open the cell
                self.game_over = True
                return self.game_over
            elif self.board[x][y].type == "safe" and self.board[x][y].bomb_around > 0:
                self.board[x][y].open_cell()  # open the cell
            else:  # case hit empty
                self.board[x][y].open_cell()  # open the cell
                to_expands = self.__find_adjacents(x, y)
                while len(to_expands) > 0:
                    coord = to_expands.pop(0)
                    x, y = coord
                    if self.board[x][y].type == "bomb" or self.board[x][y].open == True:
                        continue
                    else:
                        if self.board[x][y].bomb_around == 0:
                            self.board[x][y].open_cell()  # open the cell
                            adjacents = self.__find_adjacents(x, y)
                            to_expands += adjacents
                        else:
                            self.board[x][y].open_cell()  # open the cell

            __safe_left = self.__get_safe_left()
            if __safe_left == 0:
                self.win = True
                self.game_over = True
            return False
        else:
            if not self.game_over:
                if self.flag > 0 and not self.board[x][y].open:
                    self.flag -= 1
                    self.board[x][y].open_cell()  # open the cell
                    self.board[x][y].flagged = True
            return False

    def __cal_num_flag(self) -> int:
        return int((self.height * self.width) * 0.12)

    def __init_bomb(self):
        bomb_remain = self.bombs
        alls = [[(i, j) for j in range(self.width)]
                for i in range(self.height)]
        coords = []
        for c in alls:
            coords += c
        while bomb_remain > 0:
            coord = r.choice(coords)
            coords.pop(coords.index(coord))
            x, y = coord
            if (x, y) not in self.bomb_coords:
                self.bomb_coords.append((x, y))
                bomb_remain -= 1
        print(len(self.bomb_coords), self.bomb_coords)

    def __find_adjacents(self, x, y):
        adjacents = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i >= 0 and y+j >= 0:
                    try:
                        cell = self.board[x+i][y+j]  # try to access cell
                        adjacents.append((x+i, y+j))
                    except IndexError:
                        pass
        return adjacents

    def __count_bomb_around(self):
        for y in range(self.height):
            for x in range(self.width):
                bomb = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if y+i < 0 or x+j < 0:
                            continue
                        try:
                            if self.board[y+i][x+j].type == "bomb":
                                bomb += 1
                        except:
                            pass
                self.board[y][x].bomb_around = bomb

    def __init_board(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                is_bomb = True if (i, j) in self.bomb_coords else False
                _type = "safe" if not is_bomb else "bomb"
                cell = Cell(_type, False, False)
                row.append(cell)
            self.board.append(row)
        self.__count_bomb_around()


if __name__ == "__main__":
    board_size = int(input("Define board size:"))
    print(board_size**2)
    bombs = int(input("Specify number of bomb:"))
    board = Board(board_size, board_size, bombs=bombs)
    board.print_board()  # I ADDED THIS LATER FOR VISUALIZATION
    print("Borad Size:{}".format(board_size))
    print("There are {} bombs".format(board.bombs))
    while not board.game_over:
        try:
            x = int(input("x:"))
            y = int(input("y:"))
            if not board.on_board_click(y, x):
                board.print_board()  # I ADDED THIS LATER FOR VISUALIZATION
            else:
                break
        except:
            pass

    print("*"*100)
    board.print_board(reveal=True)  # I ADDED THIS LATER FOR VISUALIZATION
