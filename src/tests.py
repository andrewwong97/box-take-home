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

    def test_pos_not_in_bounds(self):
        self.assertFalse(in_bounds((-1, 4)))

    def test_same_casing_empty_space(self):
        self.assertFalse(same_casing('a1', ''))
        self.assertFalse(same_casing('a1', '_'))


class TestInteractiveGameMoves(unittest.TestCase):
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

    def test_lower_capture(self):
        self.g.execute('move e1 e4')
        self.assertEqual(self.g.board.lower_captured, ['p'])

    def test_end_zone(self):
        self.assertTrue(self.g.end_zone('a5'))
        self.assertFalse(self.g.end_zone('a0'))
        self.g.execute('move a1 b2')
        self.assertFalse(self.g.end_zone('a5'))
        self.assertTrue(self.g.end_zone('a0'))


class TestOtherGameMoves(unittest.TestCase):
    def setUp(self):
        self.g = Game('g')  # not interactive or file
        self.board_arr = self.g.board.board  # manually set board pieces

    def test_lower_pawn_promote(self):
        x, y = Board.sq_to_position('a4')
        self.board_arr[x][y] = PieceFactory.create_piece('p', (x, y))
        self.assertEqual(str(self.board_arr[x][y]), 'p')
        self.g.execute('move a4 a5 promote')
        self.assertEqual(self.g.board.piece_at_square('a5').piece_type, '+p')

    def test_basic_lower_pawn_drop(self):
        self.g.board.lower_captured = ['p']
        self.g.execute('drop p a1')
        self.assertEqual(self.g.board.piece_at_square('a1').piece_type, 'p')
        self.assertEqual(len(self.g.board.lower_captured), 0)

    def test_occupied_lower_pawn_drop(self):
        x, y = Board.sq_to_position('a1')
        self.board_arr[x][y] = PieceFactory.create_piece('B', (x, y))

        self.g.board.lower_captured = ['p']
        self.assertEqual(self.g.execute('drop p a1'), 0)
        self.assertEqual(self.g.board.piece_at_square('a1').piece_type, 'B')



if __name__ == '__main__':
    unittest.main()
