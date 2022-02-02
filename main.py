import math
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
worm1_1 = game.player1.worm1
worm1_2 = game.player2.worm1
grenade_group = game.grenade_group
explosion_group = game.explosion_group

# Actions
moving_right_1 = False
moving_left_1 = False
moving_right_2 = False
moving_left_2 = False
shoot_grenade = False

# Script action
running = True
actualWormPlayer = worm1_1
turn = 1

while running:
    dt = clock.tick(FPS)

    # Affichage background
    screen.blit(background, (0,0))

    # Affichage sol et worm
    pygame.draw.line(screen, RED, (0, 593), (SCREEN_WIDTH, 593))
    game.player1.showWorm(screen, moving_left_1, moving_right_1, GRAVITY)
    game.player2.showWorm(screen, moving_left_2, moving_right_2, GRAVITY)

    # Affichage autres entités
    grenade_group.update()
    grenade_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)

    # Affichage vie du joueur
    game.showHealthBar(screen, worm1_1, RED)
    game.showHealthBar(screen, worm1_2, RED)

    # Aide visée
    if(actualWormPlayer == worm1_1):
        game.aiming(screen, RED, worm1_1)
    elif(actualWormPlayer == worm1_2):
        game.aiming(screen, RED, worm1_2)

    if shoot_grenade:
        A = (actualWormPlayer.rect.centerx, actualWormPlayer.rect.centery)
        B = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        #C = (pygame.mouse.get_pos()[0], actualWormPlayer.rect.centery)

        vect_AB = (B[0] - A[0], B[1] - A[1])
        #vect_AC = (C[0] - A[0], C[1] - A[1])
        #vect_CB = (B[0] - C[0], B[1] - C[1])

        #norme_AB = math.sqrt(vect_AB[0]**2 + vect_AB[1]**2)
        #norme_AC = math.sqrt(vect_AC[0]**2 + vect_AC[1]**2)

        #prod_scalaire = vect_AB[0]*vect_AC[0] + vect_AB[1]*vect_AC[1]

        #alpha = math.acos(prod_scalaire/(norme_AB*norme_AC))

        factor = 5
        signe_x = 1
        signe_y = 1
        if vect_AB[0] < 0:
            signe_x = -1
        if vect_AB[1] < 0:
            signe_y = -1
        v = (factor * signe_x * math.sqrt(abs(vect_AB[0])), factor * signe_y * math.sqrt(abs(vect_AB[1])))

        print("Throw force :", v)
        grenade = Grenade(actualWormPlayer.rect.centerx, actualWormPlayer.rect.centery, v, game)
        shoot_grenade = False

    #print(worm.vel_y)
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
            if turn == 1:
                if event.key == pygame.K_RIGHT and actualWormPlayer.rect.x + actualWormPlayer.rect.width < SCREEN_WIDTH:
                    moving_right_1 = True
                if event.key == pygame.K_LEFT and actualWormPlayer.rect.x > 0:
                    moving_left_1 = True
            if turn == 2:
                if event.key == pygame.K_RIGHT and actualWormPlayer.rect.x + actualWormPlayer.rect.width < SCREEN_WIDTH:
                    moving_right_2 = True
                if event.key == pygame.K_LEFT and actualWormPlayer.rect.x > 0:
                    moving_left_2 = True
            if event.key == pygame.K_UP and not actualWormPlayer.in_air:
                actualWormPlayer.jump = True
        elif event.type == pygame.KEYUP:
            if turn == 1:
                if event.key == pygame.K_RIGHT:
                    moving_right_1 = False
                if event.key == pygame.K_LEFT:
                    moving_left_1 = False
            elif turn == 2:
                if event.key == pygame.K_RIGHT:
                    moving_right_2 = False
                if event.key == pygame.K_LEFT:
                    moving_left_2 = False