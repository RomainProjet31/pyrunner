import math

import pygame
from pygame import K_SPACE, Surface, K_RIGHT, K_LEFT

from src.sprite import LocalSprite
from src.sprite.animation import Animation
from src.sprite_constants import PLAYER_JUMP_FORCE, PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_SIZE, \
    PLAYER_RUN_FRAMES_DIMENSIONS, PLAYER_SPRITE_W, PLAYER_SPRITE_H


class Player(Animation):

    def __init__(self, pos: tuple, game):
        super().__init__(pos, (PLAYER_SPRITE_W, PLAYER_SPRITE_H), True)
        self.game = game
        self.load_animation(PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_RUN_FRAMES_DIMENSIONS,
                            (PLAYER_SIZE, PLAYER_SIZE))
        # Fancy effect
        self.tick_bounce = 0
        self.bounce = False

    def update(self, dt: int, colliders: list[pygame.rect.Rect] = None):
        super().update(dt, colliders)
        self.__handle_keyboard()

        if self.bounce:
            self.__handle_bounce(dt)

    def draw(self, screen: Surface, offset: tuple[int, int] = (-16, 0)):
        if self.dest_rect.right < screen.get_width() / 2 and self.grounded and not self.collides:
            self.dest_rect.x += 1
        super().draw(screen, offset)

    def __handle_keyboard(self):
        self.vel.x = 0
        keys = pygame.key.get_pressed()
        if self.grounded and keys[K_SPACE]:
            self.vel.y = -PLAYER_JUMP_FORCE

        if keys[K_RIGHT]:
            self.vel.x = 5
        elif keys[K_LEFT]:
            self.vel.x = -5

    def __handle_bounce(self, dt: int):
        self.tick_bounce += dt
        bounce_duration = 1000
        norm = self.tick_bounce / bounce_duration  # Normaliser le temps (0 → 1)

        if norm < 0.3 and self.grounded:
            scale_x = 1 + 0.1 * math.sin(norm * math.pi * 5)
            scale_y = 1
        else:
            scale_x, scale_y = 1, 1

        if self.tick_bounce >= bounce_duration or not self.grounded:  # Fin du bounce
            self.bounce = False
            self.tick_bounce = 0

        for i in range(len(self.frames)):
            new_size = (
                int(self.original_frames[0].get_width() * scale_x), int(self.original_frames[0].get_height() * scale_y)
            )
            self.frames[i] = pygame.transform.scale(self.original_frames[i], new_size)
