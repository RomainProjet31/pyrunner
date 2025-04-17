import math

import pygame
from pygame import K_SPACE, Surface

from src.sprite.animation import Animation
from src.sprite_constants import PLAYER_JUMP_FORCE, PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_SIZE, \
    PLAYER_RUN_FRAMES_DIMENSIONS, PLAYER_SPRITE_W, PLAYER_SPRITE_H, PLAYER_JUMP, PLAYER_JUMP_FRAMES_NUMBER


class Player(Animation):

    def __init__(self, pos: tuple, game):
        super().__init__(pos, (PLAYER_SPRITE_W, PLAYER_SPRITE_H), True)
        self.game = game
        self.jump = False
        self.load_animation(PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_RUN_FRAMES_DIMENSIONS,
                            (PLAYER_SIZE, PLAYER_SIZE))
        self.load_animation(PLAYER_JUMP, PLAYER_JUMP_FRAMES_NUMBER, PLAYER_RUN_FRAMES_DIMENSIONS,
                            (PLAYER_SIZE, PLAYER_SIZE))

        self.play(PLAYER_RUN)
        # Fancy effect
        self.tick_bounce = 0
        self.bounce = False

    def update(self, dt: int, colliders: list[pygame.rect.Rect] = None):
        grounded_before_upt = self.grounded
        super().update(dt, colliders)

        if not grounded_before_upt and self.grounded and self.jump:
            self.jump = False
            self.play(PLAYER_RUN)

        self.__move()

        if self.bounce:
            self.__handle_bounce(dt)

    def draw(self, screen: Surface, offset: tuple[int, int] = (-16, 0)):
        super().draw(screen, offset)

    def __move(self):
        self.vel.x = 0
        keys = pygame.key.get_pressed()
        fall = self.vel.y > 2
        jump = self.grounded and keys[K_SPACE]
        if jump or fall:
            if jump:
                self.vel.y = -PLAYER_JUMP_FORCE
            self.play(PLAYER_JUMP)
            self.jump = True

        # if keys[K_RIGHT]:
        #     self.vel.x = 5
        # elif keys[K_LEFT]:
        #     self.vel.x = -1
        if self.game.screen_size[0] \
                and self.dest_rect.right < self.game.screen_size[0] / 2 \
                and self.grounded:
            self.vel.x = 1

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
            og_frame = self.original_frames[self.sprite_played][i]
            new_size = (
                int(og_frame.get_width() * scale_x), int(og_frame.get_height() * scale_y)
            )
            self.frames[i] = pygame.transform.scale(og_frame, new_size)
