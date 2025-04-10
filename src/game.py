import pygame
from pygame import Surface, K_p
from pygame.event import Event

from src.cloud import Cloud, get_clouds_parallax
from src.color_manager import ColorManager
from src.conveyor import Conveyor
from src.local_text import LocalText
from src.menu import Menu
from src.player import Player
from src.simple_image import SimpleImage
from src.sprite_constants import PLAYER_SIZE, WHITE, BLACK, GRAY, RED, GAME_OVER_MUSIC, GAME_LOOP_MUSIC, NIGHT, \
    RANDOM_IMAGE, RANDOM_IMAGE_DIMENSIONS


class Game:
    def __init__(self, screen_size: tuple):
        self.started = False
        self.screen_size = screen_size
        self.conveyor = Conveyor(screen_size)
        self.color_manager = ColorManager()

        player_y = self.conveyor.grasses[0].dest_rect.y - PLAYER_SIZE + 1
        player_x = self.conveyor.grasses[3].dest_rect.x
        self.player = Player((player_x, player_y), self)
        self.last_score = 0

        self.clouds: list[Cloud] = get_clouds_parallax(screen_size)
        self.game_over = False
        self.score_text = LocalText(self.__get_ui_score_updated(), BLACK, (self.screen_size[0] / 2, 20))
        self.game_over_text = LocalText("GAME OVER", BLACK, (self.screen_size[0] / 2, self.screen_size[1] / 2), GRAY)
        self.restart_text = LocalText("Press [r] to restart", WHITE, (self.screen_size[0] / 2, self.screen_size[1] / 3))
        self.menu = Menu(screen_size)

        self.random_image = SimpleImage(
            path=RANDOM_IMAGE,
            x=2 * (screen_size[0] / 3),
            y=(2 * (screen_size[1] / 3)),
            w=RANDOM_IMAGE_DIMENSIONS[0],
            h=RANDOM_IMAGE_DIMENSIONS[1],
            jump=True
        )
        pygame.mixer.music.load(GAME_LOOP_MUSIC)
        pygame.mixer.music.play(loops=-1)

    def update(self, dt: int, events: list[Event]):
        day = self.color_manager.update(dt, self.game_over)
        if not self.menu.display:
            self.__update_game(dt, day)

        if not self.game_over:
            self.menu.update(events)

    def draw(self, screen: Surface):
        color = NIGHT if self.menu.display else None
        self.color_manager.draw(screen, color)
        if self.menu.display:
            self.menu.draw(screen)
        else:
            self.__draw_game(screen)

    def __get_ui_score_updated(self) -> str:
        return f"Score: {int(self.conveyor.conveyor_speed / 10)}"

    def __update_game(self, dt: int, day: bool):
        new_score = None
        if not self.game_over:
            self.conveyor.update(dt)
            self.player.update(dt)

            if self.last_score != self.conveyor.conveyor_speed:
                self.last_score = self.conveyor.conveyor_speed
                new_score = self.__get_ui_score_updated()

            for cloud in self.clouds:
                cloud.update(self.conveyor.conveyor_speed, self.screen_size[0], day)

            if self.player.dest_rect.right < 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(GAME_OVER_MUSIC)
                pygame.mixer.music.play()
                self.game_over = True
                self.score_text.update_color(WHITE)
                self.game_over_text.update_color(RED, BLACK)
        else:
            self.random_image.update(dt, self.screen_size)

        self.score_text.update(new_score)
        self.game_over_text.update()

    def __draw_game(self, screen: Surface):
        if not self.game_over:
            for cloud in self.clouds:
                if not cloud.is_day or not cloud.only_night:
                    cloud.draw(screen)

            self.conveyor.draw(screen)
            self.player.draw(screen)
        else:
            self.game_over_text.draw(screen)
            if self.game_over_text.color == self.game_over_text.goal_color:
                self.restart_text.draw(screen)
            self.random_image.draw(screen)

        self.score_text.draw(screen)
