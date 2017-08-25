import pygame, sys, random, math
from pygame.locals import *
from rotate import rotate, offsetRotate

# Constants

# Window parameters
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
# Sun parameters
SUN_RADIUS = 30
SUN_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
GRAVITY_CONSTANT = 30.0
TOO_CLOSE = SUN_RADIUS * 2

# Player ship parameters
PLAYER_WIDTH = 10
PLAYER_LENGTH = PLAYER_WIDTH + PLAYER_WIDTH // 2

# Colors used in game
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

# Player can be any color except color of background, flame, or sun
PLAYER_COLORS = [BLACK, BLUE, GREEN, PURPLE, TURQUOISE, WHITE, GREY]

# Initialize
pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Gravity")

# Player position (start well away from sun)
pos = (WINDOW_WIDTH // 20, WINDOW_HEIGHT // 10)
# Direction, in degrees from straight down
direction = 0
# Motion vector
motion = (0, 0)
# Color index in PLAYER_COLORS
color = 0
# Thrust level
thrust = 0
# Have we exploded?
exploded = False

# Main event loop
while True:

    if exploded:
        continue

    # Handle events: rotation, thrust, color change, quit

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                thrust = 1
        elif event.type == KEYUP:
            if event.key == K_ESCAPE or event.key == ord('q'):
                pygame.quit()
                sys.exit()
            elif event.key == K_LEFT:
                direction = (direction - 10) % 360
            elif event.key == K_RIGHT:
                direction = (direction + 10) % 360
            elif event.key == K_UP:
                thrust = 0
            elif event.key == ord('c'):
                color = (color + 1) % len(PLAYER_COLORS)

    # Calculate motion and position changes

    # Add result of thrust to motion
    motion = offsetRotate(motion, (0, thrust), direction)

    # Add effect of gravity
    gravityScale = GRAVITY_CONSTANT / ((pos[0] - SUN_POS[0]) ** 2 + (pos[1] - SUN_POS[1]) ** 2)
    gravityForce = ((SUN_POS[0] - pos[0]) * gravityScale, (SUN_POS[1] - pos[1]) * gravityScale)
    motion = (motion[0] + gravityForce[0], motion[1] + gravityForce[1])

    # Increment position; wrap around as needed
    pos = ((pos[0] + motion[0]) % WINDOW_WIDTH, (pos[1] + motion[1]) % WINDOW_HEIGHT)

    # Determine distance from sun for later comparison to TOO_CLOSE, to set exploded flag
    distanceFromSun = math.sqrt((pos[0]-SUN_POS[0]) ** 2 + (pos[1]-SUN_POS[1]) ** 2)

    # Draw

    # Background
    surface.fill(DARKGREY)
    # Sun
    pygame.draw.circle(surface, YELLOW, (SUN_POS), SUN_RADIUS)
    # Player's ship
    offsetl = PLAYER_WIDTH * 2
    offsetw = PLAYER_WIDTH
    tip = offsetRotate(pos, (0, offsetl), direction)
    ls = offsetRotate(pos, (offsetw, -offsetl), direction)
    rs = offsetRotate(pos, (-offsetw, -offsetl), direction)
    pygame.draw.polygon(surface,
                        PLAYER_COLORS[color],
                        (tip, rs, ls))
    if (thrust > 0):
        flametip = offsetRotate(pos, (0, - offsetl * 2), direction)
        flamels = offsetRotate(pos, (offsetw // 2, -offsetl), direction)
        flamers = offsetRotate(pos, (-offsetw // 2, -offsetl), direction)
        pygame.draw.polygon(surface,
                            RED,
                            (flametip, flamers, flamels))

    # Did we pull an Icarus?
    if distanceFromSun <= TOO_CLOSE:
        pygame.draw.circle(surface, RED, ((int(pos[0]), int(pos[1]))), SUN_RADIUS // 2)
        exploded = True

    pygame.display.update()
    mainClock.tick(40)
