
class PositionException(Exception):
    def __init__(self, message):
        super(PositionException, self).__init__(message)


class MoveException(Exception):
    def __init__(self, message):
        super(MoveException, self).__init__(message)


class TurnException(Exception):
    def __init__(self, message):
        super(TurnException, self).__init__(message)


class PieceException(Exception):
    def __init__(self, message):
        super(PieceException, self).__init__(message)
