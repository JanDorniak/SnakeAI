import pygame
from pygame.locals import *
import sys
import neural
from snake import Snake, Direction


MAX_FPS = 60
BG_COLOR = pygame.Color('#575757')
BOARD_COLOR = pygame.Color('#FFFFFF')


def initWindow():
    pygame.display.set_caption("Snake")
    return pygame.display.set_mode((600, 600))


def initSnake(window):
    return Snake(window)


def main():
    pygame.init()
    window = initWindow()
    fps_timer = pygame.time.Clock()
    snake = initSnake(window)

    while True:

        # controls
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    snake.changeDir(Direction.LEFT)
                elif event.key == K_RIGHT:
                    snake.changeDir(Direction.RIGHT)
                elif event.key == K_UP:
                    snake.changeDir(Direction.UP)
                elif event.key == K_DOWN:
                    snake.changeDir(Direction.DOWN)

        # game action
        if snake.move() == False:
            pygame.quit()

        # drawing
        window.fill(BG_COLOR)
        pygame.draw.rect(window, BOARD_COLOR,
                         (60, 10, 480, 480))
        snake.draw()
        pygame.display.update()

        # print(fps_timer.get_fps())
        fps_timer.tick(MAX_FPS)


if __name__ == "__main__":
    main()
