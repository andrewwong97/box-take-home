import os


# defined here because used in both pieces.py and board.py
def in_bounds(pos):
    """ Check if a position 2-tuple is in board bounds """
    try:
        return 4 >= pos[0] >= 0 and 4 >= pos[1] >= 0
    except IndexError:
        return False


from pieces import Piece


def _stringifySquare(sq):

    if type(sq) is not str:
        if issubclass(sq, Piece):
            sq = str(sq)

    if type(sq) is not str or len(sq) > 2:
        raise ValueError('Board must be an array of strings like "", "P", or "+P"')

    if len(sq) == 0:
        return '__|'
    if len(sq) == 1:
        return ' ' + sq + '|'
    if len(sq) == 2:
        return sq + '|'


def stringifyBoard(board):

    s = ''

    for row in range(len(board) - 1, -1, -1):
        
        s += '' + str(row + 1) + ' |'
        for col in range(0, len(board[row])):
            s += _stringifySquare(str(board[col][row]))

        s += os.linesep

    s += '    a  b  c  d  e' + os.linesep

    return s


def parseTestCase(path):
    f = open(path)
    line = f.readline()
    initialBoardState = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initialBoardState.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upperCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lowerCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initialBoardState, upperCaptures=upperCaptures, lowerCaptures=lowerCaptures, moves=moves)
