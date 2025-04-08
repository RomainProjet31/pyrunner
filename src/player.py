import math

import pygame.sprite
from pygame import K_SPACE, Surface, K_RIGHT, K_LEFT

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
        self.collides = False
        self.feet = pygame.rect.Rect(0, 0, 0, 0)
        self.head = pygame.rect.Rect(0, 0, 0, 0)
        self.right = pygame.rect.Rect(0, 0, 0, 0)
        self.left = pygame.rect.Rect(0, 0, 0, 0)

    def update(self, dt: int):
        self.__handle_y_direction(dt)
        self.__compute_side_collision()
        self.idx_frame = int(
            (pygame.time.get_ticks() / (60 * self.slowness_factor)) % self.nb_frames) if dt > 0 else 0
        if self.bounce:
            self.__handle_bounce(dt)

    def draw(self, screen: Surface):
        if self.dest_rect.right < screen.get_width() / 2 and self.grounded and not self.collides:
            self.dest_rect.x += 1

        screen.blit(self.frames[self.idx_frame], (self.dest_rect.x, self.dest_rect.y))
        # self.__draw_debug_sides(screen)

    def __draw_debug_sides(self, screen: Surface):
        pygame.draw.rect(screen, (15, 150, 10), self.head)
        pygame.draw.rect(screen, (15, 150, 10), self.right)
        pygame.draw.rect(screen, (15, 150, 10), self.feet)
        pygame.draw.rect(screen, (15, 150, 10), self.left)

    def ground_touched(self, rect: pygame.rect.Rect):
        self.dest_rect.y = rect.y - self.dest_rect.h + 1
        self.current_thrust = 0
        self.grounded = True
        self.bounce = True

    def __compute_side_collision(self):
        rects = self.game.conveyor.get_colliders()

        if self.current_thrust >= 0:
            self.__check_top(rects)
            self.__check_feet(rects)
        else:
            self.__check_feet(rects)
            self.__check_top(rects)

        self.right = pygame.rect.Rect(
            self.dest_rect.x + 2 * self.dest_rect.w / 3,
            self.dest_rect.y + self.dest_rect.h / 3,
            self.dest_rect.w / 3,
            self.dest_rect.h / 3
        )
        self.left = pygame.rect.Rect(
            self.dest_rect.x,
            self.dest_rect.y + self.dest_rect.h / 3,
            self.dest_rect.w / 3,
            self.dest_rect.h / 3
        )
        right_collision_idx = self.right.collidelist(rects)
        left_collision_idx = self.left.collidelist(rects)

        if right_collision_idx != -1:
            self.dest_rect.x = rects[right_collision_idx].x - self.dest_rect.w - 1

        if left_collision_idx != -1:
            self.dest_rect.x = rects[left_collision_idx].right + 1

    def __check_top(self, colliders: list[pygame.rect.Rect]):
        self.head = pygame.rect.Rect(
            self.dest_rect.x + self.dest_rect.w / 3,
            self.dest_rect.y,
            self.dest_rect.w / 3,
            self.dest_rect.h / 3
        )
        head_collision_idx = self.head.collidelist(colliders)
        if head_collision_idx != -1:
            self.current_thrust = 0
            self.dest_rect.y = colliders[head_collision_idx].bottom + 10

    def __check_feet(self, colliders: list[pygame.rect.Rect]):
        self.feet = pygame.rect.Rect(
            self.dest_rect.x + self.dest_rect.w / 3,
            self.dest_rect.y + 2 * self.dest_rect.h / 3,
            self.dest_rect.w / 3,
            self.dest_rect.h / 3
        )
        feet_collision_idx = self.feet.collidelist(colliders)
        self.grounded = feet_collision_idx != -1
        if self.grounded:
            self.current_thrust = 0
            self.dest_rect.y = colliders[feet_collision_idx].y - self.dest_rect.h

    def __handle_y_direction(self, dt: int):
        keys = pygame.key.get_pressed()

        if not self.grounded:
            self.current_thrust -= dt / 3
        elif keys[K_SPACE]:
            self.current_thrust = PLAYER_JUMP_FORCE

        self.dest_rect.y -= self.current_thrust

        if keys[K_RIGHT]:
            self.dest_rect.x += 10
        elif keys[K_LEFT]:
            self.dest_rect.x -= 10

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
