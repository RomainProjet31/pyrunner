import pygame.font
from pygame import Surface

from src.Cloud import Cloud, get_clouds_parallax
from src.conveyor import Conveyor
from src.player import Player
from src.sprite_constants import PLAYER_SIZE


class Game:
    def __init__(self, screen_size: tuple):
        self.started = False
        self.screen_size = screen_size
        self.conveyor = Conveyor(screen_size)
        self.game_font = pygame.font.SysFont('Comic Sans Ms', 30)
        self.score = self.__get_ui_score_updated()

        player_y = self.conveyor.grasses[0].dest_rect.y - PLAYER_SIZE + 1
        player_x = self.conveyor.grasses[3].dest_rect.x
        self.player = Player((player_x, player_y), self)
        self.last_score = 0
        self.clouds: list[Cloud] = get_clouds_parallax(screen_size)

    def update(self, dt: int, day: bool):
        self.conveyor.update(dt)
        self.player.update(dt)

        if self.last_score != self.conveyor.conveyor_speed:
            print("upgrade")
            self.last_score = self.conveyor.conveyor_speed
            self.score = self.__get_ui_score_updated()

        for cloud in self.clouds:
            cloud.update(self.conveyor.conveyor_speed, self.screen_size[0], day)

    def draw(self, screen: Surface):
        for cloud in self.clouds:
            cloud.draw(screen)

        self.conveyor.draw(screen)
        self.player.draw(screen)
        screen.blit(self.score, (10, 10))

    def __get_ui_score_updated(self) -> Surface:
        return self.game_font.render(f"{self.conveyor.conveyor_speed}", False, (255, 255, 255))
