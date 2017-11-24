import argparse
from game import Game


def test_game(fp):
    print fp
    return 0


def play_game():
    game = Game('i')

    print game.board
    print 'Captures UPPER: {}'.format(game.board.UPPER_captured)
    print 'Captures lower: {}'.format(game.board.lower_captured)
    print ''

    end_game = False
    while not end_game:
        move = raw_input(game.turn + '>')
        print '{} player action: {}'.format(game.turn, move)
        game.execute(move)
        print game.board
        print ''
        print 'Captures UPPER: {}'.format(game.board.UPPER_captured)
        print 'Captures lower: {}'.format(game.board.lower_captured)


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

