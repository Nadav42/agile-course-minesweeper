import random

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

        # remove this
        if self.has_mine:
            return "M"

        return "E"

    def to_json(self):
        pass


class Board:

    def __init__(self, rows=9, cols=9):

        self.rows = rows
        self.cols = cols

        self.game_over = False
        self.mine_probability = 0.13 # this is the difficulty

        self.cells = [[0 for col in range(self.cols)] for row in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = Cell()

        # separated because might not be defined yet
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].up = self.get_cell(i - 1, j)
                self.cells[i][j].right = self.get_cell(i, j + 1)
                self.cells[i][j].down = self.get_cell(i + 1, j)
                self.cells[i][j].left = self.get_cell(i, j - 1)

        self.place_mines()

    def get_cell(self, row, col):

        if row < 0 or row >= self.rows:
            return None

        if col < 0 or col >= self.cols:
            return None

        return self.cells[row][col]

    def click(self, row, col):

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

                if cell.has_mine and not cell.has_flag:
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
        self.game_over = True

        if mine:
            print("game over! you lose")

        if won:
            print("you win!")

    def is_game_over(self):
        return self.game_over

    def __str__(self):
        board_str = ""

        for i in range(self.rows):
            row_str = ""

            for j in range(self.cols):
                row_str = "{}{} ".format(row_str, self.cells[i][j])

            board_str = "{}{}\n".format(board_str, row_str)

        return board_str

    def to_json(self):
        pass


if __name__ == '__main__':

    board = Board(rows=5, cols=5)

    while not board.is_game_over():
        print(board)

        input_str = input()
        row = int(input_str[0])
        col = int(input_str[2])

        if input_str[1].lower() == 'f':
            board.flag_click(row, col)
        else:
            board.click(row, col)

    # board.cells[0][3].has_mine = True
    # board.click(0, 0)
    # board.click(0, 4)
    # board.flag_click(0, 3)

    #board.cells[0][0].print_cells_around()