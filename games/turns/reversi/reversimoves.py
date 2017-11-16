import random

import pygame
from pygame.locals import *
import games.turns.reversi.reversiboard
from games.turns.reversi.reversiboard import ReversiBoard


class PlayerQuitException(BaseException):
    pass


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
        raise PlayerQuitException

    return move


def getComputerMove(board, player, opponent):
#    return randomLegalMove1(board, player, opponent)
    return bestScore(board, player, opponent)

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

def bestScore(board, player, opponent):
    bestMove = None
    maxScore = -1

    for row in range(board.size):
        for col in range(board.size):
            move = (row, col)
            if isLegalMove(move, board, player, opponent):
                moveScore = score(board, player, move, opponent)
                if moveScore > maxScore:
                    bestMove = move
                    maxScore = moveScore

    return bestMove

def score(board, player, move, opponent):
    moveResult = board.resultOfMove(move, player, opponent)

    if not moveResult:
        return 0

    updatedBoard = ReversiBoard()
    updatedBoard = board.copy(updatedBoard)
    updatedBoard.apply(move, moveResult, player)
    scoreForBoard = scoreBoard(updatedBoard, player, SQUARE_WEIGHTINGS)

def scoreBoard(board, player, wts):
    totalScore = 0

    for row in range(board.size):
        for col in range(board.size):
            if board.squares[row][col] == player:
                totalScore += wts[row][col]

    return totalScore

def buildSquareWeightings(boardSize):
    wts = []
    # Initialize all squares to 1
    for row in range(boardSize):
        wts.append([])

        for col in range(boardSize):
            wts[row].append(1)

    # Set sides
    SIDE_WEIGHT = 4

    for i in range(boardSize):
        wts[0][i] = SIDE_WEIGHT
        wts[boardSize - 1][i] = SIDE_WEIGHT
        wts[i][0] = SIDE_WEIGHT
        wts[i][boardSize - 1] = SIDE_WEIGHT

    # Set corners
    CORNER_WEIGHT = 10

    for row in [0, boardSize - 1]:
        for col in [0, boardSize - 1]:
            wts[row][col] = CORNER_WEIGHT

    return wts

SQUARE_WEIGHTINGS = buildSquareWeightings(8)
