import pygame, sys, random, math
from pygame.locals import *
from rotate import rotate, offsetRotate
from movers import *

# Constants

# Window parameters
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
# Sun parameters
SUN_RADIUS = 30
SUN_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
GRAVITY_CONSTANT = 30.0
TOO_CLOSE = SUN_RADIUS * 2



# Initialize
pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Gravity")

ship = SpaceShip((WINDOW_WIDTH // 20, WINDOW_HEIGHT // 20))

# Main event loop
while True:

    # Handle events: rotation, thrust, color change, quit

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

    pygame.display.update()
    mainClock.tick(80)
