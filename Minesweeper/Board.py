
class Cell:

    def __init__(self):

        self.up = None
        self.right = None
        self.down = None
        self.left = None

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

    # not tested yet
    def get_mines_count_around(self):
        count = 0

        for cell in self.get_all_cells_around():

            if cell.has_mine:
                count = count + 1

        return count

    def print_cells_around(self):
        print(self.get_top_left(), self.up, self.get_top_right())
        print(self.left, self, self.right)
        print(self.get_bottom_left(), self.down, self.get_bottom_right())

    def __str__(self):
        return "E"

    def to_json(self):
        pass


class Board:

    def __init__(self):

        self.rows = 5
        self.cols = 5

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

    def get_cell(self, row, col):

        if row < 0 or row >= self.rows:
            return None

        if col < 0 or col >= self.cols:
            return None

        return self.cells[row][col]

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

    board = Board()

    print(board)

    print(board.cells[4][4].print_cells_around())