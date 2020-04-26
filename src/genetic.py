import numpy as np
from snake import Snake
from neural import NeuralNetwork
from settings import *


def selectBest(snakes):
    snakes.sort(key=lambda x: x.fitness, reverse=True)

    return snakes[:BEST_N]


def normalizeFitness(snakes):
    total = 0
    for snake in snakes:
        snake.calcFitness()
        total += snake.fitness

    for snake in snakes:
        snake.fitness /= total

    print(f"Avg fitness: {total/POPULATION}")


def pickParent(snakes):
    r = np.random.uniform()
    sum = 0
    for i in range(0, POPULATION):
        sum += snakes[i].fitness
        if r < sum:
            parent = snakes[i]
            break

    return parent


def newGeneration(fromZero=True, snakes=None):
    newSnakes = []

    if fromZero == True:
        for i in range(0, POPULATION):
            newSnakes.append(Snake())
        return newSnakes
    else:
        normalizeFitness(snakes)
        best = selectBest(snakes)

        for snake in best:
            newSnakes.append(Snake(snake.brain))  # add copies
        snakes.reverse()

        for i in range(0, POPULATION - BEST_N):  # add mixed snakes
            parent1 = pickParent(snakes)
            parent2 = pickParent(snakes)
            brain = NeuralNetwork([], parent1.brain)
            brain.combine(parent2.brain)
            newSnakes.append(Snake(brain))

        for i in range(BEST_N, POPULATION):  # mutate snakes
            newSnakes[i].brain.mutate(MUTATION_CHANCE)

        return newSnakes
