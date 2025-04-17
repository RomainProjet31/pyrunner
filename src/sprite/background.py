from pygame import Surface

from src.sprite.animation import Animation
from src.sprite_constants import BACKGROUND_IMAGE, BACKGROUND_DIMENSIONS, GRASS_SIZE


class Background:
    def __init__(self, screen_size: tuple[int, int] = None):
        self.screen_size = screen_size
        self.first = Animation((0, 0), (screen_size[0], screen_size[1]))
        self.second = Animation((self.first.dest_rect.right, 0), (screen_size[0], screen_size[1]))

        bg_dest_size = (screen_size[0], screen_size[1] - GRASS_SIZE)
        self.first.load_animation(BACKGROUND_IMAGE, 1, BACKGROUND_DIMENSIONS, bg_dest_size)
        self.second.load_animation(BACKGROUND_IMAGE, 1, BACKGROUND_DIMENSIONS, bg_dest_size)

    def update(self, dt: int, conveyor_speed: int) -> None:
        self.first.update(dt)
        step = background_speed(conveyor_speed)
        self.first.dest_rect.x -= step
        if self.first.dest_rect.right <= 0:
            self.first.dest_rect.x = self.screen_size[0]

        self.second.update(dt)
        self.second.dest_rect.x -= step
        if self.second.dest_rect.right <= 0:
            self.second.dest_rect.x = self.screen_size[0]

    def draw(self, screen: Surface) -> None:
        self.first.draw(screen)
        self.second.draw(screen)


def background_speed(conveyor_speed: int) -> int:
    return max(1, int(conveyor_speed / 50.0))
