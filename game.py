import pygame
from player import Player

class Game:
    def __init__(self):
        self.player1 = Player(500, 350, 1, 1)
        self.player2 = Player(780, 350, 1, 1)
        self.GRAVITY = 0.05
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()