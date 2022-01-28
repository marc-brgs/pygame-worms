import pygame
from random import randrange

GRAVITY = 0.05

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, force, explosion_group):
        super().__init__()
        self.timer = 450
        self.velocity_y = force[1]
        self.speed = force[0]
        self.img = pygame.image.load("assets/grenade.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width() * 0.8), int(self.img.get_height() * 0.8)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = 1
        self.rotation = 0
        self.rotation_speed = randrange(2, 5)
        self.explosion_group = explosion_group
        #print("Grenade rotation speed :", self.rotation_speed)

    def update(self):
        self.velocity_y += GRAVITY
        dx = self.speed
        dy = self.velocity_y

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.speed = self.speed * 3/4
            self.velocity_y = -self.velocity_y * (1/2)
            if self.rotation_speed > 0:
                self.rotation_speed -= .5

        self.rect.x += dx
        self.rect.y += dy

        self.image = pygame.transform.rotate(self.img, self.rotation)
        self.rotation += self.rotation_speed

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 2)
            self.explosion_group.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(f'assets/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        EXPLOSION_SPEED = 8
        #update explosion amimation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]