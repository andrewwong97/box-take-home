import argparse
from game import Game
from my_exceptions import MoveException, TurnException


def test_game(fp):
    game = Game('f', fp)
    moves = game.board.file_moves
    for move in moves:
        play_turn(game, move)


def play_game():
    game, end_game = Game('i'), False
    print game
    while not end_game:
        move = raw_input(game.turn + '>')
        play_turn(game, move)


def play_turn(game, move):
    print '{} player action: {}'.format(game.turn, move)
    try:
        code = game.execute(move)
    except (MoveException, TurnException) as e:
        if e.message == "stalemate":
            print 'Tie game. Too many moves.'
        else:
            print '{} player wins. Illegal move.'.format(game.other_player())
            print 'DEBUG: {}'.format(e.message)
        return
    print game


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='specify filename to read commands from')
    parser.add_argument('-i', action='store_true', default=False, help='include this flag for interactive mode')
    args = parser.parse_args()

    mode = 'i' if args.i else 'f'
    if mode == 'f':
        test_game(args.f)
    else:
        play_game()

