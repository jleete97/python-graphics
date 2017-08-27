import pygame, math
from rotate import rotate, offsetRotate

GRAVITY_CONSTANT = 2.0

class DrawableMover(object):

    motion = (0, 0)

    def __init__(self, pos, mass, seesGravity = True):
        self.pos = pos
        self.seesGravity = seesGravity

    def moveAndAdjustMotion(self, masses):
        self.pos = (self.pos[0] + self.motion[0], self.pos[1] + self.motion[1])

        for mass in masses:
            if mass.mass != 0:
                delta = (mass.pos[0] - self.pos[0], mass.pos[1] - self.pos[1])
                distSquared = delta[0] ** 2 + delta[1] ** 2
                dist = math.sqrt(distSquared)
                rawAccel = GRAVITY_CONSTANT * mass.mass / distSquared
                accel = (rawAccel * (delta[0] / dist), rawAccel * (delta[1] / dist))
                self.motion = (self.motion[0] + accel[0], self.motion[1] + accel[1])

    def draw(self, surface):
        raise BaseException("I don't know how to draw myself")

# Ship size parameters
PLAYER_WIDTH = 10
PLAYER_LENGTH = PLAYER_WIDTH + PLAYER_WIDTH // 2

# Explosion size parameters
EXPLOSION_START = 10
EXPLOSION_LIMIT = 40

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

# Player can be any color except color of background, flame, sun,
# or black (until they explode, when they stay black)
PLAYER_COLORS = [BLUE, GREEN, PURPLE, TURQUOISE, WHITE, GREY]

ROTATION_INCREMENT = 10

class SpaceShip(DrawableMover):

    exploded = False
    direction = 0
    color = 0
    rotation = 0
    explosionDiameter = 10
    thrust = 0

    def rotate(self, direction):
        if direction == 0:
            self.rotation = 0
        elif direction < 0:
            self.rotation = -ROTATION_INCREMENT
        else:
            self.rotation = ROTATION_INCREMENT

    def draw(self, surface):
        offsetl = PLAYER_WIDTH * 2
        offsetw = PLAYER_WIDTH
        front = offsetRotate(self.pos, (0, offsetl), self.direction)
        leftShoulder = offsetRotate(self.pos, (offsetw, -offsetl), self.direction)
        rightShoulder = offsetRotate(self.pos, (-offsetw, -offsetl), self.direction)
        shipColor = BLACK if self.exploded else PLAYER_COLORS[self.color]
        pygame.draw.polygon(surface,
                            shipColor,
                            (front, rightShoulder, leftShoulder))
        if (self.thrust > 0):
            flametip = offsetRotate(self.pos, (0, - offsetl * 2), self.direction)
            flamels = offsetRotate(self.pos, (offsetw // 2, -offsetl), self.direction)
            flamers = offsetRotate(self.pos, (-offsetw // 2, -offsetl), self.direction)
            pygame.draw.polygon(surface,
                                RED,
                                (flametip, flamers, flamels))

        # Did we pull an Icarus?
#        if distanceFromSun <= TOO_CLOSE:
#            exploded = True
#            thrust = 0
#
#        if exploded and explosionDiameter <= EXPLOSION_LIMIT:
#            explosionColor = RED if explosionDiameter < EXPLOSION_LIMIT - 5 else ORANGE
#            pygame.draw.circle(surface, explosionColor, ((int(pos[0]), int(pos[1]))), explosionDiameter)
#            explosionDiameter += 1

SOLAR_MASS = 50

class Sun:
    mass = SOLAR_MASS

    def __init__(self, pos):
        self.pos = pos