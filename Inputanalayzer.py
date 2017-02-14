class Inputanalyzer:
    def __init__(self, board, side):
        self.board = board
        self.side = side
    def moveForShortNotation(self, notation):
        moves = self.getLegalMovesWithShortNotation(self.side)
        for move in moves:
            if move.notation.lower() == notation.lower():
                return move

    def notationForMove(self, move):
        side = self.board.getSideOfMove(move)
        moves = self.getLegalMovesWithShortNotation(side)
        for m in moves:
            if m == move:
                return m.notation

    def getLegalMovesWithShortNotation(self, side):
        moves = []
        for legalMove in self.board.getAllMovesLegal(side):       ### baraye hame harakat haye mojaz short not ro az board dar miare
            moves.append(legalMove)
            legalMove.notation = self.board.getShortNotationOfMove(legalMove)    ##notation harakat haro dar miare
        return moves
