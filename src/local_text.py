import pygame
from pygame import Surface


class LocalText:
    def __init__(self,
                 value: str,
                 color: list[int, int, int],
                 position: tuple[float, float],
                 background: list[int, int, int] | None = None):
        """
        :param value:
        :param color:
        :param position: Center the position depending on the size of the LocalText
        :param background:
        """
        self.game_font = pygame.font.SysFont(None, 50)
        self.value = value
        self.color = color.copy()
        self.goal_color = color.copy()
        self.background = background.copy() if background else None
        self.goal_background = background.copy() if background else None
        self.text = self.game_font.render(value, False, self.color, self.background)
        self.position = position
        self.step = 1

    def update(self, new_text: str = None):
        if new_text is not None and new_text is not self.value:
            self.value = new_text

        for i in range(len(self.color)):
            if self.color[i] < self.goal_color[i]:
                self.color[i] += self.step
            elif self.color[i] > self.goal_color[i]:
                self.color[i] -= self.step

        if self.background:
            for i in range(len(self.background)):
                if self.background[i] < self.goal_background[i]:
                    self.background[i] += self.step
                elif self.background[i] > self.goal_background[i]:
                    self.background[i] -= self.step

        self.text = self.game_font.render(self.value, False, self.color, self.background)

    def draw(self, screen: Surface):
        text_position = (self.position[0] - self.text.get_width() / 2, self.position[1] - self.text.get_height() / 2)
        screen.blit(self.text, text_position)

    def update_color(self, color: list[int, int, int], background: list[int, int, int] | None = None):
        self.goal_color = color.copy()
        self.goal_background = background.copy() if background else None
