import math

import pygame
from random import randrange

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
            explosion.degats(self.game.player1.worm1, 0.1, 4)
            explosion.degats(self.game.player2.worm1, 0.1, 4)
            for e in self.game.box_group:
                explosion.degats(e, 0.1, 4)

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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, game):
        super().__init__()
        game.explosion_group.add(self)
        game.end_turn = True
        self.images = []
        for i in range(1, 8):
            img = pygame.image.load(f"assets/explosion/exp{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.img_index = 0
        self.image = self.images[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.EXPLOSION_SPEED = 8 # Plus grand = plus long
        self.compteur = 0


    def update(self):
        self.compteur += 1

        # Changement d'image
        if self.compteur >= self.EXPLOSION_SPEED:
            self.compteur = 0
            self.img_index += 1
            # Test fin animation sinon change l'image courante
            if self.img_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.img_index]

    def degats(self, element, h_courbe_ecart, l_courbe_ecart):
        g_center = (self.rect.center[0], self.rect.center[1])
        w_center = (element.rect.centerx, element.rect.centery)

        #print(self.rect.center[0], self.rect.center[1])
        #print(worm.rect.centerx, worm.rect.centery)

        # calcul de distance en mètre dans le jeu : 10 pixel = 1 mètre
        d = round(math.sqrt((g_center[0] - w_center[0])**2 + (g_center[1] - w_center[1])**2)) /10
        #print(d)

        esperance = 0

        gauss = 1/(h_courbe_ecart*math.sqrt(2*math.pi)) * math.exp(-((d-esperance)**2)/(2*l_courbe_ecart)**2) *10

        #print(round(gauss))

        #print(element.health)

        element.health -= round(gauss)
        if element.health <= 0:
            element.health = 0