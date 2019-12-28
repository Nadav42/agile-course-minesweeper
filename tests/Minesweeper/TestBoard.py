import unittest
from Minesweeper.Board import Board
import random
from Minesweeper.Board import Cell

class TestSum(unittest.TestCase):

    def test_first_click(self):
        board = Board(7, 7, 0.3)
        for i in range(10):  # check with 10 randoms points
            board.click(random.randint(0, 6), random.randint(0, 6))
            self.assertTrue(board.get_game_status)

    def test_range_difficulty(self) :
        board = Board (9,9)
        difficulty=board.get_difficulty()
        self.assertGreaterEqual (difficulty,0.12)
        self.assertLessEqual (difficulty, 0.37)

    def test_check_win(self):
        self.assertTrue (Board.check_win)

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6)

    def test_board_init_empty(self):
        self.assertTrue (Board.is_board_empty)

    def test_is_board_empty(self):
        board= Board(8,8)
        self.assertTrue(board.is_board_empty())
        board.click (random.randint (0, 6), random.randint (0, 6))
        self.assertFalse (board.is_board_empty ())

if __name__ == '__main__':
    unittest.main()
