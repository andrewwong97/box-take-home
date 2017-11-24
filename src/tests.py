import unittest
from board import Board
from pieces import *
from my_exceptions import TurnException


# A suite of sanity checks
class TestSanity(unittest.TestCase):
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
        g = GoldGeneral('g', (0, 0))
        self.assertEqual(len(g._moveset), 4)

    def test_pawn_move_two_spaces(self):
        from game import Game
        g = Game('i')
        g.execute('move a2 a4')

    def test_empty_board(self):
        b = Board(mode='')
        for i in b.board:
            for j in i:
                assert j == ''

    def test_stalemate(self):
        from game import Game
        g = Game('i')
        g.num_turns = 400
        try:
            g.execute('move a1 a2')
        except TurnException as e:
            self.assertEqual(e.message, 'stalemate')


if __name__ == '__main__':
    unittest.main()
