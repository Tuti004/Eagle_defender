import pygame
import sqlite3
from pygame.locals import *
import sys
import os
import random

# Tipos de bloques disponibles
BLOCK_TYPES = ["concreto", "madera", "acero"]

class Inventory_Defender:
    def __init__(self):
        self.blocks = {
            "concreto": 10,
            "madera": 10,
            "acero": 10
        }

    def use_block(self, block_type):
        if self.blocks[block_type] > 0:
            self.blocks[block_type] -= 1
            return True
        else:
            return False 
    def return_block(self, block_type):
        self.blocks[block_type] += 1

# Clase para las balas de tipo Bomba
class BombBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'assets', 'bomba.png')
        self.sprite_path = pygame.image.load(image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect.midbottom = (x, y)
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 320:
            self.kill()

class FireBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'assets', 'bala_fuego.png')
        self.sprite_path = pygame.image.load(image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect.midbottom = (x, y)
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 320:
            self.kill()

class WaterBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'assets', 'bala_agua.png')
        self.sprite_path = pygame.image.load(image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect.midbottom = (x, y)
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 320:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'assets', 'tank.png')
        self.sprite_path = pygame.image.load(image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.x = 200
        self.y = 200
        self.x_change = 0
        self.y_change = 0
        self.hearts = 6
        self.speed = 1
        self.rect.midbottom = (self.x, self.y)
        self.screen = screen  # Almacena la referencia a la pantalla

        self.bullet_inventory = {
            BombBullet: 5,
            FireBullet: 5,
            WaterBullet: 5
        }

        self.selected_bullet_type = WaterBullet
        self.message_timer = 0
    
    def select_bomb_bullet(self):
        self.selected_bullet_type = BombBullet

    def select_fire_bullet(self):
        self.selected_bullet_type = FireBullet

    def select_water_bullet(self):
        self.selected_bullet_type = WaterBullet

    def player_input(self):
        keys = pygame.key.get_pressed()

    def player_input(self): #esta funcion permite el moviento con wasd del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y_change = -self.speed
        if keys[pygame.K_w] == False:
            self.y_change = 0

        if keys[pygame.K_a]:
            self.x_change = -self.speed
        if keys[pygame.K_a] == False:
            self.x_change = 0

        if keys[pygame.K_s]:
            self.y_change = +self.speed
        
        if keys[pygame.K_d]:
            self.x_change = +self.speed
        if keys[pygame.K_SPACE]:
            bullet_cd(self)

        if keys[pygame.K_4]:
            self.select_bomb_bullet()  # Seleccionar bombas
        if keys[pygame.K_5]:
            self.select_fire_bullet()  # Seleccionar fuego
        if keys[pygame.K_6]:
            self.select_water_bullet()  # Seleccionar agua  
        
    def apply_border(self): #esta funcion causa que el jugador no se pueda salir de los bordes
        if self.x <= 30:
            self.x = 30
        if self.x >= 775:
            self.x = 775
        if self.y <= 50:
            self.y = 50
        if self.y >= 617:
            self.y = 617

    def update(self):  #update cada frame a cada uno de los atributos del jugador
        self.player_input()
        self.apply_border()
        self.x += self.x_change
        self.y += self.y_change
        self.rect.midbottom = (self.x, self.y)
        #if pygame.sprite.spritecollide(self, aliens, False):
#            self.hearts = self.hearts-1
        if self.message_timer > 0:
            font = pygame.font.Font(None, 36)
            text = font.render("No tienes balas disponibles", True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(text, text_rect)
            self.message_timer -= 1
            
screen = pygame.display.set_mode((800, 600))
player = pygame.sprite.Group() #spritegroup player
player.add(Player(screen)) #agrega a player al sprite group

bullets = pygame.sprite.Group()
last_shot_time = 0

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'assets', 'bala_jugador.png')
        self.sprite_path = pygame.image.load(image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 320:
            self.kill()

def bullet_cd(player):
    global last_shot_time
    current_time = pygame.time.get_ticks()
    new_bullet = None  # Inicializa la variable fuera de las declaraciones condicionales

    if current_time - last_shot_time < 600:  # cooldown
        return
    
    if player.selected_bullet_type == BombBullet:
        if player.bullet_inventory[BombBullet] > 0:
            new_bullet = BombBullet(player.rect.centerx - 32, player.rect.centery + 15)
            player.bullet_inventory[BombBullet] -= 1
        else:
            player.message_timer = 60  # Mostrar mensaje durante 1 segundo
    elif player.selected_bullet_type == FireBullet:
        if player.bullet_inventory[FireBullet] > 0:
            new_bullet = FireBullet(player.rect.centerx - 32, player.rect.centery + 15)
            player.bullet_inventory[FireBullet] -= 1
        else:
            player.message_timer = 60  # Mostrar mensaje durante 1 segundo
    elif player.selected_bullet_type == WaterBullet:
        if player.bullet_inventory[WaterBullet] > 0:
            new_bullet = WaterBullet(player.rect.centerx - 32, player.rect.centery + 15)
            player.bullet_inventory[WaterBullet] -= 1
        else:
            player.message_timer = 60  # Mostrar mensaje durante 1 segundo
     
    if new_bullet is not None:
        bullets.add(new_bullet)
        last_shot_time = current_time
        
class BlockScreen:
    def __init__(self, player1_username, player2_username, player1_role):
        pygame.init()
        window_width = 800
        window_height = 600
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Eagle Defender")
    
        self.player1_username = player1_username
        self.player2_username = player2_username
        self.player1_role = player1_role

        self.defender_turn_over = False

        # Dimensiones del marco interno
        self.ANCHO_MARCO = window_width - 100
        self.ALTO_MARCO = window_height - 150
        self.POS_X_MARCO = (window_width - self.ANCHO_MARCO) // 2
        self.POS_Y_MARCO = (window_height - self.ALTO_MARCO) // 2


        self.NUM_CELDAS = 17
        self.CELDA = self.ANCHO_MARCO // self.NUM_CELDAS


        # Colores
        self.BLANCO = (255, 255, 255)
        self.GRIS = (200, 200, 200)

        # Carga de imágenes
        self.imagen_concreto = pygame.image.load("blocks/concreto.png")
        self.imagen_madera = pygame.image.load("blocks/madera.jpeg")
        self.imagen_acero = pygame.image.load("blocks/acero.png")

        # Ajustar el tamaño de las imágenes
        self.imagen_concreto = pygame.transform.scale(self.imagen_concreto, (self.CELDA, self.CELDA))
        self.imagen_madera = pygame.transform.scale(self.imagen_madera, (self.CELDA, self.CELDA))
        self.imagen_acero = pygame.transform.scale(self.imagen_acero, (self.CELDA, self.CELDA))

        self.matriz_celdas = [[False for _ in range(self.NUM_CELDAS)] for _ in range(self.NUM_CELDAS)]
        self.selected_block = "madera"

        # Crea una instancia del inventario del defensor
        self.inventory_defender = Inventory_Defender()

        # Carga la imagen del águila
        self.eagle_image = pygame.image.load("aguila3.png")  

        # Por si quiere que el àguila sea del mismo tamaño que las celdas
        #self.eagle_image = pygame.transform.scale(self.eagle_image, (self.CELDA, self.CELDA))
        self.eagle_rect = self.eagle_image.get_rect()

        # timer
        self.timer_duration = 90 * 1000  # 90 segundos
        self.timer_start = pygame.time.get_ticks()
        self.turn_timer_expired = False
        self.confirmation_received = False

        # Musica de fondo
        pygame.mixer.init()
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)

        self.defender_songs = "Songs/Defensor"
        self.init_music(self.defender_songs)

        confirmation_width = 150
        confirmation_x = (window_width - confirmation_width) // 2

        self.confirmation_button_color = (200, 200, 200)  # Color gris
        self.confirmation_button_rect = pygame.Rect(confirmation_x, 540, confirmation_width, 40) 
        self.confirmation_button_font = pygame.font.Font(None, 25)
        self.confirmation_button_text = "Confirmar Turno"

    def draw_player_info(self):
        font = pygame.font.Font(None, 24)
        # Definir las coordenadas y el color del texto
        text_color = (0, 0, 0)

        if self.player1_role == "defender":
            # Si el jugador 1 es el defensor, mostrar sus datos en la esquina inferior izquierda
            username_text = font.render(f"Defensor: {self.player1_username}", True, text_color)
            username_rect = username_text.get_rect(topleft=(20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        else:
            # Si el jugador 1 es el atacante, mostrar sus datos en la esquina inferior derecha
            username_text = font.render(f"Atacante: {self.player1_username}", True, text_color)
            username_rect = username_text.get_rect(topright=(self.screen.get_width() - 20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        # Muestra la información del jugador 2 (el que no seleccionó el jugador 1)
        if self.player1_role == "defender":
            username_text = font.render(f"Atacante: {self.player2_username}", True, text_color)
            username_rect = username_text.get_rect(topright=(self.screen.get_width() - 20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        else:
            username_text = font.render(f"Defensor: {self.player2_username}", True, text_color)
            username_rect = username_text.get_rect(topleft=(20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)

    def dibujar_cuadricula(self):
        for x in range(self.POS_X_MARCO, self.ANCHO_MARCO + self.POS_X_MARCO, self.CELDA):
            pygame.draw.line(self.screen, self.GRIS, (x, self.POS_Y_MARCO), (x, self.ALTO_MARCO + self.POS_Y_MARCO))
        for y in range(self.POS_Y_MARCO, self.ALTO_MARCO + self.POS_Y_MARCO, self.CELDA):
            pygame.draw.line(self.screen, self.GRIS, (self.POS_X_MARCO, y), (self.ANCHO_MARCO + self.POS_X_MARCO, y))
    
    def dibujar_imagenes(self):
        for x in range(self.NUM_CELDAS):
            for y in range(self.NUM_CELDAS):
                if self.matriz_celdas[x][y]:
                    if self.matriz_celdas[x][y] == "concreto":
                        self.screen.blit(self.imagen_concreto, (x * self.CELDA + self.POS_X_MARCO, y * self.CELDA + self.POS_Y_MARCO))
                    elif self.matriz_celdas[x][y] == "madera":
                        self.screen.blit(self.imagen_madera, (x * self.CELDA + self.POS_X_MARCO, y * self.CELDA + self.POS_Y_MARCO))
                    elif self.matriz_celdas[x][y] == "acero":
                        self.screen.blit(self.imagen_acero, (x * self.CELDA + self.POS_X_MARCO, y * self.CELDA + self.POS_Y_MARCO))
    def es_dentro_del_marco(self, x, y):
        if (self.POS_X_MARCO <= x < self.POS_X_MARCO + self.ANCHO_MARCO and
            self.POS_Y_MARCO <= y < self.POS_Y_MARCO + self.ALTO_MARCO):
            return True
        return False
    
    def cuadro_ocupado(self, fila, columna):
        if (0 <= fila < self.NUM_CELDAS) and (0 <= columna < self.NUM_CELDAS):
            return self.matriz_celdas[fila][columna]
        return False

    def draw_confirmation_button(self):
        pygame.draw.rect(self.screen, self.confirmation_button_color, self.confirmation_button_rect)
        text_surf = self.confirmation_button_font.render(self.confirmation_button_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.confirmation_button_rect.center)
        self.screen.blit(text_surf, text_rect)


    def main_loop(self):
        running = True
        selected_block = None
        message_timer = 0
        eagle_row = 5  # Coordenada X inicial del águila
        eagle_col = 2  # Coordenada Y inicial del águila

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                     # Bloquea la colocación de bloques si el turno del defensor ha terminado
                    if self.defender_turn_over:
                        continue

                    x, y = event.pos
                    fila = (x - self.POS_X_MARCO) // self.CELDA
                    columna = (y - self.POS_Y_MARCO) // self.CELDA
                    
                    # Obtenga las coordenadas absolutas del bloque
                    bloque_x = fila * self.CELDA + self.POS_X_MARCO
                    bloque_y = columna * self.CELDA + self.POS_Y_MARCO

                    # Verifique si el bloque estará dentro del marco
                    if not self.es_dentro_del_marco(bloque_x, bloque_y):
                        continue

                    # Comprueba si las coordenadas están dentro del rango
                    if 0 <= fila < self.NUM_CELDAS and 0 <= columna < self.NUM_CELDAS:
                        if self.matriz_celdas[fila][columna]:  # Si hay un bloque, lo quitamos
                            self.inventory_defender.return_block(self.matriz_celdas[fila][columna])
                            self.matriz_celdas[fila][columna] = None
                        else:  # Intentamos agregar un nuevo bloque
                            if selected_block and self.inventory_defender.use_block(selected_block):
                                self.matriz_celdas[fila][columna] = selected_block
                            else:
                                message_timer = 100

                if event.type == pygame.KEYDOWN:
                    if self.defender_turn_over:
                    # Bloquea el movimiento y la selección de bloques si el turno del defensor ha terminado
                        continue

                    if event.key == pygame.K_1:
                        selected_block = "concreto"
                    elif event.key == pygame.K_2:
                        selected_block = "madera"
                    elif event.key == pygame.K_3:
                        selected_block = "acero"
                    elif event.type == pygame.KEYDOWN:
                        new_row = eagle_row
                        new_col = eagle_col
                        if event.key == pygame.K_UP:
                            new_row -= 1
                        elif event.key == pygame.K_DOWN:
                            new_row += 1
                        elif event.key == pygame.K_LEFT:
                            new_col -= 1
                        elif event.key == pygame.K_RIGHT:
                            new_col += 1
                        # Comprueba si el nuevo cuadro está vacío antes de mover el águila
                    if (0 <= new_row < self.NUM_CELDAS and 
                        0 <= new_col < self.NUM_CELDAS and 
                        not self.cuadro_ocupado(new_row, new_col) and 
                        self.es_dentro_del_marco(self.POS_X_MARCO + new_col * self.CELDA, 
                                                self.POS_Y_MARCO + new_row * self.CELDA)):
                        eagle_row = new_row
                        eagle_col = new_col
                    if event.key == pygame.K_RETURN:
                        self.show_confirmation_screen()
                        self.turn_timer_expired = True
                elif self.turn_timer_expired == True:
                    pass    

            self.screen.fill((255, 255, 255))  # Llena la pantalla de blanco
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.timer_start
            remaining_time = max(0, self.timer_duration - elapsed_time)
            minutes, seconds = divmod(remaining_time // 1000, 60)

            self.dibujar_cuadricula()
            self.dibujar_imagenes()
            self.draw_player_info()

            # Render and display the timer on the screen
            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
            timer_rect = timer_text.get_rect(center=(self.screen.get_width() // 2, 30))
            self.screen.blit(timer_text, timer_rect)

            if remaining_time == 0 and not self.turn_timer_expired:
                self.show_confirmation_screen()
                self.turn_timer_expired = True

            # Dibuja el águila en la posición deseada basada en las coordenadas de la cuadrícula
            eagle_x = self.POS_X_MARCO + eagle_col * self.CELDA
            eagle_y = self.POS_Y_MARCO + eagle_row * self.CELDA
            self.screen.blit(self.eagle_image, (eagle_x, eagle_y)) 

            # Dibuja el inventario del defensor
            inventory_x = 20
            inventory_y = 20
            inventory_spacing = 60
            for block_type in BLOCK_TYPES:
                count = self.inventory_defender.blocks[block_type]
                self.draw_inventory_block(inventory_x, inventory_y, block_type, count)
                inventory_x += inventory_spacing

            if message_timer > 0:
                font = pygame.font.Font(None, 36)
                text = font.render("No tienes bloques disponibles", True, (255, 0, 0))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                self.screen.blit(text, text_rect)
                message_timer -= 1

            if self.confirmation_received == True:
                player.update() 
                player.draw(self.screen)   
                bullets.update()
                bullets.draw(self.screen) 

            pygame.display.flip()

        pygame.quit()
        sys.exit()


    def show_confirmation_screen(self):
        self.defender_turn_over = True
        confirmation_font = pygame.font.Font(None, 40)
        confirmation_text = confirmation_font.render("Turno completado. ¿Listo para el siguiente jugador?", True, (0, 0, 0))
        confirmation_rect = confirmation_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(confirmation_text, confirmation_rect)
        pygame.mixer.music.stop()

        pygame.display.flip()

        while not self.confirmation_received:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.confirmation_received = True

                    self.attacker_songs = "Songs/Atacante"
                    self.init_music(self.attacker_songs)

                    self.timer_start = pygame.time.get_ticks()
                    self.turn_timer_expired = False

    def draw_inventory_block(self, x, y, block_type, count):
        block_color = (255, 255, 255)
        block_name = ""
        if block_type == "concreto":
            block_color = (200, 200, 200)
            block_name = "Concreto"
        elif block_type == "madera":
            block_color = (139, 69, 19)
            block_name = "Madera"
        elif block_type == "acero":
            block_color = (169, 169, 169)
            block_name = "Acero"

        pygame.draw.rect(self.screen, block_color, (x, y, 50, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 50, 50), 2)

        font = pygame.font.Font(None, 20)
        text = font.render(block_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + 25, y + 75))
        self.screen.blit(text, text_rect)

        count_text = font.render(str(count), True, (0, 0, 0))
        count_rect = count_text.get_rect(center=(x + 25, y + 25))
        self.screen.blit(count_text, count_rect)

    def init_music(self, directory):
        """Initialize the music player with songs from the provided directory."""
        self.song_list = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp3"):
                    self.song_list.append(os.path.join(root, file))

        if not self.song_list:
            print("No songs found in the directory.")
            return
        
        random.shuffle(self.song_list)
        self.current_song_index = 0
        self.play_next_song()

    def play_next_song(self):
        """Reproduce the next song."""
        pygame.mixer.music.load(self.song_list[self.current_song_index])
        pygame.mixer.music.play()