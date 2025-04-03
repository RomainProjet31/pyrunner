import pygame.font
from pygame import Surface

from src.conveyor import Conveyor
from src.player import Player
from src.sprite_constants import PLAYER_SIZE


class Game:
    def __init__(self, screen_size: tuple):
        self.started = False
        self.conveyor = Conveyor(screen_size)
        self.game_font = pygame.font.SysFont('Comic Sans Ms', 30)
        self.score = self.__get_ui_score_updated()

        player_y = self.conveyor.grasses[0].dest_rect.y - PLAYER_SIZE + 1
        player_x = self.conveyor.grasses[3].dest_rect.x
        self.player = Player((player_x, player_y), self)
        self.last_score = 0

    def update(self, dt: int):
        self.conveyor.update(dt)
        self.player.update(dt)

        if self.last_score != self.conveyor.conveyor_speed:
            print("upgrade")
            self.last_score = self.conveyor.conveyor_speed
            self.score = self.__get_ui_score_updated()

    def draw(self, screen: Surface):
        self.conveyor.draw(screen)
        self.player.draw(screen)
        screen.blit(self.score, (10, 10))

    def __get_ui_score_updated(self) -> Surface:
        return self.game_font.render(f"{self.conveyor.conveyor_speed}", False, (255, 255, 255))
