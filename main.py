import pygame
from sys import exit
import random
import math
import time
pygame.init() #empieza el modulo de display (pygame no puede hacer nada hasta que esta iniciado). basicamente me lo hace de automatico
#archivo de puntajes
archiveroute = 'puntajes'
f = open('puntajes', 'w')
f.write("placeholder\n")
f.write("placeholder")
f.close()
#score
score_list = []
score = 0
score_list.sort(reverse=True)


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
#background
#fonts
fontprincipal = pygame.font.Font('assets/DePixelHalbfett.otf', 25) #import de font principal
fontsmaller = pygame.font.Font('assets/DePixelHalbfett.otf', 15)

#todos los textos del espanol e ingles
#title name
Eagle_Defender = fontprincipal.render('Eagle Defender', True, BLACK)
#UI elements
hearts = pygame.image.load("assets/corazon.png")

#title text
start = fontprincipal.render('start-e', True, WHITE)
points = fontprincipal.render('top-points-o', True, WHITE)
quit = fontprincipal.render('quit-q', True, WHITE)
#difficulty
difficulty = fontprincipal.render('Choose your difficulty', True, WHITE)
easy = fontprincipal.render('easy-e', True, WHITE)
#game over
go = fontprincipal.render('GAME OVER', True, RED)
save_score = fontprincipal.render('to save score press f', True, WHITE)

#score
asdpoints = fontprincipal.render('Top points', True, WHITE)
asdpoints = fontprincipal.render('Puntajes mas altos', True, WHITE)

#escape text
esc_text = fontsmaller.render('Press "esc" to go to title', True, WHITE)




#player class
health_cd = 300
jugador_speed = 5
class Player(pygame.sprite.Sprite):
    def __init__(self): #empieza clase Player
        super().__init__() #parent class
        self.sprite_path = pygame.image.load('assets/cohete_jugador.png')
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.x = 40
        self.y = screen_y/2
        self.x_change = 0
        self.y_change = 0
        self.hearts = 6

    def player_imput(self): #esta funcion permite el moviento con wasd del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y_change = -jugador_speed
        if keys[pygame.K_w] == False:
            self.y_change = 0

        if keys[pygame.K_a]:
            self.x_change = -jugador_speed
        if keys[pygame.K_a] == False:
            self.x_change = 0

        if keys[pygame.K_s]:
            self.y_change = +jugador_speed
        
        if keys[pygame.K_d]:
            self.x_change = +jugador_speed
        if keys[pygame.K_SPACE]:
            bullet_cd(self)    
        
    def apply_border(self): #esta funcion causa que el jugador no se pueda salir de los bordes
        if self.x <= 30:
            self.x = 30
        if self.x >= 800:
            self.x = 800
        if self.y <= 100:
            self.y = 100
        if self.y >= 500:
            self.y = 500

    def update(self):  #update cada frame a cada uno de los atributos del jugador
        self.player_imput()
        self.apply_border()
        self.x += self.x_change
        self.y += self.y_change
        self.rect.midbottom = (self.x, self.y)
        #if pygame.sprite.spritecollide(self, aliens, False):
#            self.hearts = self.hearts-1

player = pygame.sprite.Group() #spritegroup player
player.add(Player()) #agrega a player al sprite group


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y): #el x y y aqui permite que cuando se agrege a bullets a su grupo de balas se ponga en las x y y del player
        super().__init__()
        self.sprite_path = pygame.image.load('assets/bala_jugador.png')        
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 12

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > 800:
            self.kill()
bullets = pygame.sprite.Group()
last_shot_time = 0

def bullet_cd(player): #cooldown de balas de jugador
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time < 600: #cooldown
        return
    new_bullet = PlayerBullet(player.rect.centerx, player.rect.centery+15) #cada vez que termina el cooldown agrega la clase bala a su grupo. o sea dispara
    bullets.add(new_bullet)
    last_shot_time = current_time #le hace update al ultimo shot reseteando el cooldown


