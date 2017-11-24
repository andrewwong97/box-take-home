import argparse
from game import Game
from my_exceptions import MoveException, TurnException


def test_game(fp):
    print fp
    return 0


def play_game():
    game = Game('i')

    print game

    end_game = False
    while not end_game:
        move = raw_input(game.turn + '>')
        print '{} player action: {}'.format(game.turn, move)
        try:
            code = game.execute(move)
        except (MoveException, TurnException) as e:
            if e.message == "stalemate":
                print 'Tie game. Too many moves.'
            else:
                print '{} player wins. Illegal move.'.format(game.other_player())
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

