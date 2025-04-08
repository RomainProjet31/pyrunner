import random

import pygame.rect
from pygame import Surface

from src.sprite_constants import CLOUD_SIZE, STAR_SIZE


class Cloud:
    def __init__(self, x: float, y: float, layer: int = 1):
        self.layer = layer
        self.is_day = True
        current_size = CLOUD_SIZE / layer
        self.center = pygame.rect.Rect(x + 2 * current_size, y, current_size, current_size)
        """
        Will help us to convert the cloud into a star
        """
        self.shape: list[pygame.rect.Rect] = [
            pygame.rect.Rect(x, y, current_size, current_size),
            pygame.rect.Rect(x + current_size, y, current_size, current_size),
            self.center,
            pygame.rect.Rect(x + 3 * current_size, y, current_size, current_size),
            # 2nd floor
            pygame.rect.Rect(x + current_size, y - current_size, current_size, current_size),
            pygame.rect.Rect(x + 2 * current_size, y - current_size, current_size, current_size),
            # Sub floor
            pygame.rect.Rect(x + current_size, y + current_size, current_size, current_size),
            pygame.rect.Rect(x + 2 * current_size, y + current_size, current_size, current_size),
        ]

    def update(self, speed: int, screen_width: int, is_day: bool):
        in_screen = False
        for r in self.shape:
            r.x -= speed / (10 * self.layer)
            if r.right >= 0:
                in_screen = True

        if not in_screen:
            for r in self.shape:
                r.x += screen_width

        self.is_day = is_day

    def draw(self, screen: Surface):
        if self.is_day:
            for r in self.shape:
                pygame.draw.rect(screen, (255, 255, 255), r)
        else:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                pygame.rect.Rect(self.center.x, self.center.y, STAR_SIZE, STAR_SIZE)
            )


def get_clouds_parallax(screen_size: tuple[float, float]) -> list[Cloud]:
    clouds = []
    nb_clouds = random.randint(4, 5)
    for _ in range(nb_clouds):
        x = random.randint(0, int(screen_size[0]))
        y = random.randint(0, int(screen_size[1] / 2))
        layer = random.randint(1, 5)
        clouds.append(Cloud(x, y, layer))
    return clouds
