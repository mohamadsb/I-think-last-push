from Board import Board
from Inputanalayzer import Inputanalyzer
from AI import AI
import sys

WHITE = True
BLACK = False


def askForPlayerSide():
    playerChoiceInput = input("What side would you like to play as [w/b]? ").lower()
    if 'w' in playerChoiceInput:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK
def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()

def askForDepthOfAI():
    depthInput = 2
    try:
        depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow."
                               " [n]? "))
    except:
        print("Invalid input, defaulting to 2")
    return depthInput


def makeMove(move, board):
    print()
    print("Making move : " + move.notation)
    board.makeMove(move)


def startGame(board, playerSide, ai):
    analyzer = Inputanalyzer(board, playerSide)
    while True:
        print(board)
        print()
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            return

        if board.currentSide == playerSide:
            move = None
            command = input("It's your move plz enter your move""? ").lower()
            if command == 'u':
                undoLastTwoMoves(board)
                continue
            else:
                move = analyzer.moveForShortNotation(command)
            if move:
                makeMove(move, board)
            else:
                print("please enter a valid chess move.")
        else:
            print("AI is thinking...")
            move = ai.getBestMove()
            makeMove(move, board)

board = Board()
playerSide = askForPlayerSide()
print()
aiDepth = askForDepthOfAI()
opponentAI = AI(board, not playerSide, aiDepth)

try:
    startGame(board, playerSide, opponentAI)
except KeyboardInterrupt:
    sys.exit()
