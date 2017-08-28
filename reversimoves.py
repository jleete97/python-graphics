import pygame
import random
from pygame.locals import *
from reversiboard import ReversiBoard


def getPlayerMove(drawer):
    move = None
    userQuit = False

    while move is None and not userQuit:
        for event in pygame.event.get():
            if (event.type == QUIT):
                userQuit = True
                break
            elif event.type == MOUSEBUTTONUP:
                selectedSquare = drawer.pointToSquare(event.pos)
                if selectedSquare is not None and drawer.board.squares[selectedSquare[0]][selectedSquare[1]] is None:
                    move = selectedSquare
                    break
            elif event.type == KEYUP:
                if event.key in [K_ESCAPE, ord('x'), ord('q')]:
                    userQuit = True
                    break

    if userQuit:
        move = None

    return move


def getComputerMove(board, player, opponent):
    return randomLegalMove1(board, player, opponent)

# Pick 5, 5 at ALL times
def constantMove(board):
    return (5, 5)

# Pick ANY square on the board
def randomMove(board):
    row = random.randrange(board.size)
    col = random.randrange(board.size)
    return (row, col)

# Pick a random, but still legal, move
# By picking a random square, checking
# it, and moving to the first legal
# square entry
def isLegalMove(move, board, player, opponent):
    return board.isEmptyAt(move) \
           and board.hasAdjacentSquare(move, opponent) \
           and board.resultOfMove(move, player, opponent)

def randomLegalMove1(board, player, opponent):
    for n in range(100):
        row = random.randrange(board.size)
        col = random.randrange(board.size)
        move = (row, col)
        if isLegalMove(move, board, player, opponent):
            return (row, col)

    return None

# Pick a random, but still legal, move
# By checking every square every
def randomLegalMove2(board, player, opponent):
    legalMoves = []

    for row in range(board.size):
        for col in range(board.size):
            move = (row, col)
            if isLegalMove(move, board, player, opponent):
                legalMoves.append(move)

    if len(legalMoves) == 0:
        return None
    else:
        return legalMoves[random.randrange(len(legalMoves))]

