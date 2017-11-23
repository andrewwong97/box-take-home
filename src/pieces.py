from abc import ABCMeta, abstractmethod
from my_exceptions import PieceException
from board import Board, UPPER_Y, UPPER_X, LOWER_Y, LOWER_X


class PieceFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_piece(self, piece_type, coords):
        p = piece_type.lower()
        if p == 'p':
            return Pawn(piece_type, coords)
        elif p == 'b':
            return Bishop(piece_type, coords)
        elif p == 'r':
            return Rook(piece_type, coords)
        elif p == 'sg':
            return SilverGeneral(piece_type, coords)
        elif p == 'gg':
            return GoldGeneral(piece_type, coords)
        elif p == 'k':
            return King(piece_type, coords)
        else:
            raise PieceException("{} invalid piece type".format(piece_type))


class Piece(metaclass=ABCMeta):

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
        return self._moveset

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


class King(object, Piece):
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
        self._moveset = gold_gen_moves(self.x, self.y)
        self.piece_type = '+{}'.format(self.piece_type)


class Bishop(Piece):
    def __init__(self, piece_type, coords):
        super(Bishop, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = bishop_moves(self.x, self.y), bishop_moves(self.x, self.y)

    def promote(self, to_king=False):
        if to_king:
            self._moveset = king_moves(self.x, self.y)
        self.piece_type = '+{}'.format(self.piece_type)


class Rook(Piece):
    def __init__(self, piece_type, coords):
        super(Rook, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = rook_moves(self.x, self.y), rook_moves(self.x, self.y)

    def promote(self, to_king=False):
        if to_king:
            self._moveset = king_moves(self.x, self.y)
        self.piece_type = '+{}'.format(self.piece_type)


class Pawn(Piece):
    def __init__(self, piece_type, coords):
        super(Pawn, self).__init__(piece_type, coords)
        self._moveset, self._unpromote = pawn_moves(self.x, self.y), pawn_moves(self.x, self.y)

    def promote(self):
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
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i == j:
                result.append((x + i, y + j))
    result.remove((x, y))
    return remove_out_of_bounds(result)


def rook_moves(x, y):
    result = []
    # get all possible vertical and horizontal moves
    for i in range(LOWER_X, UPPER_X+1):
        result.append((i, y))
    for j in range(LOWER_Y, UPPER_Y+1):
        result.append((x, j))
    # remove out of bounds moves
    result.remove((x, y))
    return remove_out_of_bounds(result)


def pawn_moves(x, y):
    return remove_out_of_bounds([(x, y+1)])


def remove_out_of_bounds(moves_list):
    """ Remove out of bounds 2-tuple coordinates from a moves list """
    for coord in moves_list:
        if not Board.bounds_helper(coord):
            moves_list.remove(coord)
    return moves_list
