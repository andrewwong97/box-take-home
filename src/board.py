from utils import stringifyBoard
from my_exceptions import PositionException, MoveException


class Board:
    board = []
    pieces = ['k', 'g', 's', 'b', 'r']
    lower_captured = []
    UPPER_captured = []

    def __init__(self, mode='i'):
        """
        Init Board object
        :param mode: i for interactive, f for file mode
        """
        self.board = [['', '', '', '', ''] for i in range(5)]
        if mode == 'i':
            self.set_default_positions()

    def set_default_positions(self):
        for i in xrange(0, len(self.pieces)):
            self.board[i][0] = self.pieces[i].lower()
            self.board[i][4] = self.pieces[len(self.pieces)-i-1].upper()
        self.board[0][1] = 'p'
        self.board[4][3] = 'P'

    def handle_move(self, origin, dest):
        """
        Move a board piece (win conditions and validity checked inside Game caller)
        :param origin: origin square
        :param dest: destination square
        :return: 1 if success, 0 if failure
        """
        # TODO: actually move the piece
        pass

    def piece_at_square(self, square):
        """
        Check if there is a piece at given square
        :param square: board square
        :return: piece value if found, else return None
        """
        r, c = Board.sq_to_position(square)
        for p in self.pieces:
            if self.board[r][c] == p.lower():
                return p.lower()
            elif self.board[r][c] == p.upper():
                return p.upper()
        return None

    @staticmethod
    def is_in_bounds(self, origin, dest):
        """
        Check if origin, destination are in bounds
        :param origin: origin square
        :param dest: destination square
        :return: True if in bounds, False otherwise
        """
        try:
            o = Board.sq_to_position(origin)
            d = Board.sq_to_position(dest)
            return Board.bounds_helper(o) and Board.bounds_helper(d)
        except PositionException:
            return False

    @staticmethod
    def bounds_helper(pos):
        """ Check if a position tuple is in board bounds """
        try:
            return 5 > pos[0] >= 0 and 5 > pos[1] >= 0
        except IndexError:
            return False

    @staticmethod
    def sq_to_position(square):
        """
        Convert a square to position tuple
        :param square: An origin or destination string of length 2, e.g. a1, b1
        :return: a tuple (x, y) where x is the ith row and y is
        the jth column of the 2d board
        :raises PositionException if invalid square
        """
        try:
            y = int(square[1])
            if y < 1 or y > 5:
                raise PositionException('Invalid y position: {}'.format(square[1]))
        except ValueError:
            raise PositionException('Invalid y position: {}'.format(square[1]))
        letters = ['a', 'b', 'c', 'd', 'e']
        for i in range(len(letters)):
            if square[0].lower() == letters[i]:
                return i, y-1
        raise PositionException('Invalid square: {}'.format(square))

    def __repr__(self):
        """ Used for debugging """
        s = ''
        for row in range(len(self.board)):
            s += '{}\n'.format([i for i in self.board[row]])
        return s

    def __str__(self):
        """ Board string representation """
        return stringifyBoard(self.board)

