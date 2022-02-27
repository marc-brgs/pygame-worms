import pygame
import math
from PIL import Image, ImageDraw

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

    def degats(self, element, h_courbe_ecart, l_courbe_ecart, game):
        g_center = (self.rect.center[0], self.rect.center[1])
        w_center = (element.rect.centerx, element.rect.centery)

        game.environment.destruction(g_center, 100)
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