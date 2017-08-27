import pygame
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

def getComputerMove(board):
    return (5, 5)
