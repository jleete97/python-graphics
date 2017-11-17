import random
import sys
import time

from reversiboard import *

from games.turns.reversi.reversimoves import *

# Window parameters
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

# Colors
DARK_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
LIGHT_RED = (255, 192, 192)
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

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

another_game = True

while another_game:

    playerIndex = random.randrange(2)
    board = ReversiBoard(BOARD_SIZE, sides)

    drawer = ReversiBoardDrawer(board,
                                surface,
                                WINDOW_WIDTH,
                                WINDOW_HEIGHT,
                                DARK_GREY,
                                DARK_GREEN,
                                GREEN,
                                sides, colors)

    try:
        playing = True
        missedMoves = 0
        winner = None

        while playing:
            opponentIndex = 1 - playerIndex
            player = sides[playerIndex]
            opponent = sides[opponentIndex]

            drawer.drawBoard()

            moveResult = []

            if board.noLegalMoves(player, opponent):
                print(player + " has no legal move.")
                move = None
                time.sleep(3)
            else:
                print(player + " is moving...")

                if player == HUMAN:
                    while moveResult == []:
                        move = getPlayerMove(drawer)
                        moveResult = board.resultOfMove(move, player, opponent)
                else:
                    move = getComputerMove(board, COMPUTER, HUMAN)
                    moveResult = board.resultOfMove(move, player, opponent)

            displayMove = None

            if (move is not None):
                displayMove = (move[0] + 1, move[1] + 1);

            print(player + " has moved: " + str(displayMove))

            if move is None:
                missedMoves += 1
            else:
                missedMoves = 0

            if missedMoves == 2:
                winner = board.determineWinner()
                playing = False
            else:
                board.apply(move, moveResult, player)
                drawer.drawMove(move, player)

                if board.isFull():
                    winner = board.determineWinner()
                    playing = False

                playerIndex = 1 - playerIndex

    except PlayerQuitException:
        pass

    if winner is None:
        outcome = "The game is a tie."
    else:
        outcome = "The " + winner + " wins!"

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurface = fontObj.render(outcome, True, LIGHT_RED, DARK_GREY)
    textRect = textSurface.get_rect()
    textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    surface.blit(textSurface, textRect)
    pygame.display.update()

    asking_about_another_game = True

    while asking_about_another_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                another_game = False
                asking_about_another_game = False
                break
            elif event.type == KEYUP and event.key in [K_ESCAPE, ord('r')]:
                asking_about_another_game = False
                break

        pygame.display.update()

pygame.quit()
sys.exit()
