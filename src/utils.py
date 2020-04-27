import numpy as np
from enum import Enum
from settings import *


class Direction(Enum):
    DOWN = 1
    UP = -1
    LEFT = 2
    RIGHT = -2


def checkUDIntersect(x, y, a, cory):  # ret x
    return (cory - y + a*x)/a


def checkLRIntersect(x, y, a, corx):  # ret y
    return corx*a + y - a*x


def checkDist(a, hx, hy, corx, cory):

    if BOARD_LEFT < checkUDIntersect(hx, hy, a, cory) < BOARD_RIGHT:
        x = checkUDIntersect(hx, hy, a, cory)
        y = cory
    else:
        x = corx
        y = checkLRIntersect(hx, hy, a, corx)

    return np.sqrt((hx - x)**2 + (hy - y)**2)


def saveAvgFitness(value):
    with open("other/avgfitness.csv", "a") as file:
        file.write(str(value) + ',')
