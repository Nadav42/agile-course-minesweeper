import unittest
import random

from Minesweeper.Board import Board, MIN_DIFFICULTY, MAX_DIFFICULTY, GAME_NOT_FINISHED, GAME_LOST, GAME_WON

class BoardTests(unittest.TestCase):

    def test_first_click(self):
        # check with 10 randoms points
        for i in range(100):
            board = Board() # create new empty board
            board.click(random.randint(0, 6), random.randint(0, 6))

            # game must not be finished because can't click a mine on first turn
            self.assertTrue(board.get_game_status() == GAME_NOT_FINISHED)

    def test_range_difficulty(self):
        board = Board(9, 9)
        difficulty = board.get_difficulty()

        self.assertGreaterEqual(difficulty, MIN_DIFFICULTY)
        self.assertLessEqual(difficulty, MAX_DIFFICULTY)

    def test_check_not_win_empty_board(self):
        board = Board()
        self.assertFalse(board.check_win())

    # if I click on all cells without a mine then I should win
    def test_check_win(self):
        board = Board()

        # must do first click because mines are only placed after first click
        board.click(0, 0)

        for i in range(board.rows):
            for j in range(board.cols):
                if not board.cells[i][j].has_mine:
                    board.click(i, j)

        self.assertTrue(board.check_win())
        self.assertTrue(board.get_game_status() == GAME_WON)

    # if I click on a mine then game should be over and I lost
    def test_game_lost_on_mine_click(self):
        board = Board()
        found = False

        # must do first click because mines are only placed after first click
        board.click(0, 0)

        for i in range(board.rows):
            for j in range(board.cols):
                if not found and board.cells[i][j].has_mine:
                    board.click(i, j)
                    found = True

        self.assertFalse(board.check_win())
        self.assertTrue(board.get_game_status() == GAME_LOST)


    def test_board_init_empty(self):
        board = Board()
        self.assertTrue(board.is_board_empty())

    # if I flag a cell then the board is still empty
    def test_board_empty_flag_click(self):
        board = Board()
        board.flag_click(0, 0)

        self.assertTrue(board.is_board_empty())

    # if I click on a cell then the board is not empty
    def test_board_not_empty_click(self):
        board = Board()
        board.click(0, 0)

        self.assertFalse(board.is_board_empty())

    def test_is_board_empty(self):
        board = Board(8, 8)
        self.assertTrue(board.is_board_empty())

        board.click(random.randint(0, 6), random.randint(0, 6))
        self.assertFalse(board.is_board_empty())


if __name__ == '__main__':
    unittest.main()
