from utils import stringifyBoard
from my_exceptions import PositionException


class Board:
    board = []

    def __init__(self, mode='i'):
        """
        Init Board object
        :param mode: i for interactive, f for file mode
        """
        self.board = [['', '', '', '', ''] for i in range(5)]
        if mode == 'i':
            self.set_default_positions()

    def set_default_positions(self):
        pieces = ['k', 'g', 's', 'b', 'r']
        for i in xrange(0, len(pieces)):
            self.board[i][0] = pieces[i].lower()
            self.board[i][4] = pieces[len(pieces)-i-1].upper()
        self.board[0][1] = 'p'
        self.board[4][3] = 'P'

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

