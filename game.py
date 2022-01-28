import pygame
from player import Player

class Game:
    def __init__(self):
        self.player = Player(500, 350, 1, 1)
        self.pressed = {} #dict
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()