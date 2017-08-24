import pygame, sys, random
from pygame.locals import *

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 200

PLAYER_WIDTH = 20
PLAYER_LENGTH = PLAYER_WIDTH + PLAYER_WIDTH // 2

pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Mover")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TURQUOISE = (0, 255, 255)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
DARKGREY = (128, 128, 128)

PLAYER_COLORS = [BLACK, RED, BLUE, GREEN, YELLOW, PURPLE, TURQUOISE, WHITE, GREY]

MOVESPEED = 4
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
STOPPED = (0, 0)

pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
move = STOPPED
color = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_LEFT:
                move = LEFT
            elif event.key == K_RIGHT:
                move = RIGHT
            elif event.key == K_UP:
                move = UP
            elif event.key == K_DOWN:
                move = DOWN
            elif event.key == ord('c'):
                color = (color + 1) % len(PLAYER_COLORS)
            else:
                move = STOPPED

    surface.fill(DARKGREY)

    pos = (pos[0] + move[0], pos[1] + move[1])

    if pos[0] - PLAYER_LENGTH // 2 <= 0:
        pos = (PLAYER_LENGTH // 2, pos[1])
        move = RIGHT
    elif pos[0] + PLAYER_LENGTH // 2 >= WINDOW_WIDTH:
        pos = (WINDOW_WIDTH - PLAYER_LENGTH // 2, pos[1])
        move = LEFT
    elif pos[1] - PLAYER_LENGTH // 2 <= 0:
        pos = (pos[0], PLAYER_LENGTH // 2)
        move = DOWN
    elif pos[1] + PLAYER_LENGTH // 2 >= WINDOW_HEIGHT:
        pos = (pos[0], WINDOW_HEIGHT - PLAYER_LENGTH // 2)
        move = UP

    facing = move
    if facing[0] == 0 and facing[1] == 0:
        facing = UP

    # triangle: tip, left & right shoulders
    offset = PLAYER_WIDTH // 2
    tip = (pos[0] + offset * facing[0], pos[1] - offset * facing[1])
    ls = (pos[0] + offset * (facing[1] - facing[0]), pos[1] - offset * (facing[1] + facing[0]))
    rs = (pos[0] - offset * (facing[1] - facing[0]), pos[1] + offset * (facing[1] - facing[0]))

    pygame.draw.polygon(surface,
                        PLAYER_COLORS[color],
                        (tip, rs, ls))

    pygame.display.update()
    mainClock.tick(40)
