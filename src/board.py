from utils import stringifyBoard, in_bounds, parseTestCase
from pieces import PieceFactory, Piece
from my_exceptions import PositionException, PieceException

UPPER_Y = 4
UPPER_X = 4
LOWER_Y = 0
LOWER_X = 0


class Board:
    board = []
    pieces = ['k', 'g', 's', 'b', 'r']
    lower_captured = []
    UPPER_captured = []
    file_moves = []

    def __init__(self, mode='i', fp=''):
        """
        Init Board object
        :param mode: i for interactive, f for file mode
        """
        self.board = [['', '', '', '', ''] for _ in range(5)]
        if mode == 'i':
            self.set_default_positions()
        elif mode == 'f':
            self.set_file_positions(fp)

    def set_default_positions(self):
        for i in xrange(0, UPPER_Y+1):
            self.board[i][0] = PieceFactory.create_piece(self.pieces[i].lower(), (i, 0))
            self.board[i][4] = PieceFactory.create_piece(self.pieces[UPPER_Y-i].upper(), (i, 4))
        self.board[0][1] = PieceFactory.create_piece('p', (0, 1))
        self.board[4][3] = PieceFactory.create_piece('P', (4, 3))

    def set_file_positions(self, fp):
        test_case = parseTestCase(fp)
        for p in test_case['initialPieces']:
            x, y = Board.sq_to_position(p['position'])
            piece_type = p['piece']
            self.board[x][y] = PieceFactory.create_piece(piece_type, (x, y))
        self.lower_captured = test_case['lowerCaptures']
        self.UPPER_captured = test_case['upperCaptures']
        self.file_moves = test_case['moves']

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
            x, y = self.sq_to_position(dest)
            if type(self.board[x][y]) is not str:
                if isinstance(self.board[x][y], Piece):
                    captured_piece = str(self.piece_at_square(dest))
                    if captured_piece.islower():
                        self.UPPER_captured.append(captured_piece[-1].upper())
                    else:
                        self.lower_captured.append(captured_piece[-1].lower())

                    self.board[x][y] = ''  # reset space
                # move
                self.move(origin, dest)
                return 1
            else:
                return 0
        except:
            return 0

    def promote_piece_at(self, square):
        """
        Promote piece at a square
        :param square: square
        :return: 1 if success, 0 if not success
        :raises PieceException
        """
        x, y = Board.sq_to_position(square)
        p = self.board[x][y]
        if isinstance(p, Piece):
            try:
                p.promote()
                return 1
            except PieceException:
                return 0
        return 0

    def drop(self, piece_type, dest):
        """
        Drop a piece at square
        :param piece_type: piece type, case sensitive
        :param dest: destination square
        :return: 1 if success, 0 if failure
        """
        x, y = Board.sq_to_position(dest)
        self.board[x][y] = PieceFactory.create_piece(piece_type, (x, y))
        return 1 if self.board[x][y] else 0

    def piece_at_square(self, square):
        """
        Check if there is a piece at given square
        :param square: board square
        :return: Piece object value if found, else return None
        """
        x, y = Board.sq_to_position(square)
        if isinstance(self.board[x][y], Piece):
            return self.board[x][y]
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

    @staticmethod
    def position_to_square(pos):
        """
        Convert a position tuple to square
        :param pos (x,y) int tuple
        :return: a string (e.g. a1) representing the square
        :raises PositionException if invalid square
        """
        letters = ['a', 'b', 'c', 'd', 'e']
        for j in range(len(letters)):
            if pos[0] == j:
                return letters[j] + str(pos[1]+1)
        raise PositionException('Invalid position: {}'.format(pos))

    def __repr__(self):
        """ Used for debugging """
        s = ''
        for row in range(len(self.board)):
            s += '{}\n'.format([i for i in self.board[row]])
        return s

    def __str__(self):
        """ Board string representation """
        return stringifyBoard(self.board)
