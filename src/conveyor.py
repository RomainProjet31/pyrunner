import random

import pygame.sprite
from pygame import Surface

from src.sprite_constants import GRASS_SPRITE, GRASS_SIZE, OBSTACLE_SIZE, OBSTACLE_SPRITE


class Grass(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.dest_rect = pygame.rect.Rect(x, y, GRASS_SIZE, GRASS_SIZE)
        self.image = pygame.image.load(GRASS_SPRITE)

    def update(self, dt: int, conveyor_speed: int, next_width: float):
        if self.dest_rect.x + GRASS_SIZE <= 0:
            self.dest_rect.x = next_width
        self.dest_rect.x -= dt * conveyor_speed / 100

    def draw(self, screen: Surface):
        screen.blit(self.image, self.dest_rect)


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x: float, y: float):
        super().__init__()
        self.dest_rect = pygame.rect.Rect(x, y, OBSTACLE_SIZE, OBSTACLE_SIZE)
        self.alive = True
        self.image = pygame.image.load(OBSTACLE_SPRITE)

    def update(self, dt: int, conveyor_speed: int):
        self.dest_rect.x -= dt * conveyor_speed / 100
        if self.dest_rect.x + self.dest_rect.w <= 0:
            self.alive = False

    def draw(self, screen: Surface):
        screen.blit(self.image, self.dest_rect)


class Conveyor:
    def __init__(self, screen_size: tuple):
        self.obstacles: list[Obstacle] = []
        self.grasses: list[Grass] = []
        self.screen_size = screen_size
        self.rand = random.Random()
        self.conveyor_speed = 10
        self.score_timer = 0
        self.obstacle_timer = 0

        for i in range(int(screen_size[0] / GRASS_SIZE) + 1):  # Handle empty grass
            floor_y = screen_size[1] - GRASS_SIZE
            self.grasses.append(Grass(i * GRASS_SIZE, floor_y))
            if i == 5:
                self.obstacles.append(Obstacle(i * GRASS_SIZE, floor_y - GRASS_SIZE))
            elif i == 6:
                self.obstacles.append(Obstacle(i * GRASS_SIZE, floor_y - GRASS_SIZE * 2))

    def update(self, dt: int):
        self.score_timer += dt
        if self.score_timer % 1000 <= 30:  # Each 5 seconds
            self.conveyor_speed += 1

        next_x = max(self.grasses, key=lambda curr_grass: curr_grass.dest_rect.x).dest_rect.x + GRASS_SIZE
        for grass in self.grasses:
            grass.update(dt, self.conveyor_speed, next_x)
        for obstacle in self.obstacles:
            obstacle.update(dt, self.conveyor_speed)

        if self.obstacle_timer > 1000:
            if self.rand.randint(1, 3) == 3:
                self.__add_obstacle()
            self.obstacle_timer = 0
        else:
            self.obstacle_timer += dt

    def draw(self, screen):
        for grass in self.grasses:
            grass.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def get_colliders(self) -> list[pygame.rect.Rect]:
        result = []
        for obstacle in self.obstacles:
            result.append(obstacle.dest_rect)
        for grass in self.grasses:
            result.append(grass.dest_rect)
        return result

    def __add_obstacle(self):
        obstacle_x = max(self.screen_size[0], max([o.dest_rect.x for o in self.obstacles]))
        last_offset_y = None
        max_x = self.rand.randint(1, 4) * OBSTACLE_SIZE + self.screen_size[0]
        while obstacle_x < max_x:
            if last_offset_y is not None:
                offset_y = 2 if last_offset_y == 3 else 3
            else:
                offset_y = 2 if self.rand.randint(10, 20) <= 15 else 3

            self.obstacles.append(Obstacle(obstacle_x, self.screen_size[1] - offset_y * OBSTACLE_SIZE))
            # Handle new x
            new_x = OBSTACLE_SIZE if self.rand.randint(0, 1) == 0 or last_offset_y is not None else 0
            obstacle_x += new_x
            last_offset_y = offset_y if new_x == 0 else None
