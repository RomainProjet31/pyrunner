import pygame
from pygame import Surface
from pygame.event import Event

from src.game_properties_constants import Properties
from src.gui.color_manager import ColorManager
from src.gui.local_text import LocalText
from src.gui.menus import PauseMenu, StartMenu
from src.managers.conveyor import Conveyor
from src.managers.game_informations import read, write
from src.sprite.background import Background, background_speed
from src.sprite.cloud import Cloud, get_clouds_parallax
from src.sprite.player import Player
from src.sprite.simple_image import SimpleImage
from src.sprite_constants import PLAYER_SIZE, WHITE, BLACK, GRAY, RED, GAME_OVER_MUSIC, GAME_LOOP_MUSIC, NIGHT, \
    RANDOM_IMAGE, RANDOM_IMAGE_DIMENSIONS


class Game:
    def __init__(self, screen_size: tuple):
        self.started = False
        self.screen_size = screen_size
        self.color_manager = ColorManager()
        self.conveyor = Conveyor(screen_size)
        self.bg = Background(self.screen_size)

        player_y = self.conveyor.grasses[0].dest_rect.y - PLAYER_SIZE + 1
        player_x = self.conveyor.grasses[3].dest_rect.x
        self.player = Player((player_x, player_y), self)

        self.clouds: list[Cloud] = get_clouds_parallax(screen_size)
        self.game_over = False
        self.score_text = LocalText(self.__get_ui_score_updated(), GRAY, (self.screen_size[0] / 2, 20))
        self.bg_score_text = pygame.rect.Rect(0, 0, self.screen_size[0], self.score_text.text.get_height() + 1)
        self.game_over_text = LocalText("GAME OVER", BLACK, (self.screen_size[0] / 2, self.screen_size[1] / 2), GRAY)
        self.restart_text = LocalText("Press [r] to restart", WHITE, (self.screen_size[0] / 2, self.screen_size[1] / 3))

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
        pygame.mixer.music.pause()
        self.pause_menu = PauseMenu(screen_size)
        self.start_menu = StartMenu(screen_size)

    def update(self, dt: int, events: list[Event]):
        if self.start_menu.display:
            self.start_menu.update(events)
        else:
            if not self.game_over:
                self.pause_menu.update(events)

            day = self.color_manager.update(dt, self.game_over)
            if not self.pause_menu.display:
                self.__update_game(dt, day)

    def draw(self, screen: Surface):
        color = NIGHT if self.pause_menu.display else None
        self.color_manager.draw(screen, color)

        if self.start_menu.display:
            self.start_menu.draw(screen)
        elif self.pause_menu.display:
            self.pause_menu.draw(screen)
        else:
            self.__draw_game(screen)

    def stop_game(self):
        self.__save_game()
        pygame.mixer.stop()
        self.player.alive = False

    def __save_game(self):
        if not self.start_menu.display:
            # Only when the game is over after started, otherwise it'll always be 0
            max_score = read(Properties.MAX_SCORE)
            d_props: dict[Properties, any] = {Properties.LAST_SCORE: self.conveyor.score}
            if not max_score or int(max_score) < self.conveyor.score:
                d_props.update({Properties.MAX_SCORE: self.conveyor.score})
            write(d_props)

    def __update_game(self, dt: int, day: bool):
        speed = self.conveyor.conveyor_speed
        if not self.game_over:
            self.bg.update(dt, speed)
            self.conveyor.update(dt)
            self.player.update(dt, self.conveyor.get_colliders())

            for cloud in self.clouds:
                if not cloud.only_night:
                    step = max(
                        background_speed(speed),
                        speed / cloud.layer
                    )
                else:
                    step = 1
                cloud.update(step, self.screen_size[0], day)

            if self.player.dest_rect.right < 0:
                self.player.dest_rect.x = self.screen_size[0] / 2
                pygame.mixer.music.stop()
                pygame.mixer.music.load(GAME_OVER_MUSIC)
                pygame.mixer.music.play()
                self.game_over = True
                self.__save_game()
                self.score_text.update_color(WHITE)
                self.game_over_text.update_color(RED, BLACK)
        else:
            self.random_image.update(dt, self.screen_size)

        self.score_text.value = self.__get_ui_score_updated()
        self.score_text.update()
        self.game_over_text.update()

    def __get_ui_score_updated(self) -> str:
        return f"Score: {self.conveyor.score}"

    def __draw_game(self, screen: Surface):
        if not self.game_over:
            stars = [star for star in self.clouds if star.only_night and not star.is_day]
            clouds = [cloud for cloud in self.clouds if not cloud.only_night and cloud.is_day]

            for star in stars:
                star.draw(screen)

            self.bg.draw(screen)

            for cloud in clouds:
                cloud.draw(screen)

            self.conveyor.draw(screen)
            self.player.draw(screen)
        else:
            self.game_over_text.draw(screen)
            if self.game_over_text.color == self.game_over_text.goal_color:
                self.restart_text.draw(screen)
            self.random_image.draw(screen)

        pygame.draw.rect(screen, BLACK, self.bg_score_text)
        self.score_text.draw(screen)
