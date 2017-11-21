import unittest
from board import Board


# A suite of sanity checks
class TestThings(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_square_to_position(self):
        self.assertEqual(Board.sq_to_position('a1'), (0, 0))
        self.assertEqual(Board.sq_to_position('b1'), (1, 0))
        self.assertEqual(Board.sq_to_position('e5'), (4, 4))


if __name__ == '__main__':
    unittest.main()
