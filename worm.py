import pygame
from projectile import Grenade

class Worm(pygame.sprite.Sprite):
    def __init__(self, name, x, y, scale, speed, color):
        super().__init__() # init Sprite
        self.name = name
        self.PLAYER_COLOR = color
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.speed = speed
        self.velocity_y = 0
        img = pygame.image.load("assets/worm_p1.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = True
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.projectile = pygame.sprite.Group()

    def showName(self, screen):
        font = pygame.font.SysFont("consolas", 17)
        img = font.render(str(self.name), True, self.PLAYER_COLOR)
        screen.blit(img, (self.rect.centerx - (img.get_width() / 2), self.rect.top - 30))

    def showHealthBar(self,screen):
        font = pygame.font.SysFont("consolas", 17)
        img = font.render(str(self.health), True, self.PLAYER_COLOR)
        screen.blit(img, (self.rect.centerx - (img.get_width() / 2), self.rect.top - 10))

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right, GRAVITY):
        dx = 0
        dy = 0
        if (pygame.mouse.get_pos()[0] - self.rect.centerx) < 0:
            self.flip = False
            self.direction = -1
        else:
            self.flip = True
            self.direction = 1
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1
        if self.jump:
            self.velocity_y = -3
            self.jump = False
            self.in_air = True

        self.velocity_y += 0.05 #GRAVITY

        dy += self.velocity_y

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def launch_grenade(self):
        self.projectile.add(Grenade())