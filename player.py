import pygame
from worm import Worm

name_list = ["Bobby", "Joe", "Sam", "Timmy", "Bob"]
name_index = 0

class Player:
    def __init__(self, game, x, y, color):
        global name_list
        global name_index
        self.game = game
        self.color = color
        if len(name_list) == name_index:
            name_index -= 1
            name_list[name_index] = "Autogen"
        self.worm1 = Worm(self.game, name_list[name_index], x, y, 1, 1, self.color)
        name_index += 1

    def showWorm(self, screen, moveL, moveR):
        self.worm1.draw(screen)
        self.worm1.showName(screen)
        self.worm1.showHealthBar(screen)
        self.worm1.move(moveL, moveR)