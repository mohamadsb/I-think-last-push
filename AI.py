from Inputanalayzer import Inputanalyzer
import random

WHITE = True
BLACK = False

class AI:

    depth = 1
    board = None
    side = None
    movesAnalyzed = 0

    def __init__(self, board, side, depth):
        self.board = board
        self.side = side
        self.depth = depth
        self.analyzer = Inputanalyzer(self.board, self.side)


    def generateMoveTree(self):
        moveTree = []
        for move in self.board.getAllMovesLegal(self.side):
            moveTree.append(MoveNode(move, [], None))

        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateNodeChildren(node)
            self.board.undoLastMove()
        return moveTree                          #hala inja harkodoom az move ha tooye movetree  ye emtiaz daran

    def populateNodeChildren(self, node):
        node.pointAdvantage = self.board.getPointAdvantageOfSide(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return

        side = self.board.currentSide

        legalMoves = self.board.getAllMovesLegal(side)
        if not legalMoves:
            if self.board.isCheckmate():
                node.move.checkmate = True
                return
            elif self.board.isStalemate():
                node.move.stalemate = True
                node.pointAdvantage = 0
                return
            raise Exception()

        for move in legalMoves:
            node.children.append(MoveNode(move, [], node))           ##harakat haye jadido bache node mizarim
            self.board.makeMove(move)
            self.populateNodeChildren(node.children[-1])
            self.board.undoLastMove()

    def getOptimalPointAdvantageForNode(self, node):
        if node.children:
            for child in node.children:                                 #child ha harkodoom az shakhe haye baadie shekl bekesh barash
                child.pointAdvantage = self.getOptimalPointAdvantageForNode(child)

            # age depth zoj bashe bayad min begire chon bayad bbine ke hadeaqal emitiaze harfi cheqad mishe.
            #age fard bshe max ke emtiaze khodeshe dg
            if node.children[0].depth % 2 == 1:
                return(max(node.children).pointAdvantage)
            else:
                return(min(node.children).pointAdvantage)
        else:
            return node.pointAdvantage

    def getBestMove(self):
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        randomBestMove = random.choice(bestMoves)                   #az beyne harkati ke emtiaze barabar darand yeki random bar midare
        randomBestMove.notation = self.analyzer.notationForMove(randomBestMove)
        return randomBestMove

    def bestMovesWithMoveTree(self, moveTree):
        bestMoveNodes = []
        for moveNode in moveTree:
            moveNode.pointAdvantage = self.getOptimalPointAdvantageForNode(moveNode)
            if not bestMoveNodes:            ## az beyne harakata balatarin emtiaz ro add mikone,
                bestMoveNodes.append(moveNode)
            elif moveNode > bestMoveNodes[0]:
                bestMoveNodes = []
                bestMoveNodes.append(moveNode)
            elif moveNode == bestMoveNodes[0]:     #dota masir emtiaze barabar ham dashtan jofteshun ezafe mishe
                bestMoveNodes.append(moveNode)

        return [node.move for node in bestMoveNodes]




class MoveNode:

    def __init__(self, move, children, parent):
        self.move = move
        self.children = children
        self.parent = parent
        self.pointAdvantage = None
        self.depth = 1

    def __gt__(self, other):
        if self.move.checkmate and not other.move.checkmate:
            return True
        if not self.move.checkmate and other.move.checkmate:
            return False
        if self.move.checkmate and other.move.checkmate:
            return False
        return self.pointAdvantage > other.pointAdvantage

    def __lt__(self, other):
        if self.move.checkmate and not other.move.checkmate:
            return False
        if not self.move.checkmate and other.move.checkmate:
            return True
        if self.move.stalemate and other.move.stalemate:
            return False
        return self.pointAdvantage < other.pointAdvantage

    def __eq__(self, other):
        if self.move.checkmate and other.move.checkmate:
            return True
        return self.pointAdvantage == other.pointAdvantage


    def getDepth(self):              ##tooye populate node children seda mizane
        depth = 1
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
                depth += 1
            else:
                return depth
