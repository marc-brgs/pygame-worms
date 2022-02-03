import pygame
from player import Player

import math

class Game:
    def __init__(self):
        self.GRAVITY = 9.81
        self.player1 = Player(500, 350, (255, 0, 0))
        self.player2 = Player(780, 350, (0, 0, 255))
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

    def aiming(self, screen, RED, worm):
        WHITE = (255, 255, 255)
        worm_to_cursor = (pygame.mouse.get_pos()[0] - worm.rect.centerx, pygame.mouse.get_pos()[1]-30 - worm.rect.centery)
        x_0 = worm.rect.centerx
        y_0 = worm.rect.centery

        #print(vector[0]);
        factor = 5
        direction_x = 1
        direction_y = 1
        if worm_to_cursor[0] < 0:
            direction_x = -1
        if worm_to_cursor[1] < 0:
            direction_y = -1

        #linear
        #v = (worm_to_cursor[0]/2, worm_to_cursor[1]/2)
        # square root
        #v = (factor * direction_x * math.sqrt(abs(worm_to_cursor[0])), factor * direction_y * math.sqrt(abs(worm_to_cursor[1])))
        # ease out sine
        if abs(worm_to_cursor[0]/300) > 1:
            worm_to_cursor = (direction_x * 300, worm_to_cursor[1])
        if abs(worm_to_cursor[1]/300) > 1:
            worm_to_cursor = (worm_to_cursor[0], direction_y * 300)
        v = (100 * direction_x * math.sin((abs(worm_to_cursor[0]/300) * math.pi) / 2), 100 * direction_y * math.sin((abs(worm_to_cursor[1]/300) * math.pi) / 2))
        v_norme = math.sqrt(v[0] ** 2 + v[1] ** 2)

        size = 8
        t = .5
        while t <= 5:
            x = v[0] * t + x_0
            y = -0.5 * -self.GRAVITY * t ** 2 + v[1] * t + y_0
            point = pygame.Rect(x, y, size, size)
            pygame.draw.ellipse(screen, WHITE, point, 0)
            t += .5
            size -= .2

        #pygame.draw.line(screen, WHITE, (worm.rect.centerx, worm.rect.centery), (pygame.mouse.get_pos()))