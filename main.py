from turtledemo import clock

import pygame
from game import Game
from projectile import Grenade

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = SCREEN_WIDTH*(9/16) #ration 16/9

pygame.display.set_caption("Worms")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 144

background = pygame.image.load("assets/background.jpg")
RED = (255, 0, 0)

game = Game()
player = game.player

GRAVITY = 0.05
moving_right = False
moving_left = False
shoot_grenade = False

running = True

while running:
    dt = clock.tick(FPS)
    screen.blit(background, (0,0))
    pygame.draw.line(screen, RED, (0, 600), (SCREEN_WIDTH, 600))
    player.draw(screen)

    game.grenade_group.update()
    game.grenade_group.draw(screen)
    game.explosion_group.update()
    game.explosion_group.draw(screen)

    player.move(moving_left, moving_right, GRAVITY)

    font = pygame.font.SysFont(None, 24)
    img = font.render(str(player.health), True, RED)
    screen.blit(img, (player.pos.centerx-(img.get_width()/2), player.pos.top-10))

    pygame.draw.line(screen, RED, (player.pos.centerx, player.pos.centery), (pygame.mouse.get_pos()))
    if shoot_grenade:
        forcex = pygame.mouse.get_pos()[0] - player.pos.centerx
        forcey = pygame.mouse.get_pos()[1] - player.pos.centery
        force = ((forcex-forcex/2)/40, (forcey-forcey/2)/40)
        #print("Throw force :", force)
        grenade = Grenade(player.pos.centerx, player.pos.centery, force, game.explosion_group)
        game.grenade_group.add(grenade)
        shoot_grenade = False

    #print(player.velocity_y)
    #print(clock.get_fps())
    pygame.display.update() # Update l'affichage

    # Gestion des events
    for event in pygame.event.get():
        # Fermeture du jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shoot_grenade = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shoot_grenade = False
        # Appuis des touches stockés dans un dict
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_RIGHT and player.pos.x + player.pos.width < SCREEN_WIDTH:
                moving_right = True
            if event.key == pygame.K_LEFT and player.pos.x > 0:
                moving_left = True
            if event.key == pygame.K_UP and not player.in_air:
                player.jump = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
