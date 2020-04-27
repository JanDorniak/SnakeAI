import pygame
import numpy as np
from pygame.locals import *
from neural import NeuralNetwork
from settings import *
from utils import *


# element of snake
class Element:

    def __init__(self, position, direction=None):
        self.x = position[0]
        self.y = position[1]
        self.direction = direction

    def calcDistance(self, other):  # calc distance to other element
        return np.sqrt(np.power(self.x - other.x, 2) + np.power(self.y - other.y, 2))

    def checkCollisionWithLine(self, line):  # chceck if collides with line
        a = line[0]
        if a == None:
            return self.x - RADIUS < line[1] < self.x + RADIUS
        b = line[1]
        value = a * self.x + b
        return self.y - RADIUS < value < self.y + RADIUS


class Snake:

    def __init__(self, brain=None):
        if brain == None:
            self.brain = NeuralNetwork(NETWORK)  # new brain
        else:
            self.brain = NeuralNetwork([], brain)  # copy brain
        self.active = True
        self.ticks_alive = 0
        self.body = []
        self.body.append(Element((BOARD_LEFT + BOARD_SIZE//2,
                                  BOARD_TOP + BOARD_SIZE//2), Direction.UP))
        self.turns = []
        self.think_lock = 0
        # every snake has his own apple to collect
        self.apple = Element((0, 0))
        self.placeApple()
        self.apples_eaten = 0
        self.steps_without_apple = 0

    def draw(self, window):
        for element in self.body:
            pygame.draw.circle(window, pygame.Color(SNAKE_COLOR),
                               (element.x, element.y), RADIUS)
        # apple
        pygame.draw.circle(window, pygame.Color(APPLE_COLOR),
                           (int(self.apple.x), int(self.apple.y)), RADIUS)

    def placeApple(self):
        good_position = False
        while good_position == False:
            self.apple.x = np.random.randint(
                BOARD_LEFT + RADIUS, BOARD_RIGHT - RADIUS)
            self.apple.y = np.random.randint(
                BOARD_TOP + RADIUS, BOARD_DOWN - RADIUS)

            good_position = True
            for element in self.body:
                if self.apple.calcDistance(element) < RADIUS:
                    good_position = False
                    break

    def addTail(self):
        self.apples_eaten += 1
        dir = self.body[-1].direction
        x = self.body[-1].x + (dir == Direction.LEFT) * \
            2 * RADIUS - (dir == Direction.RIGHT) * 2 * RADIUS
        y = self.body[-1].y + (dir == Direction.UP) * 2 * \
            RADIUS - (dir == Direction.DOWN) * 2 * RADIUS
        self.body.append(Element((x, y), dir))

    def calcFitness(self):
        self.fitness = self.ticks_alive * np.power(2, self.apples_eaten)

    def changeDir(self, dir):
        if dir.value == self.body[0].direction.value * (-1) or self.body[0].direction == dir:
            return

        self.turns.append((self.body[0].x, self.body[0].y, dir))
        self.steps_without_apple += 1

    def move(self):
        self.think_lock -= 1
        self.ticks_alive += 1

        # change position
        for element in self.body:
            for turn in self.turns:
                if element.x == turn[0] and element.y == turn[1]:
                    element.direction = turn[2]
                    if element == self.body[-1]:
                        self.turns.remove(turn)

            element.x += -(element.direction == Direction.LEFT) * \
                SPEED + (element.direction == Direction.RIGHT) * SPEED
            element.y += -(element.direction == Direction.UP) * \
                SPEED + (element.direction == Direction.DOWN) * SPEED

        # check for collisions
        # with wall
        if self.body[0].x < BOARD_LEFT + RADIUS or self.body[0].x > BOARD_RIGHT - RADIUS \
                or self.body[0].y > BOARD_DOWN - RADIUS or self.body[0].y < BOARD_TOP + RADIUS:
            self.active = False
        # with body
        for element in self.body:
            if len(self.body) > 1 and element != self.body[0] and self.body[0].calcDistance(element) < RADIUS:
                self.active = False
        # with apple
        if self.body[0].calcDistance(self.apple) < 2*RADIUS:
            self.addTail()
            self.placeApple()
            self.steps_without_apple = 0

        if self.steps_without_apple > STEPS_WITHOUT_APPLE_MAX:  # 15
            self.active = False

    def think(self):
        if self.think_lock > 0:
            return

        input = self.getInputArray()
        decision = np.argmax(self.brain.predict(input))
        if decision == 0:
            self.changeDir(Direction.UP)
        elif decision == 1:
            self.changeDir(Direction.DOWN)
        elif decision == 2:
            self.changeDir(Direction.LEFT)
        elif decision == 3:
            self.changeDir(Direction.RIGHT)

        self.think_lock = THINK_LOCK

    def checkSide(self, line, condition1, condition2, dist_value, dir=None):
        inputs = [0] * 3
        head = self.body[0]
        if dir != None and head.direction.value == -1 * dir.value:
            inputs[0] = 1
        else:
            for element in self.body:
                if element != head and element.checkCollisionWithLine(line) and condition1(element):
                    inputs[0] = 1
                    break

        inputs[1] = 1 * \
            (self.apple.checkCollisionWithLine(line) and condition2)

        if line[0] == None or line[0] == 0:
            inputs[2] = 1 / (abs(dist_value) + 0.01)
        else:
            inputs[2] = 1 / checkDist(line[0], head.x,
                                      head.y, dist_value[0], dist_value[1])

        return inputs

    def getInputArray(self):
        inputs_array = []
        head = self.body[0]
        # check up
        inputs_array += self.checkSide([None, head.x],
                                       lambda element: element.y < head.y, self.apple.y < head.y, head.y - RADIUS - BOARD_TOP, Direction.UP)
        # check down
        inputs_array += self.checkSide([None, head.x],
                                       lambda element: element.y > head.y, self.apple.y > head.y, head.y + RADIUS - BOARD_DOWN, Direction.DOWN)
        # check left
        inputs_array += self.checkSide([0, head.y],
                                       lambda element: element.x < head.x, self.apple.x < head.x, head.x - RADIUS - BOARD_LEFT, Direction.LEFT)
        # check right
        inputs_array += self.checkSide([0, head.y],
                                       lambda element: element.x > head.x, self.apple.x > head.x, head.x + RADIUS - BOARD_RIGHT, Direction.RIGHT)
        # check up right
        inputs_array += self.checkSide([-1, head.y + head.x],
                                       lambda element: element.y < head.y, self.apple.y < head.y, (BOARD_RIGHT, BOARD_TOP))
        # check down left
        inputs_array += self.checkSide([-1, head.y + head.x],
                                       lambda element: element.y > head.y, self.apple.y > head.y, (BOARD_LEFT, BOARD_DOWN))
        # check up left
        inputs_array += self.checkSide([1, head.y - head.x],
                                       lambda element: element.y < head.y, self.apple.y < head.y, (BOARD_LEFT, BOARD_TOP))
        # check down right
        inputs_array += self.checkSide([1, head.y - head.x],
                                       lambda element: element.y > head.y, self.apple.y > head.y, (BOARD_RIGHT, BOARD_DOWN))

        return inputs_array
