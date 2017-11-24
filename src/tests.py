import unittest
from board import Board
from pieces import King, GoldGeneral


# A suite of sanity checks
class TestThings(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_piece_at_init(self):
        self.assertEqual(self.board.piece_at_square('a1'), 'k')

    def test_square_to_position(self):
        self.assertEqual(Board.sq_to_position('a1'), (0, 0))
        self.assertEqual(Board.sq_to_position('b1'), (1, 0))
        self.assertEqual(Board.sq_to_position('e5'), (4, 4))

    def test_piece_owner(self):
        k = King('k', (2, 2))
        self.assertEqual(k.owner, 'lower')

    def test_get_moves_king(self):
        k = King('k', (2, 2))
        self.assertEqual(len(k._moveset), 8)

    def test_get_moves_goldgen(self):
        gg = GoldGeneral('g', (0, 0))
        self.assertEqual(len(gg._moveset), 4)

    def test_empty_board(self):
        b = Board(mode='')
        for i in b.board:
            for j in i:
                assert j == ''


if __name__ == '__main__':
    unittest.main()
