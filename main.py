import pygame
from pygame.locals import *

from src.game import Game

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480), vsync=1)


def init_game() -> Game:
    tmp_game = Game((screen.get_width(), screen.get_height()))
    tmp_game.started = True
    return tmp_game


game = init_game()
dt = 0
running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
            running = False

    if game.game_over:
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            game = init_game()

    game.update(dt, events)

    screen.fill((0, 0, 0))
    game.draw(screen)
    pygame.display.flip()
    dt = clock.tick(30)

pygame.quit()
