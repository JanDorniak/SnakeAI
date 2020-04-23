from enum import Enum
import pygame
from pygame.locals import *
import random
import numpy as np


SPEED = 2
RADIUS = 12
SNAKE_COLOR = pygame.Color("#00FF00")
APPLE_COLOR = pygame.Color("#FF0000")


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 3
    RIGHT = 4


class Element:

    def __init__(self, position, direction=None):
        self.x = position[0]
        self.y = position[1]
        self.direction = direction

    def calcDistance(self, other):
        return np.sqrt(np.power(self.x - other.x, 2) + np.power(self.y - other.y, 2))


class Snake:

    def __init__(self, window):
        self.window = window
        self.length = 1
        self.body = []
        self.body.append(Element((100, 100), Direction.DOWN))
        self.curves = []
        # every snake has his own apple to collect
        self.apple = Element((0, 0))
        self.placeApple()

    def draw(self):
        for element in self.body:
            pygame.draw.circle(self.window, SNAKE_COLOR,
                               (element.x, element.y), RADIUS)
        # apple
        pygame.draw.circle(self.window, APPLE_COLOR,
                           (int(self.apple.x), int(self.apple.y)), RADIUS)

    def changeDir(self, dir):
        self.curves.append((self.body[0].x, self.body[0].y, dir))

    def addTail(self):
        self.length += 1
        dir = self.body[-1].direction
        x = self.body[-1].x + (dir == Direction.LEFT) * \
            2 * RADIUS - (dir == Direction.RIGHT) * 2 * RADIUS
        y = self.body[-1].y + (dir == Direction.UP) * 2 * \
            RADIUS - (dir == Direction.DOWN) * 2 * RADIUS
        self.body.append(Element((x, y), dir))

    def move(self):
        # change position
        for element in self.body:
            if len(self.curves) > 0:
                for curve in self.curves:
                    if element.x == curve[0] and element.y == curve[1]:
                        element.direction = curve[2]
                        if element == self.body[-1]:
                            self.curves.remove(curve)

            element.x += -(element.direction == Direction.LEFT) * \
                SPEED + (element.direction == Direction.RIGHT) * SPEED
            element.y += -(element.direction == Direction.UP) * \
                SPEED + (element.direction == Direction.DOWN) * SPEED

        # check for collisions
        # with wall
        if self.body[0].x < 60 + RADIUS or self.body[0].x > 540 - RADIUS or self.body[0].y > 490 - RADIUS or self.body[0].y < 10 + RADIUS:
            return False
        # with body
        for element in self.body:
            if self.length > 1 and element != self.body[0] and self.body[0].calcDistance(element) < RADIUS:
                return False
        # with apple
        if self.body[0].calcDistance(self.apple) < 2*RADIUS:
            self.addTail()
            self.placeApple()

        return True

    def placeApple(self):
        self.apple.x = random.uniform(60 + RADIUS, 540 - RADIUS)
        self.apple.y = random.uniform(10 + RADIUS, 490 - RADIUS)
