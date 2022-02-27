import pygame
from PIL import Image, ImageDraw

class Evironment():
    def __init__(self, groundPath, backgroundPath):
        self.ground = Image.open(groundPath).convert("RGBA")
        self.background = Image.open(backgroundPath).convert("RGBA")
        self.actualGround = self.ground.copy().convert("RGBA")
        self.background_show = Image.alpha_composite(self.background, self.actualGround).convert('RGB')
        self.saveBackground()
        self.pygameBackground = pygame.image.load("assets/background_show.jpg")

    def updateBackgroundFusion(self, img1, img2):
        self.background_show = Image.alpha_composite(img1, img2).convert('RGB')

    def save(self, name, img):
        img.save('assets/' + name + '.png', 'PNG')

    def saveBackground(self):
        self.background_show.save("assets/background_show.jpg")

    def destruction(self, center, size):
        draw = ImageDraw.Draw(self.actualGround)
        draw.ellipse(((center[0] - size/2, center[1] - size/2), center[0] + size, center[1] + size), fill=(0, 0, 0, 0))
        self.save("ground-actual", self.actualGround)
        self.updateBackgroundFusion(self.background, self.actualGround)
        self.saveBackground()
        self.pygameBackground = pygame.image.load("assets/background_show.jpg")

    #def collision(self, player):
        #coords = self.actualGround.getpixel((player.worm1.rect.x,player.worm1.rect.y))
        #print(coords)
        #if(player.worm1.rect.y + 30 >= coords[1] and coords == (0, 0, 0, 0)):
            #player.worm1.rect.y = coords[1]
