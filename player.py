import pygame
from worm import Worm

class Player:
    def __init__(self, x, y, scale, speed):
        self.worm1 = Worm(x, y, scale, speed)

    def showWorm(self,screen, moveL, moveR, gravity):
        self.worm1.draw(screen)
        self.worm1.move(moveL, moveR, gravity)