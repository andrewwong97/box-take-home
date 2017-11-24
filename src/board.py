from utils import stringifyBoard, in_bounds
from pieces import PieceFactory, Piece
from my_exceptions import PositionException

UPPER_Y = 4
UPPER_X = 4
LOWER_Y = 0
LOWER_X = 0


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
        for i in xrange(0, UPPER_Y+1):
            self.board[i][0] = PieceFactory.create_piece(self.pieces[i].lower(), (i, 0))
            self.board[i][4] = PieceFactory.create_piece(self.pieces[UPPER_Y-i].upper(), (i, 4))
        self.board[0][1] = PieceFactory.create_piece('p', (0, 1))
        self.board[4][3] = PieceFactory.create_piece('P', (4, 3))

    def move(self, origin, dest):
        """
        Move a board piece (win conditions and validity checked inside Game caller)
        :param origin: origin square
        :param dest: destination square
        :return: 1 if success, 0 if failure
        """
        try:
            o = self.sq_to_position(origin)
            d = self.sq_to_position(dest)
            self.board[d[0]][d[1]] = self.board[o[0]][o[1]]
            self.board[o[0]][o[1]] = ''
            return 1
        except:
            return 0

    def capture(self, origin, dest):
        """
        Perform board operations for a capture event, assuming correct inputs.
        First capture, then move.
        :param origin: origin square
        :param dest: destination square
        :return: 1 if success, 0 if failure
        """
        try:
            # capture
            d = self.sq_to_position(dest)
            if isinstance(self.board[d[0]][d[1]], Piece):
                captured_piece = self.piece_at_square(dest)
                if captured_piece.islower():
                    self.UPPER_captured.append(captured_piece)
                else:
                    self.lower_captured.append(captured_piece)
            # move
            self.move(origin, dest)
            return 1
        except:
            return 0

    def piece_at_square(self, square):
        """
        Check if there is a piece at given square
        :param square: board square
        :return: piece value if found, else return None
        """
        r, c = Board.sq_to_position(square)
        if isinstance(self.board[r][c], Piece):
            return self.board[r][c].piece_type[-1]
        else:
            return None

    @staticmethod
    def is_in_bounds(origin, dest):
        """
        Check if origin, destination are in bounds
        :param origin: origin square
        :param dest: destination square
        :return: True if in bounds, False otherwise
        """
        try:
            o = Board.sq_to_position(origin)
            d = Board.sq_to_position(dest)
            return in_bounds(o) and in_bounds(d)
        except PositionException:
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



