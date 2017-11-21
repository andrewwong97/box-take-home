from board import Board


class Game:
    def __init__(self, mode):
        """
        Initialize a Game state
        :param mode: i for interactive or f for file mode
        """
        self.board = Board(mode)

    def execute(self, move):


    @staticmethod
    def extract_move(move):
        line = move.strip().split()
        if len(line) == 4:
            # promote
            cmd, origin, dest, promote = line
        elif len(line) == 3:
            if line[0] == 'move':
                origin, dest = line[1:]
            elif line[0] == 'dest':
                origin, dest = line[1: