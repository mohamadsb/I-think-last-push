from Piece import Piece
from Tuplemake import TUPLE as C
from Move import Move


WHITE = True
BLACK = False

class Pawn(Piece):

    stringRep = 'p'
    value = 1

    def __init__(self, board, side, position,  movesMade=0):
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position

        # Pawn moves one up
        movement = C(0, 1) if self.side == WHITE else C(0, -1)
        advanceOnePosition = currentPosition + movement
        if self.board.isValidPos(advanceOnePosition):
                    yield Move(self, advanceOnePosition)

        # Pawn moves two up
        if self.movesMade == 0:
            movement = C(0, 2) if self.side == WHITE else C(0, -2)
            advanceTwoPosition = currentPosition + movement
            if self.board.isValidPos(advanceTwoPosition):
                if self.board.pieceAtPosition(advanceTwoPosition) is None and self.board.pieceAtPosition(advanceOnePosition) is None:
                    yield Move(self, advanceTwoPosition)

        # Pawn takes
        movements = [C(1, 1), C(-1, 1)]  if self.side == WHITE else [C(1, -1), C(-1, -1)]

        for movement in movements:
            newPosition = self.position + movement
            if self.board.isValidPos(newPosition):
                pieceToTake = self.board.pieceAtPosition(newPosition)
                if pieceToTake and pieceToTake.side != self.side:
                        yield Move(self, newPosition,pieceToCapture=pieceToTake)



class Bishop (Piece):

    stringRep = 'B'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        super(Bishop, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position
        directions = [C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,direction, self.side):
                yield move




class Knight(Piece):

    stringRep = 'N'
    value = 3

    def __init__(self, board, side, position,  movesMade=0):
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        currentPos = self.position
        movements = [C(2, 1), C(2, -1), C(-2, 1), C(-2, -1), C(1, 2),C(1, -2), C(-1, -2), C(-1, 2)]
        for movement in movements:
            newPos = currentPos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)


class Rook (Piece):

    stringRep = 'R'
    value = 5

    def __init__(self, board, side, position,  movesMade=0):
        super(Rook, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,direction, self.side):
                yield move

class Queen(Piece):

    stringRep = 'Q'
    value = 9

    def __init__(self, board, side, position, movesMade=0):
        super(Queen, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0), C(1, 1),C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,direction, self.side):
                yield move

class King (Piece):

    stringRep = 'K'
    value = 100

    def __init__(self, board, side, position,  movesMade=0):
        super(King, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPos = self.position
        movements = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0), C(1, 1),C(1, -1), C(-1, 1), C(-1, -1)]
        for movement in movements:
            newPos = currentPos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if self.board.pieceAtPosition(newPos) is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)

        # Castling    saay kar kardam kar bendazam nmishe :(

        if self.movesMade == 0:
            inCheck = False
            kingsideCastleBlocked = False
            queensideCastleBlocked = False
            kingsideCastleCheck = False
            queensideCastleCheck = False
            kingsideRookMoved = True
            queensideRookMoved = True

            kingsideCastlePositions = [self.position - C(1, 0),self.position - C(2, 0)]
            for pos in kingsideCastlePositions:
                if self.board.pieceAtPosition(pos):
                    kingsideCastleBlocked = True

            queensideCastlePositions = [self.position + C(1, 0), self.position + C(2, 0),self.position + C(3, 0)]
            for pos in queensideCastlePositions:
                if self.board.pieceAtPosition(pos):
                    queensideCastleBlocked = True

            if kingsideCastleBlocked and queensideCastleBlocked:
                return

            otherSideMoves = self.board.getAllMovesUnfiltered(not self.side,includeKing=False)
            for move in otherSideMoves:
                if move.newPos == self.position:
                    inCheck = True
                    break
                if move.newPos == self.position - C(1, 0) or move.newPos == self.position - C(2, 0):
                    kingsideCastleCheck = True
                if move.newPos == self.position + C(1, 0) or move.newPos == self.position + C(2, 0):
                    queensideCastleCheck = True

            kingsideRookPos = self.position - C(3, 0)
            kingsideRook = self.board.pieceAtPosition(kingsideRookPos) if self.board.isValidPos(kingsideRookPos) else None
            if kingsideRook and kingsideRook.stringRep == 'R' and kingsideRook.movesMade == 0:
                kingsideRookMoved = False

            queensideRookPos = self.position + C(4, 0)
            queensideRook = self.board.pieceAtPosition(queensideRookPos) if self.board.isValidPos(queensideRookPos) else None
            if queensideRook and queensideRook.stringRep == 'R' and queensideRook.movesMade == 0:
                queensideRookMoved = False

            if not inCheck:
                if not kingsideCastleBlocked and not kingsideCastleCheck and not kingsideRookMoved:
                    move = Move(self, self.position - C(2, 0))
                    rookMove = Move(self.position, self.position - C(1, 0))
                    move.specialMovePiece = self.board.pieceAtPosition(kingsideRookPos)
                    move.kingsideCastle = True
                    move.rookMove = rookMove
                    yield move
                if not queensideCastleBlocked and not queensideCastleCheck and not queensideRookMoved:
                    move = Move(self, self.position + C(2, 0))
                    rookMove = Move(self.position, self.position + C(1, 0))
                    move.specialMovePiece = self.board.pieceAtPosition(queensideRookPos)
                    move.queensideCastle = True
                    move.rookMove = rookMove
                    yield move