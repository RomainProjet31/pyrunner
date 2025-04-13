import pygame
from pygame import Surface

from src.sprite import LocalSprite


class Animation(LocalSprite):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], collides: bool = False):
        super().__init__(pos, size, collides)
        self.idx_frame = 0
        self.nb_frames = 0
        self.animation_tick = 0
        self.frames = []
        self.sprite_sheet = None
        self.slowness_factor = 3
        self.original_frames = []

    def update(self, dt: int, colliders: list[pygame.rect.Rect] = None) -> None:
        super().update(dt, colliders)
        self.idx_frame = int(
            (pygame.time.get_ticks() / (60 * self.slowness_factor)) % self.nb_frames) if dt > 0 else 0

    def draw(self, screen: Surface, offset: tuple[int, int] = (0, 0)) -> None:
        screen.blit(self.frames[self.idx_frame], (self.dest_rect.x + offset[0], self.dest_rect.y - offset[1]))

    def load_animation(self, sprite_sheet_path: str, nb_frames: int, dimension: tuple, scale_dimension: tuple = None):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.nb_frames = nb_frames
        self.frames.clear()
        self.idx_frame = 0

        for f in range(self.nb_frames):
            # Take it
            frame = self.sprite_sheet.subsurface((f * dimension[0], 0, dimension[0], dimension[1]))
            # Scale it if needed
            scale = scale_dimension if scale_dimension else dimension
            scaled_frame = pygame.transform.scale(frame, (scale[0], scale[1]))
            # Store it
            self.frames.append(scaled_frame)
            self.original_frames.append(scaled_frame)  # Avoid scaling bugs during the bounce process
