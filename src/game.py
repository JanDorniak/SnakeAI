import pygame
import sys
from pygame.locals import *
from neural import NeuralNetwork
from snake import Snake, Direction
from genetic import newGeneration
from settings import *


def initWindow():
    pygame.display.set_caption("SnakeAI")
    return pygame.display.set_mode((2 * MARGIN_SIDES + BOARD_SIZE, MARGIN_TOP + MARGIN_DOWN + BOARD_SIZE))


def updateInfo(generation):
    print(f"\nNew generation: {generation}")


def drawWindow(window, alive):
    window.fill(pygame.Color(BG_COLOR))
    pygame.draw.rect(window, pygame.Color(BOARD_COLOR),
                     (BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE))
    alive.draw(window)
    pygame.display.update()


def main():
    pygame.init()
    window = initWindow()
    fps_timer = pygame.time.Clock()
    snakes = newGeneration()
    max_fps = 60
    generation = 1
    draw = True
    updateInfo(generation)

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
                    snakes[0].brain.saveWeighs()
                elif event.key == K_UP:
                    max_fps = 60
                elif event.key == K_DOWN:
                    max_fps = 1000

        # game action
        alive = None
        for snake in snakes:
            if snake.active == True:
                snake.think()
                snake.move()
            if snake.active == True and alive == None:
                alive = snake

        # new generation
        if alive == None:
            snakes = newGeneration(False, snakes)
            updateInfo(generation)
            generation += 1
            continue

        # drawing
        if draw:
            drawWindow(window, alive)

        fps_timer.tick(max_fps)


if __name__ == "__main__":
    main()
