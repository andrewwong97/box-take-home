from board import Board


class Game:
    def __init__(self, mode):
        """
        Initialize a Game state
        :param mode: i for interactive or f for file mode
        """
        self.board = Board(mode)

    def execute(self, command):
        print command