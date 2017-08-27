import pygame, sys
from reversiboard import *
from reversimoves import *
import random
import time

# Window parameters
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Colors
DARK_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Board size (number of squares on each side)
BOARD_SIZE = 8

HUMAN = 'human'
COMPUTER = 'computer'

# Players: computer is 'W', human is 'B'
# Pick random starting player
sides = [ HUMAN, COMPUTER ]
colors = { HUMAN : WHITE , COMPUTER : BLACK }

playerIndex = random.randrange(2)
board = ReversiBoard(BOARD_SIZE, sides)

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

drawer = ReversiBoardDrawer(board,
                            surface,
                            WINDOW_WIDTH,
                            WINDOW_HEIGHT,
                            DARK_GREY,
                            DARK_GREEN,
                            GREEN,
                            sides, colors)

while True:
    opponentIndex = 1 - playerIndex

    player = sides[playerIndex]
    opponent = sides[opponentIndex]

    drawer.drawBoard()

    if player == HUMAN:
        move = getPlayerMove(drawer)

        if move is None:
            pygame.quit()
            sys.exit()
    else:
        move = getComputerMove(board, COMPUTER, HUMAN)

        if move is None:
            print("I can't find a move. :(")
            pygame.quit()
            sys.exit()

    moveResult = board.resultOfMove(move, player, opponent)
    board.apply(moveResult, player)
    drawer.drawMove(move, player)

    playerIndex = 1 - playerIndex
