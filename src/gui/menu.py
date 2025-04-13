import pygame
from pygame import Surface, KEYDOWN
from pygame.locals import K_p

from src.gui.local_text import LocalText
from src.sprite_constants import WHITE, PAUSE_SOUND


class Menu:
    def __init__(self, screen_size: tuple[float, float]):
        self.screen_size = screen_size
        self.display = False
        self.start_text = LocalText("Press [SPACE] to start", WHITE, ((screen_size[0] / 2), (screen_size[1] / 2)))

        self.pause_sound = pygame.mixer.Sound(PAUSE_SOUND)

    def update(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == KEYDOWN and event.key == K_p:
                self.display = not self.display
                if self.display:
                    pygame.mixer.music.pause()
                    self.pause_sound.play()
                else:
                    pygame.mixer.music.unpause()

        self.start_text.value = "Press [r] to start"

    def draw(self, screen: Surface):
        self.start_text.draw(screen)
