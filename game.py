import pygame
from player import Player

class Game:
    def __init__(self):
        self.player1 = Player(500, 350, 1, 1)
        self.player2 = Player(780, 350, 1, 1)
        self.GRAVITY = 9.81
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        
    def showHealthBar(self,screen, worm, RED):
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(worm.health), True, RED)
        screen.blit(img, (worm.rect.centerx - (img.get_width() / 2), worm.rect.top - 10))

    def aiming(self, screen, RED, worm):
        pygame.draw.line(screen, RED, (worm.rect.centerx, worm.rect.centery), (pygame.mouse.get_pos()))