import pygame.sprite
from pygame import Surface


class LocalSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple, collides: bool = False):
        """
        pos (tuple): The default position of the sprite on the screen
        size (tuple): Its size WxH
        collides (bool): Either it will be a collider (with gravity fall) or not
        """
        super().__init__()
        self.alive = True
        self.grounded = True
        self.collides = collides
        self.vel = pygame.math.Vector2(0, 0)
        self.dest_rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])

    def update(self, dt: int, colliders: list[pygame.rect.Rect] = None) -> None:
        if self.collides and colliders:
            self.__compute_collision(colliders)
            if not self.grounded:
                self.vel.y += dt / 10
        else:
            self.dest_rect.x += self.vel.x
            self.dest_rect.y += self.vel.y

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, (255, 255, 255), self.dest_rect)

    def __compute_collision(self, world_colliders: list[pygame.rect.Rect]):
        print(f"Au début {self.vel}")
        self.dest_rect.x += self.vel.x
        for rect in world_colliders:
            if self.dest_rect.colliderect(rect):
                if self.vel.x >= 0:
                    self.dest_rect.x = rect.left - self.dest_rect.w
                elif self.vel.x < 0:
                    self.dest_rect.left = rect.right
                self.vel.x = 0

        self.dest_rect.y += self.vel.y
        self.grounded = False
        for rect in world_colliders:
            if self.dest_rect.colliderect(rect):
                if self.vel.y > 0:
                    self.dest_rect.bottom = rect.top
                    self.grounded = True
                elif self.vel.y < 0:
                    self.dest_rect.top = rect.bottom
                self.vel.y = 0
        print(f"A la fin {self.vel}")
