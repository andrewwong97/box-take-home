import argparse
from board import Board
from game import Game


def test_game(fp):
    print fp
    return 0


def play_game():
    game = Game('i')

    end_game = False
    while not end_game:
        command = raw_input()
        game.execute(command)


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

