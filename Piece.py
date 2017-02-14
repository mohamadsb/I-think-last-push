from Tuplemake import TUPLE as C
from Move import Move

WHITE = True
BLACK = False
X = 0
Y = 1


class Piece:

    def __init__(self, board, side, position, movesMade=0):
        self.board = board
        self.side = side
        self.position = position
        self.movesMade = 0

    def movesInDirectionFromPos(self, pos, direction, side):
        for dis in range(1, 8):
            movement = C(dis * direction[X], dis * direction[Y])
            newPos = pos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)

                elif pieceAtNewPos is not None:
                    if pieceAtNewPos.side != side:
                        yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
                    return



