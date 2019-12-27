import unittest
from Minesweeper.Board import Board

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6)

if __name__ == '__main__':
    unittest.main()
