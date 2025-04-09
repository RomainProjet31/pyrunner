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
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if game.game_over:
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            game = init_game()

    game.update(dt)
    game.draw(screen)
    pygame.display.flip()
    dt = clock.tick(30)

pygame.quit()
