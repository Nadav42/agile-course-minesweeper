import random

# enum
GAME_NOT_FINISHED = 0
GAME_WON = 1 # cleared all mines
GAME_LOST = 2 # clicked a mine

# difficulty
MIN_DIFFICULTY = 0.07
MAX_DIFFICULTY = 0.37

class Cell:

    def __init__(self):

        self.up = None
        self.right = None
        self.down = None
        self.left = None

        self.clicked = False
        self.has_mine = False
        self.has_flag = False

    def get_top_right(self):

        if self.right is not None:
            return self.right.up

        return None

    def get_top_left(self):

        if self.left is not None:
            return self.left.up

        return None

    def get_bottom_right(self):

        if self.right is not None:
            return self.right.down

        return None

    def get_bottom_left(self):

        if self.left is not None:
            return self.left.down

        return None

    def get_all_cells_around(self):
        return [self.up, self.right, self.down, self.left, self.get_top_right(), self.get_top_left(), self.get_bottom_left(), self.get_bottom_right()]

    def get_mines_count_around(self):
        count = 0

        for cell in self.get_all_cells_around():

            if cell is not None and cell.has_mine:
                count = count + 1

        return count

    def click(self):

        if self.clicked:
            return

        self.clicked = True

        # if safe then recursivly click all cells around
        # if not safe then just show this cell as clicked (reveal number)
        if self.get_mines_count_around() == 0:
            for cell in self.get_all_cells_around():
                if cell is not None:
                    cell.click()

    def flag_click(self):
        if not self.clicked:
            self.has_flag = not self.has_flag

    def get_has_mine(self):
        return self.has_mine

    def print_cells_around(self):
        print(self.get_top_left(), self.up, self.get_top_right())
        print(self.left, self, self.right)
        print(self.get_bottom_left(), self.down, self.get_bottom_right())

    def __str__(self):

        if self.clicked:

            if self.has_mine:
                return "M"

            else:
                return str(self.get_mines_count_around())

        if self.has_flag:
            return "F"

        # remove this (print cheats)
        if self.has_mine:
            return "M"

        return "E"

    def to_json(self, reveal_mines=False):

        # {"clicked": ..., "flag": ..., "mine": ..., "adjacentMines": ...}
        json_dic = {"clicked": self.clicked, "flag": self.has_flag}

        if reveal_mines:
            json_dic["mine"] = self.has_mine

        # if clicked
        if self.clicked:

            # only send mine data if mine was clicked
            if self.has_mine:
                json_dic["mine"] = True

            else:
                json_dic["adjacentMines"] = self.get_mines_count_around()

        return json_dic


class Board:

    def __init__(self, rows=9, cols=9, mine_probability=0.13):

        # load the board
        self.reset(rows=rows, cols=cols, mine_probability=mine_probability)

    def reset(self, rows=9, cols=9, mine_probability=0.13):
        self.rows = rows
        self.cols = cols
        self.mine_probability = mine_probability
        self.game_over = GAME_NOT_FINISHED

        # cell objects
        self.cells = [[0 for col in range(self.cols)] for row in range(self.rows)]

        # init cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = Cell()

        # link cells, separated because might not be defined yet.
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].up = self.get_cell(i - 1, j)
                self.cells[i][j].right = self.get_cell(i, j + 1)
                self.cells[i][j].down = self.get_cell(i + 1, j)
                self.cells[i][j].left = self.get_cell(i, j - 1)

        # init mines
        self.place_mines()

    def get_cell(self, row, col):

        if row < 0 or row >= self.rows:
            return None

        if col < 0 or col >= self.cols:
            return None

        return self.cells[row][col]

    def click(self, row, col):

        if self.get_game_status() != GAME_NOT_FINISHED:
            return

        cell = self.get_cell(row, col)

        if cell is not None:

            # block clicks on flagged cells
            if cell.has_flag:
                return

            if cell.get_has_mine():
                self.finish_game(mine=True)

            else:
                cell.click()
                self.check_win()

    def flag_click(self, row, col):

        if self.get_game_status() != GAME_NOT_FINISHED:
            return

        cell = self.get_cell(row, col)

        if cell is not None:
            cell.flag_click()
            self.check_win()

    def check_win(self):
        won = True

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                if not cell.clicked and not cell.has_mine:
                    won = False

                if cell.has_mine and cell.clicked:
                    won = False

        if won:
            self.finish_game(won=True)

        return won

    def place_mines(self):
        total_cells = self.rows * self.cols
        mines_to_place = int(total_cells * self.mine_probability)

        current_mines = 0

        while current_mines < mines_to_place:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            self.get_cell(row, col).has_mine = True

            current_mines = current_mines + 1

        print("\nplaced {} mines on board\n".format(current_mines))

    def finish_game(self, mine=False, won=False):

        if mine:
            self.game_over = GAME_LOST
            print("game over! you lose")

        if won:
            self.game_over = GAME_WON
            print("you win!")

    def get_game_status(self):
        return self.game_over

    def get_difficulty(self):
        return self.mine_probability

    def __str__(self):
        board_str = ""

        for i in range(self.rows):
            row_str = ""

            for j in range(self.cols):
                row_str = "{}{} ".format(row_str, self.cells[i][j])

            board_str = "{}{}\n".format(board_str, row_str)

        return board_str

    def to_json(self):
        cells = [[0 for col in range(self.cols)] for row in range(self.rows)]

        reveal_mines = False

        if self.get_game_status() == GAME_LOST or self.get_game_status() == GAME_WON:
            reveal_mines = True

        for i in range(self.rows):
            for j in range(self.cols):
                cells[i][j] = self.cells[i][j].to_json(reveal_mines=reveal_mines)

        return cells



if __name__ == '__main__':

    board = Board(rows=5, cols=5)

    while board.get_game_status() == GAME_NOT_FINISHED:
        print(board)

        input_str = input()
        row = int(input_str[0])
        col = int(input_str[2])

        if input_str[1].lower() == 'f':
            board.flag_click(row, col)
        else:
            board.click(row, col)

        print(board.to_json())

    # board.cells[0][3].has_mine = True
    # board.click(0, 0)
    # board.click(0, 4)
    # board.flag_click(0, 3)

    #board.cells[0][0].print_cells_around()