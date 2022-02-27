import pygame
from explosion import Explosion

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        game.box_group.add(self)

        self.health = 10
        self.img = pygame.image.load("assets/box.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width()), int(self.img.get_height())))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.health <= 0:
            self.kill()
            self.explosion()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def explosion(self):
        explosion = Explosion(self.rect.x, self.rect.y, 2, self.game)
        explosion.degats(self.game.player1.worm1, 0.075, 6)
        explosion.degats(self.game.player2.worm1, 0.075, 6)
