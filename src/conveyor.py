import pygame.sprite
from pygame import Surface

from src.sprite_constants import GRASS_SPRITE, GRASS_SIZE


class Grass(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.dest_rect = pygame.rect.Rect(x, y, GRASS_SIZE, GRASS_SIZE)
        self.image = pygame.image.load(GRASS_SPRITE)
        self.speed = 3

    def update(self, dt: int, next_width: float):
        if self.dest_rect.x + GRASS_SIZE <= 0:
            self.dest_rect.x = next_width
        self.dest_rect.x -= dt * self.speed / 100

    def draw(self, screen: Surface):
        screen.blit(self.image, self.dest_rect)


class Obstacle(pygame.sprite.Sprite):

    def update(self, dt: int):
        pass

    def draw(self, screen: Surface):
        pass


class Conveyor:
    def __init__(self, screen_size: tuple):
        self.grasses = []
        self.obstacles = []
        for i in range(int(screen_size[0] / GRASS_SIZE) + 1):  # Handle empty grass
            self.grasses.append(Grass(i * GRASS_SIZE, screen_size[1] - GRASS_SIZE))

    def update(self, dt: int):
        next_x = max(self.grasses, key=lambda curr_grass: curr_grass.dest_rect.x).dest_rect.x + GRASS_SIZE
        for grass in self.grasses:
            grass.update(dt, next_x)

    def draw(self, screen):
        for grass in self.grasses:
            grass.draw(screen)

    def collides(self, rect: pygame.rect.Rect) -> Grass | None:
        return next(
            (grass
             for grass in self.grasses
             if rect.colliderect(grass.dest_rect)),
            None
        )
