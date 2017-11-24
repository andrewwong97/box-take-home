from board import Board
from my_exceptions import MoveException, TurnException


class Game:
    turn = 'lower'
    num_turns = 0

    def __init__(self, mode):
        """
        Initialize a Game state
        :param mode: i for interactive or f for file mode
        """
        self.board = Board(mode)

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
            # elif len(line) == 4 and line[3].lower() == 'promote':
            #     origin, dest = line[1:3]
            #     if self.handle_move(origin, dest):
            #         # TODO: promote piece if move successful
            #         pass
            #     else:
            #         return 0
            else:
                raise MoveException('Command {} is not a valid move'.format(move))
        # elif line[0].lower() == 'drop':
        #     if len(line) == 3:
        #         piece, dest = line[1:]
        #     else:
        #         raise MoveException('Command {} is not a valid move'.format(move))
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
        # TODO:
        # if exists wrong turn piece at origin: TurnException
        pass
        if Board.is_in_bounds(origin, dest):
            o_piece = self.board.piece_at_square(origin)
            d_piece = self.board.piece_at_square(dest)
            if o_piece:
                if not same_casing(o_piece, self.turn):
                    raise TurnException("{} attempted to move other player's piece".format(self.turn))
                if not d_piece:
                    # simple move, _moveset check
                    if Board.sq_to_position(dest) in o_piece.get_moves:
                        return self.board.move(origin, dest)
                    else:
                        # print [Board.position_to_square(i) for i in o_piece.get_moves]
                        print 'DEBUG: {}'.format(o_piece.get_moves)
                        raise MoveException("not in moveset: {}, position {}".format(dest, Board.sq_to_position(dest)))
                if same_casing(o_piece, d_piece):
                    # exists player owned piece at destination
                    raise MoveException("{} and {} are both owned by the same player".format(origin, dest))
                if not same_casing(o_piece, d_piece):
                    # exists opposite pieces, capture event
                    return self.board.capture(origin, dest)
            else:
                # there is no piece at origin
                raise MoveException("no piece at {} to move".format(origin))
        else:
            raise MoveException('{} or {} out of bounds'.format(origin, dest))

    def next_turn(self):
        self.turn = self.other_player()
        self.num_turns += 1

    def other_player(self):
        if self.turn == 'lower':
            return 'UPPER'
        else:
            return 'lower'

    def __str__(self):
        """ stringify Game state """
        s = str(self.board)
        s += '\n'
        s += 'Captures UPPER: {}\n'.format(self.board.UPPER_captured)
        s += 'Captures lower: {}\n'.format(self.board.lower_captured)
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
