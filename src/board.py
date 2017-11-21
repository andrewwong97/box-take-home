from utils import stringifyBoard


class Board:
    board = []

    def __init__(self, mode):
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

    def __repr__(self):
        """ Used for debugging """
        s = ''
        for row in range(len(self.board)):
            s += '{}\n'.format([i for i in self.board[row]])
        return s

    def __str__(self):
        """ Board string representation """
        return stringifyBoard(self.board)

