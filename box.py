import pygame
import math

import game
from projectile import Explosion

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.health = 10
        self.img = pygame.image.load("assets/box.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width()), int(self.img.get_height())))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def explosion(self, game):
        if self.health <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 2, game)
            explosion.degats(game.player1.worm1, 0.075, 6)
            explosion.degats(game.player2.worm1, 0.075, 6)
