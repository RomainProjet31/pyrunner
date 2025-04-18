import pygame
from pygame import Surface, KEYUP
from pygame.locals import K_p, K_SPACE

from src.game_properties_constants import Properties
from src.gui.local_text import LocalText
from src.managers.game_informations import read
from src.sprite_constants import WHITE, PAUSE_SOUND, ICON


class Menu:
    def __init__(self, screen_size: tuple[float, float], display: bool = False, compute_on_bg: bool = False):
        self.screen_size = screen_size
        self.display = display
        self.compute_on_bg = compute_on_bg

    def update(self, events: list[pygame.event.Event]):
        if self.display or self.compute_on_bg:
            self.update_events(events)

    def draw(self, screen: Surface):
        pass

    def update_events(self, events: list[pygame.event.Event]):
        pass


class PauseMenu(Menu):
    def __init__(self, screen_size: tuple[float, float]):
        super().__init__(screen_size, compute_on_bg=True)
        self.pause_text = LocalText("Press [p] to continue", WHITE, ((screen_size[0] / 2), (screen_size[1] / 2)))
        self.pause_sound = pygame.mixer.Sound(PAUSE_SOUND)

    def update(self, events: list[pygame.event.Event]):
        super().update(events)
        self.pause_text.update()

    def draw(self, screen: Surface):
        self.pause_text.draw(screen)

    def update_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == KEYUP:
                if event.key == K_p:
                    self.display = not self.display
                    if self.display:
                        pygame.mixer.music.pause()
                        self.pause_sound.play()
                    else:
                        pygame.mixer.music.unpause()


class StartMenu(Menu):
    def __init__(self, screen_size: tuple[int, int]):
        """
        TODO: Add the score view => Maybe add a generic menu system
        Is similar to PauseMenu, however the logic will change
        """
        super().__init__(screen_size, True)
        self.main_icon = pygame.image.load(ICON)
        self.main_icon_pos = ((screen_size[0] / 2) - self.main_icon.get_width() / 2, 10)

        self.pause_sound = pygame.mixer.Sound(PAUSE_SOUND)

        self.start_text = LocalText(
            "Press [SPACE] to start",
            WHITE,
            ((screen_size[0] / 2),
             self.main_icon_pos[1] + self.main_icon.get_height() + 50)
        )

        self.last_score_text = LocalText(
            f"Last score: {read(Properties.LAST_SCORE)}",
            WHITE,
            ((screen_size[0] / 3) - 10,
             self.start_text.position[1] + self.start_text.text.get_height() + 1)
        )

        self.max_score_text = LocalText(
            f"Max score: {read(Properties.MAX_SCORE)}",
            WHITE,
            (2 * (screen_size[0] / 3) + 10, self.last_score_text.position[1])
        )

    def update(self, events: list[pygame.event.Event]):
        super().update(events)
        self.start_text.update()

    def draw(self, screen: Surface):
        screen.blit(self.main_icon, self.main_icon_pos)
        self.start_text.draw(screen)
        self.last_score_text.draw(screen)
        self.max_score_text.draw(screen)

    def update_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == KEYUP and event.key == K_SPACE:
                self.display = False
                pygame.mixer.music.pause()
                self.pause_sound.play()
                pygame.mixer.music.unpause()
