class Move:

    def __init__(self, piece, newPos, pieceToCapture=None):
        self.notation = None
        self.check = False
        self.checkmate = False
        self.kingsideCastle = False
        self.queensideCastle = False
        self.promotion = False
        self.pessant = False
        self.stalemate = False

        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.pieceToCapture = pieceToCapture
        # baraye pessant va castling ke kar nakardand
        self.specialMovePiece = None
        self.rookMove = None

    def __eq__(self, other):
        if self.oldPos == other.oldPos and self.newPos == other.newPos and self.specialMovePiece == other.specialMovePiece:
            if not self.specialMovePiece:
                return True
            if self.specialMovePiece and self.specialMovePiece == other.specialMovePiece:
                return True
            else:
                return False
        else:
            return False


    def reverse(self):
        return Move(self.piece, self.piece.position,pieceToCapture=self.pieceToCapture)
