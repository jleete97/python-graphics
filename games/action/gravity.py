import math
import pygame
import sys
from pygame.locals import *

from games.action.rotate import offsetRotate

# Constants

# Window parameters
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
# Sun parameters
SUN_RADIUS = 30
SUN_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
GRAVITY_CONSTANT = 500.0
TOO_CLOSE = SUN_RADIUS * 3 // 2
EXPLOSION_START = 10
EXPLOSION_LIMIT = 40

# Player ship parameters
PLAYER_WIDTH = 10
PLAYER_LENGTH = PLAYER_WIDTH + PLAYER_WIDTH // 2

# Colors used in game
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 224, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TURQUOISE = (0, 255, 255)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
DARKGREY = (128, 128, 128)

# Player can be any color except color of background, flame, sun,
# or black (until they explode, when they stay black)
PLAYER_COLORS = [BLUE, GREEN, PURPLE, TURQUOISE, WHITE, GREY]

# Initialize
pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Gravity")

def initShip():
    global pos, direction, motion, color, thrust, exploded, rotation, explosionDiameter
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
    # Rotation direction
    rotation = 0
    # Diameter of explosion; not used until you explode
    explosionDiameter = 10

initShip()

# Main event loop
while True:

    # Handle events: rotation, thrust, color change, quit

    if exploded:
        # Exploded: handle quit, reset events only
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                elif event.key == ord('r'):
                    initShip()
    else:
        # Still alive - handle all events.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    thrust = 1
                elif event.key == K_LEFT:
                    rotation = -10
                elif event.key == K_RIGHT:
                    rotation = 10
            elif event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    rotation = 0
                elif event.key == K_UP:
                    thrust = 0
                elif event.key == ord('c'):
                    color = (color + 1) % len(PLAYER_COLORS)

    # Calculate motion and position changes

    # Add rotation to direction the ship is facing
    direction = (direction + rotation) % 360

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
    front = offsetRotate(pos, (0, offsetl), direction)
    leftShoulder = offsetRotate(pos, (offsetw, -offsetl), direction)
    rightShoulder = offsetRotate(pos, (-offsetw, -offsetl), direction)
    shipColor = BLACK if exploded else PLAYER_COLORS[color]
    pygame.draw.polygon(surface,
                        shipColor,
                        (front, rightShoulder, leftShoulder))
    if (thrust > 0):
        flametip = offsetRotate(pos, (0, - offsetl * 2), direction)
        flamels = offsetRotate(pos, (offsetw // 2, -offsetl), direction)
        flamers = offsetRotate(pos, (-offsetw // 2, -offsetl), direction)
        pygame.draw.polygon(surface,
                            RED,
                            (flametip, flamers, flamels))

    # Did we pull an Icarus?
    if distanceFromSun <= TOO_CLOSE:
        exploded = True
        thrust = 0

    if exploded and explosionDiameter <= EXPLOSION_LIMIT:
        explosionColor = RED if explosionDiameter < EXPLOSION_LIMIT - 5 else ORANGE
        pygame.draw.circle(surface, explosionColor, ((int(pos[0]), int(pos[1]))), explosionDiameter)
        explosionDiameter += 1

    pygame.display.update()
    mainClock.tick(80)
