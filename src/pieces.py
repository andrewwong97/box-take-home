from abc import ABCMeta, abstractmethod
from my_exceptions import PieceException
from utils import in_bounds


class PieceFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_piece(piece_type, coords):
        """
        Create and return a Piece object
        :param piece_type: one of [p, b, r, s, g, k] piece types (case sensitive)
        :param coords: 2-tuple of piece position on board
        :return: new Piece object
        """
        promote, piece_type = piece_type[0], piece_type[-1]
        p = piece_type.lower()
        if p == 'p':
            piece = Pawn(piece_type, coords)
        elif p == 'b':
            piece = Bishop(piece_type, coords)
        elif p == 'r':
            piece = Rook(piece_type, coords)
        elif p == 's':
            piece = SilverGeneral(piece_type, coords)
        elif p == 'g':
            piece = GoldGeneral(piece_type, coords)
        elif p == 'k':
            piece = King(piece_type, coords)
        else:
            raise PieceException("{} invalid piece type".format(piece_type))
        if promote == '+':
            piece.promote()
        return piece


class Piece:

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
        self._moveset = []
        self._unpromote = self._moveset

    @property
    def get_moves(self):
        """ Returns list of possible (x,y) coordinates to move to """
        return remove_out_of_bounds(self._moveset)

    @property
    def owner(self):
        return 'lower' if self.piece_type.islower() else 'UPPER'

    @abstractmethod
    def promote(self):
        """ Promote a piece """
        pass

    def unpromote(self):
        self._moveset = self._unpromote
        self.piece_type = self.piece_type[-1]

    def __str__(self):
        return self.piece_type[-1]


class King(Piece):
    def __init__(self, piece_type, coords):
        super(King, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = king_moves(self.x, self.y), king_moves(self.x, self.y)

    def promote(self):
        raise PieceException('{} cannot be promoted'.format(__name__))


class GoldGeneral(Piece):
    def __init__(self, piece_type, coords):
        super(GoldGeneral, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = gold_gen_moves(self.x, self.y), gold_gen_moves(self.x, self.y)

    def promote(self):
        raise PieceException('{} cannot be promoted'.format(__name__))


class SilverGeneral(Piece):
    def __init__(self, piece_type, coords):
        super(SilverGeneral, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = silver_gen_moves(self.x, self.y), silver_gen_moves(self.x, self.y)

    def promote(self):
        """ Moves like a gold general """
        self._moveset = gold_gen_moves(self.x, self.y)
        self.piece_type = '+{}'.format(self.piece_type)


class Bishop(Piece):
    def __init__(self, piece_type, coords):
        super(Bishop, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = bishop_moves(self.x, self.y), bishop_moves(self.x, self.y)

    def promote(self):
        """ Moves like a bishop or king """
        self._moveset = list(set(king_moves(self.x, self.y) + bishop_moves(self.x, self.y)))
        self.piece_type = '+{}'.format(self.piece_type)


class Rook(Piece):
    def __init__(self, piece_type, coords):
        super(Rook, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = rook_moves(self.x, self.y), rook_moves(self.x, self.y)

    def promote(self):
        """ Moves like a rook or king """
        self._moveset = list(set(king_moves(self.x, self.y) + rook_moves(self.x, self.y)))
        self.piece_type = '+{}'.format(self.piece_type)


class Pawn(Piece):
    def __init__(self, piece_type, coords):
        super(Pawn, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = pawn_moves(self.x, self.y), pawn_moves(self.x, self.y)

    def promote(self):
        """ Moves like a gold general """
        self._moveset = gold_gen_moves(self.x, self.y)
        self.piece_type = '+{}'.format(self.piece_type)


def king_moves(x, y):
    result = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            result.append((x + i, y + j))
    result.remove((x, y))
    return remove_out_of_bounds(result)


def gold_gen_moves(x, y):
    result = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            result.append((x + i, y + j))
    result.remove((x, y))
    result.remove((x - 1, y - 1))
    result.remove((x + 1, y - 1))
    return remove_out_of_bounds(result)


def silver_gen_moves(x, y):
    result = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            result.append((x + i, y + j))
    result.remove((x, y))
    result.remove((x-1, y))
    result.remove((x+1, y))
    result.remove((x, y-1))
    return remove_out_of_bounds(result)


def bishop_moves(x, y):
    result = []
    for i in range(-4, 5):
        for j in range(-4, 5):
            if i == j or i == -1*j:
                result.append((x + i, y + j))
    result.remove((x, y))
    return remove_out_of_bounds(result)


def rook_moves(x, y):
    result = []
    # get all possible vertical and horizontal moves
    for i in range(0, 5):
        result.append((i, y))
    for j in range(0, 5):
        result.append((x, j))
    # remove out of bounds moves
    result.remove((x, y))
    return remove_out_of_bounds(result)


def pawn_moves(x, y):
    return remove_out_of_bounds([(x, y+1), (x, y-1)])


def remove_out_of_bounds(moves_list):
    """ Remove out of bounds 2-tuple coordinates from a moves list """
    for coord in moves_list:
        if not in_bounds(coord):
            moves_list.remove(coord)
    return list(set(moves_list))


