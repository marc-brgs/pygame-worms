import pygame
import constant_dispenser

#groundForMask = pygame.image.load("assets/ground-actual.png")
#groundMask = pygame.mask.from_surface(groundForMask)

class Worm(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, scale, speed, color):
        super().__init__() # init Sprite
        self.game = game
        game.worm_group.add(self)

        self.name = name
        self.PLAYER_COLOR = color
        self.health = 100
        self.max_health = 100
        self.attack = 10

        self.vel_x = speed
        self.vel_y = 0
        self.dx = 0
        self.dy = 0

        self.img = pygame.image.load("assets/worm_p1.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flip = True
        self.direction = 1

        self.jump = False
        self.in_air = True

    def showName(self, screen):
        font = pygame.font.SysFont("consolas", 17)
        img = font.render(str(self.name), True, self.PLAYER_COLOR)
        screen.blit(img, (self.rect.centerx - (img.get_width() / 2), self.rect.top - 30))

    def showHealthBar(self,screen):
        font = pygame.font.SysFont("consolas", 17)
        img = font.render(str(self.health), True, self.PLAYER_COLOR)
        screen.blit(img, (self.rect.centerx - (img.get_width() / 2), self.rect.top - 10))

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right):
        self.dx = 0
        self.dy = 0

        if moving_left and self.rect.left > 0:
            self.dx = -self.vel_x
            self.flip = False
            self.direction = -1
        if moving_right and self.rect.right < constant_dispenser.SCREEN_WIDTH:
            self.dx = self.vel_x
            self.flip = True
            self.direction = 1
        if self.jump:
            self.vel_y = -3
            self.jump = False
            self.in_air = True

        self.vel_y += 0.05 #GRAVITY

        self.dy += self.vel_y

        if self.rect.bottom + self.dy > 600:
            self.dy = 600 - self.rect.bottom
            self.in_air = False

        self.wormCollisionWith(self.game.box_group)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def lookCursor(self):
        if (pygame.mouse.get_pos()[0] - self.rect.centerx) < 0:
            self.flip = False
            self.direction = -1
        else:
            self.flip = True
            self.direction = 1

    def wormCollisionWith(self, element_group):
        collision_tolerance = 20
        for element in element_group:
            if self.rect.colliderect(element.rect):
                if abs(element.rect.top+15 - self.rect.bottom) < collision_tolerance and self.vel_y > 0:
                    self.vel_y = 0
                if abs(element.rect.bottom - self.rect.top) < collision_tolerance and self.vel_y < 0:
                    self.vel_y = 0
                if abs(element.rect.right-10 - self.rect.left) < collision_tolerance and self.direction < 0:
                    self.rect.bottom = element.rect.top+5 # auto climb
                if abs(element.rect.left+10 - self.rect.right) < collision_tolerance and self.direction > 0:
                    self.rect.bottom = element.rect.top+5 # auto climb
                self.in_air = False

    def wormCollisionWithGround(self, mask, x=0, y=0):
        worm_mask = pygame.mask.from_surface(self.img)
        offset = (int(x - self.rect.x), int(y - self.rect.y))
        collision = mask.overlap(worm_mask, offset)
        #print(collision)
        return collision