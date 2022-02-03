import math
from turtledemo import clock

import pygame
from game import Game
from projectile import Grenade
from box import Box

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
tab_worms = [game.player1.worm1, game.player2.worm1]
grenade_group = game.grenade_group
explosion_group = game.explosion_group
box = game.box

# Actions
moving_right_1 = False
moving_left_1 = False
moving_right_2 = False
moving_left_2 = False
shoot_grenade = False

# Script action
running = True
actualWormPlayer = tab_worms[0]
turn = 0
endgame = False

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
    box.draw(screen)
    box.update()

    # Aide visée
    if(actualWormPlayer == tab_worms[0]):
        game.aiming(screen, RED, tab_worms[0])
    elif(actualWormPlayer == tab_worms[1]):
        game.aiming(screen, RED, tab_worms[1])

    if shoot_grenade:
        A = (actualWormPlayer.rect.centerx, actualWormPlayer.rect.centery)
        B = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] -30)
        #C = (pygame.mouse.get_pos()[0], actualWormPlayer.rect.centery)

        vect_AB = (B[0] - A[0], B[1] - A[1])

        '''
        #vect_AC = (C[0] - A[0], C[1] - A[1])
        #vect_CB = (B[0] - C[0], B[1] - C[1])

        #norme_AB = math.sqrt(vect_AB[0]**2 + vect_AB[1]**2)
        #norme_AC = math.sqrt(vect_AC[0]**2 + vect_AC[1]**2)

        #prod_scalaire = vect_AB[0]*vect_AC[0] + vect_AB[1]*vect_AC[1]

        #alpha = math.acos(prod_scalaire/(norme_AB*norme_AC))
        '''

        factor = 5
        direction_x = 1
        direction_y = 1
        if vect_AB[0] < 0:
            direction_x = -1
        if vect_AB[1] < 0:
            direction_y = -1

        if abs(vect_AB[0]/300) > 1:
            vect_AB = (direction_x * 300, vect_AB[1])
        if abs(vect_AB[1]/300) > 1:
            vect_AB = (vect_AB[0], direction_y * 300)
        v = (100 * direction_x * math.sin((abs(vect_AB[0]/300) * math.pi) / 2), 100 * direction_y * math.sin((abs(vect_AB[1]/300) * math.pi) / 2))

        #print("Throw force :", v)
        grenade = Grenade(actualWormPlayer.rect.centerx-actualWormPlayer.rect.width/2, actualWormPlayer.rect.centery-actualWormPlayer.rect.width/2, v, game)
        shoot_grenade = False
        turn += 1
        actualWormPlayer = tab_worms[turn % 2]
        moving_right_1 = False
        moving_left_1 = False
        moving_right_2 = False
        moving_left_2 = False

    if box.health <= 0:
        game.box.kill()
        #box.explosion(game)

    font = pygame.font.SysFont("consolas", 25)

    if(tab_worms[0].health <= 0 and tab_worms[1].health <= 0):
        end_message = font.render("égalité !", True, (255, 80, 255))
        screen.blit(end_message, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        endgame = True

    elif(tab_worms[0].health <= 0):
        end_message = font.render(str(tab_worms[1].name) + " a gagné !", True, tab_worms[1].PLAYER_COLOR)
        screen.blit(end_message, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        endgame = True
    elif (tab_worms[1].health <= 0):
        end_message = font.render(str(tab_worms[0].name) + " a gagné !", True, tab_worms[0].PLAYER_COLOR)
        screen.blit(end_message, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        endgame = True

    #print(clock.get_fps())
    pygame.display.update() # Update affichage

    # Gestion des events
    for event in pygame.event.get():

        # Fermeture du jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if not endgame :

            # Input souris
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot_grenade = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                shoot_grenade = False

            # Input claviers
            elif event.type == pygame.KEYDOWN:
                if turn%2 == 0:
                    if event.key == pygame.K_RIGHT and actualWormPlayer.rect.x + actualWormPlayer.rect.width < SCREEN_WIDTH:
                        moving_right_1 = True
                    if event.key == pygame.K_LEFT and actualWormPlayer.rect.x > 0:
                        moving_left_1 = True
                if turn%2 == 1:
                    if event.key == pygame.K_RIGHT and actualWormPlayer.rect.x + actualWormPlayer.rect.width < SCREEN_WIDTH:
                        moving_right_2 = True
                    if event.key == pygame.K_LEFT and actualWormPlayer.rect.x > 0:
                        moving_left_2 = True
                if event.key == pygame.K_UP and not actualWormPlayer.in_air:
                    actualWormPlayer.jump = True
            elif event.type == pygame.KEYUP:
                if turn%2 == 0:
                    if event.key == pygame.K_RIGHT:
                        moving_right_1 = False
                    if event.key == pygame.K_LEFT:
                        moving_left_1 = False
                elif turn%2 == 1:
                    if event.key == pygame.K_RIGHT:
                        moving_right_2 = False
                    if event.key == pygame.K_LEFT:
                        moving_left_2 = False