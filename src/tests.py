import unittest
from board import Board
from pieces import *
from my_exceptions import TurnException, MoveException
from game import Game, same_casing
from utils import in_bounds


# A suite of sanity checks
class TestSanity(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_piece_at_init(self):
        self.assertEqual(str(self.board.piece_at_square('a1')), 'k')

    def test_square_to_position(self):
        self.assertEqual(Board.sq_to_position('a1'), (0, 0))
        self.assertEqual(Board.sq_to_position('b1'), (1, 0))
        self.assertEqual(Board.sq_to_position('e5'), (4, 4))
        self.assertEqual(Board.sq_to_position('e2'), (4, 1))

    def test_position_to_square(self):
        self.assertEqual(Board.position_to_square((0, 0)), 'a1')
        self.assertEqual(Board.position_to_square((4, 1)), 'e2')

    def test_piece_owner(self):
        k = King('k', (2, 2))
        self.assertEqual(k.owner, 'lower')

    def test_get_moves_king(self):
        k = King('k', (2, 2))
        self.assertEqual(len(k._moveset), 8)

    def test_get_moves_goldgen(self):
        g = GoldGeneral('g', (0, 0))
        self.assertEqual(len(g._moveset), 4)

    def test_empty_board(self):
        b = Board(mode='')
        for i in b.board:
            for j in i:
                assert j == ''

    def test_remove_out_of_bounds(self):
        self.assertEqual(remove_out_of_bounds([(-1, 6), (4, 1), (0, 2)]), [(4, 1), (0, 2)])

    def test_pos_in_bounds(self):
        self.assertFalse(in_bounds((-1, 4)))

    def test_same_casing_empty_space(self):
        self.assertFalse(same_casing('a1', ''))
        self.assertFalse(same_casing('a1', '_'))


class TestGameMoves(unittest.TestCase):
    def setUp(self):
        self.g = Game('i')

    def test_B_move_many_spaces(self):
        self.g.execute('move a1 b2')  # lower player moves, increments turn
        self.g.execute('move b5 e2')  # UPPER player moves bishop

    def test_p_move_two_spaces(self):
        self.assertRaises(MoveException, self.g.execute, 'move a2 a4')

    def test_stalemate(self):
        self.g.num_turns = 400
        try:
            self.g.execute('move a1 a2')
        except TurnException as e:
            self.assertEqual(e.message, 'stalemate')


if __name__ == '__main__':
    unittest.main()
