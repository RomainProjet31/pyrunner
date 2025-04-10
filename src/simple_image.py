import pygame.sprite
from pygame import Surface


class SimpleImage(pygame.sprite.Sprite):

    def __init__(self, path: str, x: int, y: int, w: int, h: int, jump: bool = False):
        super().__init__()
        self.dest_rec = pygame.rect.Rect(x, y, w, h)
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (w, h))
        self.flipped = False

        self.jump = jump
        self.step_x = 5
        self.max_jump = 50

        if self.jump:
            x = self.step_x
            y = self.max_jump
        else:
            x = 0
            y = 0
        self.vel = pygame.math.Vector2(x, y)

    def update(self, dt: int, screen: tuple[int, int]):
        if self.jump:
            self.vel.y -= dt / 5
            if self.dest_rec.bottom >= screen[1]:
                self.vel.y = self.max_jump

            if self.dest_rec.x < 0:
                self.vel.x = self.step_x
            elif self.dest_rec.right >= screen[0]:
                self.vel.x = -self.step_x

            if (self.dest_rec.centerx <= screen[0] / 2 and self.vel.x < 0 and not self.flipped) or (
                    self.dest_rec.centerx > screen[0] / 2 and self.vel.x > 0 and self.flipped):
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = not self.flipped

        self.dest_rec.x += self.vel.x
        self.dest_rec.y -= self.vel.y

    def draw(self, screen: Surface):
        screen.blit(self.image, self.dest_rec)
