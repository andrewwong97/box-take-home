from abc import ABCMeta, abstractmethod

can_promote = ['s', 'b', 'r', 'p']


class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, piece_type, coords):
        """
        :param piece_type: Case sensitive piece name
        :param coords: (x,y) board position tuple
        """
        self.piece_type = piece_type
        x, y = coords
        self.x = x
        self.y = y

    @abstractmethod
    def get_moves(self):
        """ Returns list of possible (x,y) coordinates to move to """
        pass

    @property
    def owner(self):
        return 'lower' if self.piece_type.islower() else 'UPPER'

    def promote(self):
        """ Promote a piece """
        pass


class King(Piece):
    def __init__(self, piece_type, coords):
        super(King, self).__init__(piece_type, coords)

    def get_moves(self):
        result = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                result.append((self.x+i, self.y+j))
        result.remove((self.x, self.y))
        return result
