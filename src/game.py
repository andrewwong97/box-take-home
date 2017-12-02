from board import Board
from pieces import Piece
from my_exceptions import MoveException, TurnException


class Game:
    turn = 'lower'
    num_turns = 0

    def __init__(self, mode, fp=None):
        """
        Initialize a Game state
        :param mode: i for interactive or f for file mode
        """
        self.board = Board(mode, fp)

    def execute(self, move):
        """
        Execute a move or drop command
        :param move: command string given by a file or shell
        :return: 1 if success, 0 if failure
        :raises: MoveException if invalid
        """
        if self.num_turns >= 400:
            raise TurnException("stalemate")

        line = move.strip().split()
        if line[0].lower() == 'move':
            if len(line) == 3:
                origin, dest = line[1:]
                self.handle_move(origin, dest)
            elif len(line) == 4 and line[3].lower() == 'promote':
                origin, dest = line[1:3]
                if self.handle_move(origin, dest):
                    # promote piece if move successful
                    if self.end_zone(dest):
                        return self.board.promote_piece_at(dest)
                else:
                    return 0
            else:
                raise MoveException('Invalid move: {}'.format(move))
        elif line[0].lower() == 'drop':
            if len(line) == 3:
                piece_type, dest = line[1:]
                if len(piece_type.strip()) != 1:
                    raise MoveException('Invalid drop, piece must be a single value: {}'.format(piece_type))
                if self.turn == 'lower':
                    if piece_type in self.board.lower_captured and not self.board.piece_at_square(dest):
                        self.board.lower_captured.remove(piece_type)
                        return self.board.drop(piece_type, dest)
                    return 0
                elif self.turn == 'UPPER':
                    if piece_type.upper() in self.board.UPPER_captured and not self.board.piece_at_square(dest):
                        self.board.UPPER_captured.remove(piece_type.upper())
                        return self.board.drop(piece_type.upper(), dest)
                    return 0
                else:
                    return 0
            else:
                raise MoveException('Invalid drop: {}'.format(move))
        self.next_turn()

    def handle_move(self, origin, dest):
        """
        Move a board piece, if there exists a piece and the move is valid.
        Win conditions checked here.
        :param origin: origin square
        :param dest: destination square
        :return: 1 if success, 0 if failure
        :raises: MoveException if piece does not exist or the move is invalid
                 TurnException if move out of turn or move invalid piece
        """
        pass
        if Board.is_in_bounds(origin, dest):
            o_piece = self.board.piece_at_square(origin)
            d_piece = self.board.piece_at_square(dest)
            if o_piece:
                if not same_casing(o_piece, self.turn):
                    raise TurnException("{} attempted to move other player's piece".format(self.turn))
                if not d_piece:
                    # simple move, _moveset check
                    if self.is_valid_move(origin, dest):
                        return self.board.move(origin, dest)
                    else:
                        # print [Board.position_to_square(i) for i in o_piece.get_moves]
                        # print 'DEBUG: {}'.format(o_piece.get_moves)
                        raise MoveException("not in moveset: {}, position {}".format(dest, Board.sq_to_position(dest)))
                if same_casing(o_piece, d_piece):
                    # exists player owned piece at destination
                    raise MoveException("{} and {} are both owned by the same player".format(origin, dest))
                if not same_casing(o_piece, d_piece):
                    # exists opposite pieces, capture event
                    if self.is_valid_move(origin, dest):
                        return self.board.capture(origin, dest)

            else:
                # there is no piece at origin
                raise MoveException("no piece at {} to move".format(origin))
        else:
            raise MoveException('{} or {} out of bounds'.format(origin, dest))

    def is_valid_move(self, origin, dest):
        """ Helper function for valid move checks, no jumps """
        o_piece = self.board.piece_at_square(origin)

        # if there is a piece of the same player behind o_piece, concat moveset of that piece to o_piece.get_moves
        behind_pos = Board.sq_to_position(origin)  # (x,y)-tuple
        if self.turn == 'lower':
            behind_pos = (behind_pos[0], behind_pos[1]-1)
        else:
            behind_pos = (behind_pos[0], behind_pos[1]+1)

        behind_piece = self.board.piece_at_square(Board.position_to_square(behind_pos))
        shift = []
        if behind_piece:
            if self.turn == 'lower':
                # get_moves is a list of valid (x, y) coordinates inside the board
                shift = [(i[0], i[1] + 1) for i in behind_piece.get_moves]
            else:
                shift = [(i[0], i[1] - 1) for i in behind_piece.get_moves]

        new_moveset = list(set(o_piece.get_moves + shift))  # list concat

        if Board.sq_to_position(dest) in new_moveset:
            for pos in self.get_path_positions(origin, dest, new_moveset):
                if self.board.piece_at_square(Board.position_to_square(pos)):
                    # there is a piece between origin and destination
                    return False
            # no piece between origin and destination
            return True
        # destination is not a valid move
        return False

    def get_path_positions(self, origin, dest, move_set):
        """
        Get intermediate positions between origin and destination
        :param origin: origin square (e.g. a1)
        :param dest: destination square (e.g. b2)
        :return: list of position 2-tuples
        """
        result = []
        # o_piece = self.board.piece_at_square(origin)
        o_pos = Board.sq_to_position(origin)
        d_pos = Board.sq_to_position(dest)
        if Board.is_bishop_path(o_pos, d_pos):
            for pos in move_set:
                if pos != o_pos and pos != d_pos and Board.is_bishop_path(o_pos, pos):
                    if Board.in_between(pos, o_pos, d_pos):
                        result.append(pos)
        if Board.is_rook_path(o_pos, d_pos):
            for pos in move_set:
                if pos != o_pos and pos != d_pos and Board.is_rook_path(o_pos, pos):
                    if Board.in_between(pos, o_pos, d_pos):
                        result.append(pos)
        return result

    def next_turn(self):
        self.turn = self.other_player()
        self.num_turns += 1

    def other_player(self):
        if self.turn == 'lower':
            return 'UPPER'
        else:
            return 'lower'

    def end_zone(self, dest):
        """ Is destination is in end zone for current turn? """
        if self.turn == 'lower':
            try:
                return int(dest[-1]) == 5
            except ValueError:
                return False
        else:
            try:
                return int(dest[-1]) == 0
            except ValueError:
                return False

    def __str__(self):
        """ stringify Game board and capture state """
        s = str(self.board)
        s += '\n'
        s += 'Captures UPPER: {}\n'.format(' '.join(self.board.UPPER_captured))
        s += 'Captures lower: {}\n'.format(' '.join(self.board.lower_captured))
        return s


def same_casing(s1, s2):
    """
    Check if two object string representation are the same casing
    :param s1: first object
    :param s2: second object
    :return: True if same casing, False if not same casing
    """
    s1, s2 = str(s1), str(s2)
    return (s1.islower() and s2.islower()) or (s1.isupper() and s2.isupper())
