import math

import pygame
from pygame.locals import *

from games.action.rotate import offsetRotate

GRAVITY_CONSTANT = 2.0

class DrawableMover(object):

    def __init__(self, pos, mass, seesGravity = True, limits = None, limitStrategy = 'wrap'):
        self.pos = pos
        self.mass = mass
        self.seesGravity = seesGravity
        self.motion = (0, 0)
        self.accel = (0, 0)
        self.limits = limits
        self.limitStrategy = limitStrategy

    def calculateMotionChange(self, otherMasses):
        if self.seesGravity:
            self.accel = self.accelerationFromOtherMasss(otherMasses)

    def accelerationFromOtherMasss(self, otherMasses):
        totalAcceleration = (0, 0)

        for otherMass in otherMasses:
            if otherMass != self and otherMass.mass != 0:
                delta = (otherMass.pos[0] - self.pos[0], otherMass.pos[1] - self.pos[1])
                distSquared = delta[0] ** 2 + delta[1] ** 2

                if (distSquared > 0):
                    dist = math.sqrt(distSquared)
                    rawAccel = GRAVITY_CONSTANT * otherMass.mass / distSquared
                    accel = (rawAccel * (delta[0] / dist), rawAccel * (delta[1] / dist))
                else:
                    accel = (0, 0)

                totalAcceleration = (totalAcceleration[0] + accel[0],
                                     totalAcceleration[1] + accel[1])

        return totalAcceleration

    def incrementPosition(self):
        self.pos = (self.pos[0] + self.motion[0],
                    self.pos[1] + self.motion[1])

        if self.limits is not None:
            if (self.limitStrategy == 'wrap'):
                self.pos = wrap(self.pos, self.limits)
            else:
                self.motion = bouncedMotion(self.motion, self.pos, self.limits)
                self.pos = bouncedPosition(self.pos, self.limits)

        self.motion = (self.motion[0] + self.accel[0],
                       self.motion[1] + self.accel[1])

    def draw(self, surface):
        raise BaseException("I don't know how to draw myself")

def wrap(pos, limits):
    return (pos[0] % limits[0], pos[1] % limits[1])

def bouncedMotion(motion, pos, limits):
    return (motion[0] if pos[0] > 0 and pos[0] < limits[0] else -motion[0],
            motion[1] if pos[1] > 0 and pos[1] < limits[1] else -motion[1])

def bouncedPosition(pos, limits):
    return (bounce(pos[0], limits[0]), bounce(pos[1], limits[1]))

def bounce(coord, limit):
    if coord < 0:
        return -coord
    elif coord >= limit:
        return coord - (limit - coord + 1)
    else:
        return coord

# Ship size parameters
PLAYER_WIDTH = 6
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
BROWN = (128, 128, 0)

# Player can be any color except color of background, flame, sun,
# or black (until they explode, when they stay black)
PLAYER_COLORS = [BLUE, GREEN, PURPLE, TURQUOISE, WHITE, GREY]

ROTATION_INCREMENT = 10

class SpaceShip(DrawableMover):

    def __init__(self, pos, seesGravity = True, limits = None, limitStrategy = 'wrap'):
        super().__init__(pos, 0, True, limits = limits, limitStrategy = limitStrategy)

        self.direction = 0
        self.rotation = 0
        self.thrust = 0
        self.colorIndex = 0
        self.exploded = False
        self.explosionDiameter = 10

    def calculateMotionChange(self, otherMasses):
        super().calculateMotionChange(otherMasses)

        # Add rotation to direction the ship is facing
        self.direction = (self.direction + self.rotation) % 360

        # Add result of thrust to motion
        self.motion = offsetRotate(self.motion, (0, self.thrust), self.direction)

    def rotate(self, direction):
        if direction == 0:
            self.rotation = 0
        elif direction < 0:
            self.rotation = -ROTATION_INCREMENT
        else:
            self.rotation = ROTATION_INCREMENT


    def handle(self, event):
        if (event.type == KEYUP):
            if event.key == K_UP:
                self.thrust = 0
            elif event.key == K_LEFT or event.key == K_RIGHT:
                self.rotation = 0
            else:
                return False
        elif (event.type == KEYDOWN):
            if event.key == K_UP:
                self.thrust = 1
            elif event.key == K_LEFT:
                self.rotation = -10
            elif event.key == K_RIGHT:
                self.rotation = 10
            elif event.key == ord('c'):
                self.colorIndex = (self.colorIndex + 1) % len(PLAYER_COLORS)
            else:
                return False # no case matched, we didn't handle the event
        else:
            return False # not our type of event; we didn't handle.

        return True # we handled the event.

    def draw(self, surface):
        drawPos = (int(self.pos[0]), int(self.pos[1]))
        offsetl = PLAYER_WIDTH * 2
        offsetw = PLAYER_WIDTH
        front = offsetRotate(drawPos, (0, offsetl), self.direction)
        leftShoulder = offsetRotate(self.pos, (offsetw, -offsetl), self.direction)
        rightShoulder = offsetRotate(self.pos, (-offsetw, -offsetl), self.direction)
        shipColor = BLACK if self.exploded else PLAYER_COLORS[self.colorIndex]
        pygame.draw.polygon(surface,
                            shipColor,
                            (front, rightShoulder, leftShoulder))

        if (self.thrust > 0):
            flametip = offsetRotate(drawPos, (0, - offsetl * 2), self.direction)
            flamels = offsetRotate(drawPos, (offsetw // 2, -offsetl), self.direction)
            flamers = offsetRotate(drawPos, (-offsetw // 2, -offsetl), self.direction)
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

class Sun(DrawableMover):
    def __init__(self, pos, mass, diameter = 50, color = YELLOW, seesGravity = True):
        super().__init__(pos, mass, seesGravity)
        self.diameter = diameter
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (intPos(self.pos)), self.diameter)


class Planet(DrawableMover):
    def __init__(self, pos, mass, initialMotion, diameter = 5, color = BROWN, seesGravity = True):
        super().__init__(pos, mass, seesGravity)
        self.diameter = diameter
        self.color = color
        self.motion = initialMotion

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (intPos(self.pos)), self.diameter)

def intPos(pos):
    return (int(pos[0]), int(pos[1]))