import pygame
from pygame.locals import *

from src.game import Game

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))


def init_game() -> Game:
    tmp_game = Game((screen.get_width(), screen.get_height()))
    tmp_game.started = True
    return tmp_game


game = init_game()
dt = 0
running = 1
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0

    game.update(dt)
    screen.fill((0, 0, 0))
    game.draw(screen)
    pygame.display.flip()
    dt = clock.tick(30)

pygame.quit()