#define los "game states"
state = "title" #deja el state como la primera pantalla, esta siendo los idiomas
#gameloop
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #crea el evento de cerrar el programa al activar el flag de quit
            exit() #detiene el "while true loop" para que no de error cuando cierre el programa
        #eventos de botton
        elif state == "title": #en el game state de titulo define que pasa al presionar ciertas teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    state = "difficulty"
                if event.key == pygame.K_o:
                    state = "points"
                if event.key == pygame.K_q:
                    state = "quit"
        elif state == "difficulty":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    state = "easy" 
        #eventos al perder juego
        elif state == "easy": 
            if Player.hearts <= 0:
                state = "game_over"

        elif state == "game_over": #manera de salir de escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"
                    Player.x = 40
                    Player.y = screen_y/2      
    
        elif state == "points": #define que pasa al tocar una tecla en la pantalla de puntajes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title"
            

        elif state == "options": #esc de opciones
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "title" 



    pygame.display.flip() #updatea la pantalla cada vez que pasa un argumento
    clock.tick(60) #fps
    current_time = pygame.time.get_ticks() #current time
    #assets
    screen.fill(GREEN)
#los blits son de texto o imagenes
    if state == "title": #dibuja el texto en title
        screen.blit(Eagle_Defender, (400, screen_y/2-25))
        screen.blit(start, (40, 90))
        screen.blit(points, (40, 180))
        screen.blit(quit, (40, 360))
        Player.hearts=6 #resetea los hearts
        score=0
 
    elif state == "difficulty": #difficulty state
        screen.blit(difficulty, (40, 90))   
        screen.blit(easy, (40, 180))  

    elif state == "easy": #easy state
        #update a la clase de jugador y a la clase de balas
        player.update() 
        player.draw(screen)   
        bullets.update()
        bullets.draw(screen)    

#        if current_time - alien_spawn_timer > 2000: #spawnea el enemigo si el current time menos el punto en el que el ultimo spawneo es mayor a los ticks
#            new_alien= Alien1() #convierte a la variable new_alien en la clase de Alien1
#            aliens.add(new_alien) #anade al grupo aliens el alien nuevo
#            alien_spawn_timer = current_time #resetea cooldown
#        alien_bullets.update()
#        alien_bullets.draw(screen)
#        aliens.update()
#        aliens.draw(screen)

#        for new_bullet in bullets: #usa a la clase dentro del grupo
#            alien_hit = pygame.sprite.spritecollide(new_bullet, aliens, True) #define el estado de colision
#            if alien_hit:
#                score += 1


#        for Player in player:#usa a la clase dentro del grupo
#            player_hit = pygame.sprite.spritecollide(Player, aliens, True)#define el estado de colision
#           if player_hit:
#                Player.hearts += -1

#        for Player in player:#usa a la clase dentro del grupo
#            player_hit = pygame.sprite.spritecollide(Player, alien_bullets, True)#define el estado de colision
#            if player_hit:
#                Player.hearts += -2

        
        #dibuja corazones dependiendo de la vida
        if Player.hearts==6:
            screen.blit(hearts, (10, 10))
            screen.blit(hearts, (50, 10))
            screen.blit(hearts, (90, 10))
        if Player.hearts>=4 and Player.hearts <6:
            screen.blit(hearts, (10, 10))
            screen.blit(hearts, (50, 10))
        if Player.hearts>=2 and Player.hearts <4:
            screen.blit(hearts, (10, 10))
        if Player.hearts<=1:
            score_list.append(score)
            Player.hearts=0
        score_surface = fontprincipal.render("Score: " + str(score), True, WHITE) #define score con su propia variable
        screen.blit(score_surface, (200, 10)) #dibuja score

    elif state == "game_over": #dibuja texto en game over
        screen.blit(esc_text, (30, 470))
        screen.blit(go, (screen_x/2-100, screen_y/2))
        screen.blit(save_score, (200, 200))
        score_surface = fontprincipal.render("Score: " + str(score), True, WHITE)
        screen.blit(score_surface, (screen_x/2-100, screen_y/2+50))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                score_list.append(score)

    elif state == "points":
        screen.blit(asdpoints, (30, 90))
        screen.blit(esc_text, (30, 470))











    elif state == "quit": #cierra el programa
        game = False
