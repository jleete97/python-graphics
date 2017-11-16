import sys

from games.action.movers import *

# Constants

# Window parameters
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
window = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Sun parameters
SUN_RADIUS = 30
SUN_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
GRAVITY_CONSTANT = 30.0
TOO_CLOSE = SUN_RADIUS * 2

BACKGROUND_COLOR = (128, 128, 128)


# Initialize
pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Gravity")

# Define things moving around the screen (or not)
ship = SpaceShip((WINDOW_WIDTH // 20, WINDOW_HEIGHT // 20), limits = window)
sun1 = Sun((WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2), mass = 1000, diameter = 20)
sun2 = Sun((2 * WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2), mass = 300, diameter = 10)
planet1 = Planet((sun2.pos[0] + WINDOW_WIDTH // 30, sun2.pos[1]), 70, (0, 2))

sun1.motion = (0, 0.55)
sun2.motion = (0, -2)
planet1.color = GREEN

movers = [sun1, sun2, planet1, ship]
#movers = [sun1, ship]

def isQuitEvent(event):
    return event.type == QUIT \
        or ( (event.type == KEYUP) \
              and (event.key == K_ESCAPE or event.key == ord('q')) )

# Main event loop
while True:

    # Handle events: rotation, thrust, color change, quit

    for event in pygame.event.get():
        if isQuitEvent(event):
            pygame.quit()
            sys.exit()
        else:
            handled = ship.handle(event)

    # Calculate motion and position changes

    for mover in movers:
        mover.calculateMotionChange(movers)

    for mover in movers:
        mover.incrementPosition()

    # Draw

    # Background
    surface.fill(BACKGROUND_COLOR)

    # Various bodies
    for mover in movers:
        mover.draw(surface)

    pygame.display.update()
    mainClock.tick(800)
