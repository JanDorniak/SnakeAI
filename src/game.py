import pygame
import sys
from pygame.locals import *
from neural import NeuralNetwork
from snake import Snake
from genetic import *
from settings import *


def initWindow():
    return pygame.display.set_mode((2 * MARGIN_SIDES + BOARD_SIZE, MARGIN_TOP + MARGIN_DOWN + BOARD_SIZE))


def updateInfo(generation, alive):
    pygame.display.set_caption(
        f"Generation {generation}, snakes alive {alive}")


def drawWindow(window, alive):
    window.fill(pygame.Color(BG_COLOR))
    pygame.draw.rect(window, pygame.Color(BOARD_COLOR),
                     (BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE))
    alive.draw(window)
    pygame.display.update()


def saveGeneration(snakes, generation):
    with open("models/generation.txt", "w") as f:
        f.write(f"{generation}")
    for i in range(0, POPULATION):
        snakes[i].brain.saveWeighs(i)


def loadGeneration():
    with open("models/generation.txt", "r") as f:
        generation = int(f.readline())
    snakes = newGeneration()
    for i in range(0, POPULATION):
        snakes[i].brain.readWeighs(i)

    return snakes, generation


def main():
    draw = True
    pygame.init()
    window = initWindow()
    fps_timer = pygame.time.Clock()
    snakes = newGeneration()
    max_fps = 60
    generation = 1
    print(f"\nNew generation: {generation}")
    updateInfo(generation, POPULATION)

    while True:
        # controls
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    draw = True
                elif event.key == K_RIGHT:
                    draw = False
                elif event.key == K_s:
                    saveGeneration(snakes, generation)
                elif event.key == K_l:
                    snakes, generation = loadGeneration()
                    updateInfo(generation, POPULATION)
                elif event.key == K_UP:
                    max_fps = 60
                elif event.key == K_DOWN:
                    max_fps = 1000

        # game action
        snakes_left = 0
        alive = None
        for snake in snakes:
            if snake.active == True:
                snake.think()
                snake.move()
                snakes_left += 1
            if snake.active == True and alive == None:
                alive = snake

        # new generation
        if alive == None:
            snakes = newGeneration(False, snakes)
            print(f"\nNew generation: {generation}")
            generation += 1
            continue

        # drawing
        if draw:
            drawWindow(window, alive)
            updateInfo(generation, snakes_left)

        fps_timer.tick(max_fps)


if __name__ == "__main__":
    main()
