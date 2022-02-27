import pygame
from random import randrange
from explosion import Explosion

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, force, game):
        super().__init__()
        game.grenade_group.add(self)

        self.game = game
        self.GRAVITY = game.GRAVITY

        self.img = pygame.image.load("assets/grenade.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width() * 0.8), int(self.img.get_height() * 0.8)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x_0 = x
        self.y_0 = y


        self.vel_x = force[0]
        self.vel_y = force[1]

        self.direction_x = 1
        self.direction_y = 1

        self.rotation = 0
        self.rotation_speed = randrange(2, 5)
        self.timer = 450
        self.t = 0
        #print("Grenade rotation speed :", self.rotation_speed)

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y

        # Equation de trajectoire sans frottements
        self.rect.x = self.vel_x * self.t + self.x_0
        self.rect.y = -0.5 * -self.GRAVITY * self.t**2 + self.vel_y * self.t + self.y_0

        # Detection direction
        if (self.rect.x - old_x) > 0:
            self.direction_x = 1
        else:
            self.direction_x = -1
        if(self.rect.y - old_y) > 0:
            self.direction_y = 1
        else:
            self.direction_y = -1

        # Rebonds
        if self.rect.bottom > 600 and self.direction_y > 0:
            self.rect.bottom = 600
            self.resetThrow()
            self.vel_x = self.vel_x * (3 / 4)
            self.vel_y = -abs(self.vel_y) * (3 / 4)
            if self.rotation_speed > 0:
                self.rotation_speed -= .5

        # Box and worm collision
        self.grenadeCollisionWith(self.game.box_group)
        self.grenadeCollisionWith(self.game.worm_group)

        self.image = pygame.transform.rotate(self.img, self.rotation)
        self.rotation += self.rotation_speed

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 2, self.game)
            explosion.degats(self.game.player1.worm1, 0.1, 4, self.game)
            explosion.degats(self.game.player2.worm1, 0.1, 4, self.game)
            for e in self.game.box_group:
                explosion.degats(e, 0.1, 4, self.game)

        self.t += .05

    def grenadeCollisionWith(self, element_group):
        collision_tolerance = 10
        for element in element_group:
            if self.rect.colliderect(element.rect):
                if abs(element.rect.top - self.rect.bottom) < collision_tolerance and self.direction_y > 0:
                    self.resetThrow()
                    self.vel_x = self.vel_x * (3 / 4)
                    self.vel_y = -self.vel_y * (3 / 4)
                if abs(element.rect.bottom - self.rect.top) < collision_tolerance and self.direction_y < 0:
                    self.resetThrow()
                    self.vel_x = self.vel_x * (3 / 4)
                    self.vel_y = -self.vel_y * (3 / 4)
                if abs(element.rect.right - self.rect.left) < collision_tolerance and self.direction_x < 0:
                    self.resetThrow()
                    self.vel_x = -self.vel_x * (3 / 4)
                    self.vel_y = self.vel_y * (3 / 4)
                if abs(element.rect.left - self.rect.right) < collision_tolerance and self.direction_x > 0:
                    self.resetThrow()
                    self.vel_x = -self.vel_x * (3 / 4)
                    self.vel_y = self.vel_y * (3 / 4)

    def resetThrow(self):
        self.t = 0
        self.x_0 = self.rect.x
        self.y_0 = self.rect.y