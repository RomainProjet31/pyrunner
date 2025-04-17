import random

import pygame.sprite

from src.sprite import LocalSprite
from src.sprite.animation import Animation
from src.sprite_constants import GRASS_SPRITE, GRASS_SIZE, OBSTACLE_SIZE, OBSTACLE_SPRITE


class Conveyor:
    def __init__(self, screen_size: tuple):
        self.obstacles: list[LocalSprite] = []
        self.grasses: list[LocalSprite] = []
        self.screen_size = screen_size
        self.rand = random.Random()
        self.conveyor_speed = 5
        self.score_timer = 0
        self.obstacle_timer = 0
        self.time_level = 1000
        self.score = 0

        for i in range(int(screen_size[0] / GRASS_SIZE) + 1):  # Handle empty grass
            floor_y = screen_size[1] - GRASS_SIZE
            grass = Animation((i * GRASS_SIZE, floor_y), (GRASS_SIZE, GRASS_SIZE))
            grass.load_animation(GRASS_SPRITE, 1, (GRASS_SIZE, GRASS_SIZE))
            self.grasses.append(grass)
            if i == 5 or i == 6:
                level = 1 if i == 5 else 2
                obstacle = Animation((i * GRASS_SIZE, floor_y - GRASS_SIZE * level), (OBSTACLE_SIZE, OBSTACLE_SIZE))
                obstacle.load_animation(OBSTACLE_SPRITE, 1, (OBSTACLE_SIZE, OBSTACLE_SIZE))
                self.obstacles.append(obstacle)

    def update(self, dt: int):
        self.score_timer += dt
        if self.score_timer % self.time_level < dt:
            self.score += 1
            self.score_timer = 0
            self.time_level += 500
            if self.score % 5 == 0 and self.conveyor_speed < 10:
                self.conveyor_speed += 1

        step = self.conveyor_speed
        next_x = max(self.grasses, key=lambda curr_grass: curr_grass.dest_rect.x).dest_rect.x + GRASS_SIZE
        for grass in self.grasses:
            if grass.dest_rect.x + GRASS_SIZE <= 0:
                grass.dest_rect.x = next_x
            grass.dest_rect.x -= step

        for obstacle in self.obstacles:
            obstacle.dest_rect.x -= step
            if obstacle.dest_rect.x + obstacle.dest_rect.w <= 0:
                obstacle.alive = False

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

            obstacle = Animation((obstacle_x, self.screen_size[1] - offset_y * OBSTACLE_SIZE),
                                 (OBSTACLE_SIZE, OBSTACLE_SIZE))
            obstacle.load_animation(OBSTACLE_SPRITE, 1, (OBSTACLE_SIZE, OBSTACLE_SIZE))
            self.obstacles.append(obstacle)
            # Handle new x
            new_x = OBSTACLE_SIZE if self.rand.randint(0, 1) == 0 or last_offset_y is not None else 0
            obstacle_x += new_x
            last_offset_y = offset_y if new_x == 0 else None
