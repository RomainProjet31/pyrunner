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


DAY = [120, 154, 241]
NIGHT = [36, 43, 61]
current_color = [NIGHT[0], NIGHT[1], NIGHT[2]]
day_tick = 0
timer_day_changer = 150
to_day = False

game = init_game()
dt = 0
running = 1
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0

    game.update(dt)

    day_tick += dt
    if day_tick >= timer_day_changer:
        day_tick = 0
        comparator = DAY if to_day else NIGHT
        goal = True
        for i in range(len(current_color)):
            if current_color[i] < comparator[i]:
                current_color[i] += 1
                goal = False
            elif current_color[i] > comparator[i]:
                current_color[i] -= 1
                goal = False

        if goal:
            to_day = not to_day

    screen.fill((current_color[0], current_color[1], current_color[2]))
    game.draw(screen)
    pygame.display.flip()
    dt = clock.tick(30)

pygame.quit()
