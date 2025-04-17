import pygame
from pygame.locals import *

from src.managers.game import Game

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
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == QUIT or keys[K_ESCAPE]:
            running = False
            break

    if game.game_over and keys[K_r]:
        game = init_game()

    if running:
        screen.fill((0, 0, 0))
        game.update(dt, events)
        game.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)
    else:
        game.stop_game()

pygame.quit()
