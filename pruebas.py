import pygame
from sys import exit
import random
import math
import time
pygame.init() #starts game module

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (250,250,51)
GREEN = (180, 212, 181)

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (250,250,51)
GREEN = (180, 212, 181)


clock = pygame.time.Clock() #objeto que mide el tiempo dentro del programa
screen_x = 800
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y)) #resolucion de pantalla
pygame.display.set_caption("Eagle Defender") #nombre de pestana de juego

#fonts
fontprincipal = pygame.font.Font('assets/DePixelHalbfett.otf', 25) #import de font principal
fontsmaller = pygame.font.Font('assets/DePixelHalbfett.otf', 15)

#login
Login = fontprincipal.render('Eagle Defender', True, BLACK)
start = fontprincipal.render('Start-e', True, WHITE)
leaderboard = fontprincipal.render('Leaderboard-o', True, WHITE)

#title text
Eagle_Defender = fontprincipal.render('Eagle Defender-E', True, BLACK)
start = fontprincipal.render('Start-S', True, WHITE)
leaderboard = fontprincipal.render('Leaderboard-L', True, WHITE)
options = fontprincipal.render('Options-o', True, WHITE)
credits = fontprincipal.render('Credits-c', True, WHITE)
quit = fontprincipal.render('Quit-q', True, WHITE)

#start game
start_game_title = fontprincipal.render('Start game', True, BLACK)

#game UI elements
points = fontprincipal.render('Points + variable_puntos', True, BLACK) #variable de puntos

#Leaderboard
leaderboard_title = fontprincipal.render('Leaderboard', True, BLACK)

#options
options_title = fontprincipal.render('Options', True, BLACK)

#credits
credits_title = fontprincipal.render('Credits', True, BLACK)

#escape
esc_text = fontsmaller.render('Press "esc" to go to title', True, WHITE)



#define los "game states"
state = "title" #deja el state como la primera pantalla, esta siendo los idiomas
#gameloop
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #crea el evento de cerrar el programa al activar el flag de quit
            exit()
        elif state == "login":
            break
        elif state == "title":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    state = "start"
                if event.key == pygame.K_l:
                    state = "leaderboard"
                if event.key == pygame.K_o:
                    state = "options"
                if event.key == pygame.K_c:
                    state = "credits"
                
        elif state == "start":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"
                if event.key == pygame.K_s:
                    state == "game"

        elif state == "game":
            break
        
        elif state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"

        elif state == "options":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"

        elif state == "credits":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"



    pygame.display.flip()
    

    if state == "login":
        break

    if state == "title": #dibuja el texto en title
        screen.fill(GREEN)
        screen.blit(Eagle_Defender, (Eagle_Defender.get_rect(center=(screen_x/2, 80))))
        screen.blit(start, (start.get_rect(center=(screen_x/2, 150))))
        screen.blit(leaderboard, (leaderboard.get_rect(center=(screen_x/2, 230))))
        screen.blit(options, (options.get_rect(center=(screen_x/2, 310))))
        screen.blit(credits, (credits.get_rect(center=(screen_x/2, 390))))
        screen.blit(quit, (quit.get_rect(center=(screen_x/2, 470))))
    
    elif state == "title":
            screen.fill(GREEN)
            screen.blit(Eagle_Defender, (Eagle_Defender.get_rect(center=(screen_x/2, 90))))
    
    if state == "start":
            screen.fill(GREEN)

            screen.blit(esc_text, (30, 470))
            screen.blit(start_game_title, (start_game_title.get_rect(center=(screen_x/2, 90))))

    if state == "game":
            screen.fill(GREEN)
            screen.blit(esc_text, (30, 470))
            screen.blit(points, (points.get_rect(points=(screen_x/2, 90))))

    if state == "options":
            screen.fill(GREEN)
            screen.blit(esc_text, (30, 470))
            screen.blit(options_title, (options_title.get_rect(center=(screen_x/2, 90))))

    if state == "leaderboard":
            screen.fill(GREEN)
            screen.blit(esc_text, (30, 470))
            screen.blit(leaderboard_title, (leaderboard_title.get_rect(center=(screen_x/2, 90))))

    if state == "credits":
            screen.fill(GREEN)
            screen.blit(esc_text, (30, 470))
            screen.blit(credits_title, (credits_title.get_rect(center=(screen_x/2, 90))))