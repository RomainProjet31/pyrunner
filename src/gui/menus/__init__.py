from abc import abstractmethod

import pygame
from pygame import Surface, KEYUP
from pygame.locals import K_p, K_SPACE

from src.gui.local_text import LocalText
from src.sprite_constants import WHITE, PAUSE_SOUND


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
        # if pygame.key.get_pressed()[K_p]:
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
        self.start_text = LocalText("Press [SPACE] to start", WHITE, ((screen_size[0] / 2), (screen_size[1] / 2)))
        self.pause_sound = pygame.mixer.Sound(PAUSE_SOUND)

    def update(self, events: list[pygame.event.Event]):
        super().update(events)
        self.start_text.update()

    def draw(self, screen: Surface):
        self.start_text.draw(screen)

    def update_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == KEYUP and event.key == K_SPACE:
                self.display = False
                pygame.mixer.music.pause()
                self.pause_sound.play()
                pygame.mixer.music.unpause()
