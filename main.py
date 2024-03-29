from turtledemo import clock

import pygame
from game import Game
from projectile import Grenade

pygame.init()
SCREEN_WIDTH = 1280 # (1280x720)
SCREEN_HEIGHT = SCREEN_WIDTH*(9/16) # ratio 16/9

pygame.display.set_caption("Worms")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 144

background = pygame.image.load("assets/background.jpg")
RED = (255, 0, 0)

# Init
game = Game()
GRAVITY = game.GRAVITY
player = game.player
grenade_group = game.grenade_group
explosion_group = game.explosion_group

# Actions
moving_right = False
moving_left = False
shoot_grenade = False

# Script action
running = True

while running:
    dt = clock.tick(FPS)

    # Affichage background
    screen.blit(background, (0,0))

    # Affichage sol et player
    pygame.draw.line(screen, RED, (0, 600), (SCREEN_WIDTH, 600))
    player.draw(screen)
    player.move(moving_left, moving_right, GRAVITY)

    # Affichage autres entités
    grenade_group.update()
    grenade_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)

    # Affichage vie du joueur
    font = pygame.font.SysFont(None, 24)
    img = font.render(str(player.health), True, RED)
    screen.blit(img, (player.rect.centerx-(img.get_width()/2), player.rect.top-10))

    # Aide visée
    pygame.draw.line(screen, RED, (player.rect.centerx, player.rect.centery), (pygame.mouse.get_pos()))

    if shoot_grenade:
        force_x = pygame.mouse.get_pos()[0] - player.rect.centerx
        force_y = pygame.mouse.get_pos()[1] - player.rect.centery
        force = ((force_x-force_x/2)/40, (force_y-force_y/2)/40)
        #print("Throw force :", force)
        grenade = Grenade(player.rect.centerx, player.rect.centery, force, game)
        shoot_grenade = False

    #print(player.vel_y)
    #print(clock.get_fps())
    pygame.display.update() # Update affichage

    # Gestion des events
    for event in pygame.event.get():

        # Fermeture du jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Input souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shoot_grenade = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shoot_grenade = False

        # Input claviers
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player.rect.x + player.rect.width < SCREEN_WIDTH:
                moving_right = True
            if event.key == pygame.K_LEFT and player.rect.x > 0:
                moving_left = True
            if event.key == pygame.K_UP and not player.in_air:
                player.jump = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
