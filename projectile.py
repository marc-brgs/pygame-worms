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

        self.direction = 1
        self.rotation = 0
        self.rotation_speed = randrange(2, 5)
        self.timer = 450
        self.t = 0
        #print("Grenade rotation speed :", self.rotation_speed)

    def update(self):
        self.rect.x = self.vel_x * self.t + self.x_0
        self.rect.y = -0.5 * -self.GRAVITY * self.t**2 + self.vel_y * self.t + self.y_0

        # Ancien code trajectoire
        """
        #self.vel_y += 0.05 #self.GRAVITY
        dx = self.vel_x
        dy = self.vel_y


        # Touche le sol
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.vel_x = self.vel_x * 3/4
            self.vel_y = -self.vel_y * (1/2)
            if self.rotation_speed > 0:
                self.rotation_speed -= .5

        self.rect.x = dx
        self.rect.y += dy
        """

        # Rebonds
        if self.rect.bottom > 600:
            self.t = 0
            self.x_0 = self.rect.x
            self.y_0 = self.rect.y
            self.vel_x = self.vel_x * (1 / 2)
            self.vel_y = self.vel_y * (3 / 4)
            if self.rotation_speed > 0:
                self.rotation_speed -= .5



        self.image = pygame.transform.rotate(self.img, self.rotation)
        self.rotation += self.rotation_speed

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 2, self.game)
            explosion.degats(self.game.player1.worm1)
            explosion.degats(self.game.player2.worm1)

        self.t += .05

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, game):
        super().__init__()
        game.explosion_group.add(self)

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

    def degats(self, worm):
        g_center = (self.rect.center[0], self.rect.center[1])
        w_center = (worm.rect.centerx, worm.rect.centery)

        #print(self.rect.center[0], self.rect.center[1])
        #print(worm.rect.centerx, worm.rect.centery)

        # calcul de distance en mètre dans le jeu : 10 pixel = 1 mètre
        d = round(math.sqrt((g_center[0] - w_center[0])**2 + (g_center[1] - w_center[1])**2)) /10
        #print(d)

        esperance = 0
        h_courbe_ecart = 0.1
        l_courbe_ecart = 4

        gauss = 1/(h_courbe_ecart*math.sqrt(2*math.pi)) * math.exp(-((d-esperance)**2)/(2*l_courbe_ecart)**2) *10
        #print(gauss)
        print(round(gauss))

        worm.health -= round(gauss)