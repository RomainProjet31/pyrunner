from pygame import Surface

from src.conveyor import Conveyor
from src.player import Player
from src.sprite_constants import PLAYER_SIZE


class Game:
    def __init__(self, screen_size: tuple):
        self.started = False
        self.conveyor = Conveyor(screen_size)

        player_y = self.conveyor.grasses[0].dest_rect.y - PLAYER_SIZE + 1
        player_x = self.conveyor.grasses[3].dest_rect.x
        self.player = Player((player_x, player_y), self)

    def update(self, dt: int):
        self.conveyor.update(dt)
        self.player.update(dt)

    def draw(self, screen: Surface):
        self.conveyor.draw(screen)
        self.player.draw(screen)
