import pygame.sprite
from pygame import Surface

from src.sprite_constants import GRASS_SPRITE, GRASS_SIZE


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
        self.dest_rect = pygame.rect.Rect(x, y, GRASS_SIZE, GRASS_SIZE)
        self.alive = True
        self.image = pygame.image.load(GRASS_SPRITE)

    def update(self, dt: int, conveyor_speed: int):
        self.dest_rect.x -= dt * conveyor_speed / 100
        if self.dest_rect.x + self.dest_rect.w <= 0:
            self.alive = False

    def draw(self, screen: Surface):
        screen.blit(self.image, self.dest_rect)

    def collides_left(self, center: tuple[float, float]) -> bool:
        collision_x, collision_y = self.__collision_point(center)
        x_detected = abs(collision_x - self.dest_rect.x) <= GRASS_SIZE
        y_detected = self.dest_rect.y <= collision_y <= self.dest_rect.bottom
        return x_detected and y_detected

    def collides_top(self, center: tuple[float, float]) -> bool:
        collision_x, collision_y = self.__collision_point(center)
        y_detected = abs(collision_y - self.dest_rect.y) < 10
        x_detected = self.dest_rect.x <= collision_x <= self.dest_rect.right
        return x_detected and y_detected

    def __collision_point(self, center: tuple[float, float]) -> tuple[float, float]:
        collision_x = center[0] + (center[0] - self.dest_rect.center[0]) / 2
        collision_y = center[1] + (center[1] - self.dest_rect.center[1]) / 2
        return collision_x, collision_y


class Conveyor:
    def __init__(self, screen_size: tuple):
        self.conveyor_speed = 1
        self.score_timer = 0
        self.grasses: list[Grass] = []
        self.obstacles: list[Obstacle] = []
        for i in range(int(screen_size[0] / GRASS_SIZE) + 1):  # Handle empty grass
            floor_y = screen_size[1] - GRASS_SIZE
            self.grasses.append(Grass(i * GRASS_SIZE, floor_y))
            if i == 5:
                self.obstacles.append(Obstacle(i * GRASS_SIZE, floor_y - GRASS_SIZE))

    def update(self, dt: int):
        self.score_timer += dt
        if self.score_timer % 1000 <= 30:  # Each 5 seconds
            print("upgrade")
            self.conveyor_speed += 1

        next_x = max(self.grasses, key=lambda curr_grass: curr_grass.dest_rect.x).dest_rect.x + GRASS_SIZE
        for grass in self.grasses:
            grass.update(dt, self.conveyor_speed, next_x)
        for obstacle in self.obstacles:
            obstacle.update(dt, self.conveyor_speed)

    def draw(self, screen):
        for grass in self.grasses:
            grass.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def collides_floor(self, rect: pygame.rect.Rect) -> Grass | None:
        floor = next(
            (grass for grass in self.grasses if rect.colliderect(grass.dest_rect)),
            None
        )
        if floor is None:
            floor = next(
                (obstacle for obstacle in self.obstacles if rect.colliderect(obstacle.dest_rect)),
                None
            )

        return floor

    def collides_obstacle(self, center: tuple) -> Obstacle | None:
        return next(
            (obstacle for obstacle in self.obstacles if obstacle.collides_left(center)),
            None
        )
