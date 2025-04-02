import math

import pygame.sprite
from pygame import K_SPACE, Surface

from src.sprite_constants import PLAYER_JUMP_FORCE, PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_SIZE, \
    PLAYER_RUN_FRAMES_DIMENSIONS


class Player(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, game):
        super().__init__()
        self.game = game
        self.dest_rect = pygame.rect.Rect(pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE)
        self.current_thrust = 0
        self.animation_tick = 0
        self.nb_frames = 0
        self.sprite_sheet = None
        self.frames = []
        self.original_frames = []
        self.idx_frame = 0
        self.slowness_factor = 3
        self.__init_animations(PLAYER_RUN, PLAYER_RUN_FRAMES_NUMBER, PLAYER_RUN_FRAMES_DIMENSIONS)
        self.bounce = False
        self.tick_bounce = 0
        self.grounded = True

    def update(self, dt: int):
        # Know if we are falling or not
        self.grounded = self.game.conveyor.collides_floor(self.dest_rect) is not None

        self.__handle_y_direction(dt)

        # if not self.bounce:
        self.idx_frame = int(
            (pygame.time.get_ticks() / (60 * self.slowness_factor)) % self.nb_frames) if dt > 0 else 0

        if not self.grounded:
            collider = self.game.conveyor.collides_floor(self.dest_rect)
            if collider is not None:
                self.ground_touched(collider.dest_rect)

        obstacle = self.game.conveyor.collides_obstacle(self.dest_rect.center)
        if obstacle is not None:
            self.dest_rect.x = obstacle.dest_rect.x - self.dest_rect.w

        if self.bounce:
            self.__handle_bounce(dt)

    def draw(self, screen: Surface):
        screen.blit(self.frames[self.idx_frame], (self.dest_rect.x, self.dest_rect.y))

    def ground_touched(self, rect: pygame.rect.Rect):
        self.dest_rect.y = rect.y - self.dest_rect.h + 1
        self.current_thrust = 0
        self.grounded = True
        self.bounce = True

    def __handle_y_direction(self, dt: int):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and self.current_thrust == 0:
            self.current_thrust = PLAYER_JUMP_FORCE
        elif not self.grounded:
            self.current_thrust -= dt / 5

        self.dest_rect.y -= self.current_thrust

    def __handle_bounce(self, dt: int):
        self.tick_bounce += dt
        bounce_duration = 1000
        norm = self.tick_bounce / bounce_duration  # Normaliser le temps (0 → 1)

        if norm < 0.3 and self.grounded:
            scale_x = 1 + 0.2 * math.sin(norm * math.pi * 4)
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

    def __init_animations(self, sprite_sheet_path: str, nb_frames: int, dimension: tuple):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.nb_frames = nb_frames
        self.frames.clear()
        self.idx_frame = 0

        for f in range(self.nb_frames):
            frame = self.sprite_sheet.subsurface((f * dimension[0], 0, dimension[0], dimension[1]))
            scaled_frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))
            self.frames.append(scaled_frame)
            self.original_frames.append(scaled_frame)  # Avoid scaling bugs during the bounce process
