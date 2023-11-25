import pygame
import sqlite3
from pygame.locals import *
import sys
import os
import random

#global variables
last_shot_time = 0

bailabilidad_label = 0
acustica_label = 0
tempo_label = 0
popularidad_label = 0

extra_agua = 0

is_paused = False
pause_start_time = 0

# Tipos de bloques disponibles
BLOCK_TYPES = ["concreto", "madera", "acero"]
BULLETS_TYPES = ["bomba", "fuego", "agua"]

class Inventory_Defender:
    def __init__(self):
        self.blocks = {
            "concreto": 10,
            "madera": 10,
            "acero": 10
        }

        self.block_images = {
            # Carga de imágenes
            "concreto": pygame.image.load("blocks/concreto.png"),
            "madera": pygame.image.load("blocks/madera.jpeg"),
            "acero": pygame.image.load("blocks/acero.png")
        }

        for block_type, image in self.block_images.items():
            self.block_images[block_type] = pygame.transform.scale(image, (50, 50))

    def use_block(self, block_type):
        if self.blocks[block_type] > 0:
            self.blocks[block_type] -= 1
            return True
        else:
            return False
    def return_block(self, block_type):
        self.blocks[block_type] += 1

class AttackerInventory:
    def __init__(self):
        self.bullet_types = {
            "bomba": 5,
            "fuego": 5,
            "agua": 5
        }

        self.bullet_images = {
            "bomba": pygame.image.load("assets/bomba.png"),
            "fuego": pygame.image.load("assets/bala_fuego.png"),
            "agua": pygame.image.load("assets/bala_agua.png")
        }

        self.last_bullet_return_time = 0

    def use_bullet(self, bullet_type):
        if self.bullet_types[bullet_type] > 0:
            self.bullet_types[bullet_type] -= 1
            return True
        else:
            return False

    def return_bullet(self, bullet_type):
        self.bullet_types[bullet_type] += 1

    def adjust_water_bullets(self, amount):
        self.bullet_types["agua"] += amount

#bullet death time
bullet_death_time = 1150

# Open/Closed Principle
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        current_directory = os.path.dirname(__file__)
        full_image_path = os.path.join(current_directory, 'assets', image_path)
        self.sprite_path = pygame.image.load(full_image_path)
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect.midbottom = (x, y)
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > bullet_death_time:
            self.kill()

class BombBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, 'bomba.png')

class FireBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, 'bala_fuego.png')

class WaterBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, 'bala_agua.png')

class Player(pygame.sprite.Sprite):
    def __init__(self, tank_skin):
        super().__init__()
        self.image = pygame.image.load(tank_skin)
        self.rect = self.image.get_rect()
        self.x = 500
        self.y = 280
        self.x_change = 0
        self.y_change = 0
        self.hearts = 6
        self.speed = 1
        self.rect.midbottom = (self.x, self.y)
        self.attacker_inventory = AttackerInventory()

        self.selected_bullet_type = "agua"
        self.message_timer = 0

        self.message_timer_balas = 0

    def update_tank_image(self, new_tank_img):
        self.image = pygame.image.load(new_tank_img)
    def select_bomb_bullet(self):
        self.selected_bullet_type = "bomba"

    def select_fire_bullet(self):
        self.selected_bullet_type = "fuego"

    def select_water_bullet(self):
        self.selected_bullet_type = "agua"

    def player_input(self): #esta funcion permite el moviento con wasd del jugador
        global is_paused

        if is_paused:
            return
        else:
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
        if self.x <= 80:
            self.x = 80
        if self.x >= 725:
            self.x = 725
        if self.y <= 120:
            self.y = 120
        if self.y >= 545:
            self.y = 545

    def update(self):
        self.player_input()
        self.apply_border()
        bullet_regen(self)
        self.x += self.x_change
        self.y += self.y_change
        self.rect.topleft = (self.x, self.y)

        if self.message_timer_balas > 0:
            self.message_timer_balas -= 1

bullets = pygame.sprite.Group()

def bullet_regen(player):
    current_time = pygame.time.get_ticks()

    if current_time - player.attacker_inventory.last_bullet_return_time >= 1000 * 30:
        for bullet_type in BULLETS_TYPES:
            if player.attacker_inventory.bullet_types[bullet_type] < 5:
                player.attacker_inventory.bullet_types[bullet_type] += 1

        player.attacker_inventory.last_bullet_return_time = current_time

def bullet_cd(player):
    global last_shot_time
    current_time = pygame.time.get_ticks()
    new_bullet = None

    if current_time - last_shot_time < 1200:  # cooldown
        return

    if player.selected_bullet_type == "bomba":
        if player.attacker_inventory.use_bullet("bomba"):
            new_bullet = BombBullet(player.rect.centerx - 32, player.rect.centery + 15)
        else:
            player.message_timer_balas = 100  # Mostrar mensaje de falta de balas durante 1 segundo
    elif player.selected_bullet_type == "fuego":
        if player.attacker_inventory.use_bullet("fuego"):
            new_bullet = FireBullet(player.rect.centerx - 32, player.rect.centery + 15)
        else:
            player.message_timer_balas = 100  # Mostrar mensaje de falta de balas durante 1 segundo
    elif player.selected_bullet_type == "agua":
        if player.attacker_inventory.use_bullet("agua"):
            new_bullet = WaterBullet(player.rect.centerx - 32, player.rect.centery + 15)
        else:
            player.message_timer_balas = 100  # Mostrar mensaje de falta de balas durante 1 segundo

    if new_bullet is not None:
        bullets.add(new_bullet)
        last_shot_time = current_time

class BlockScreen:
    def __init__(self, player1_username, player2_username, player1_role, tank_img, game_time, idioma):
        pygame.init()
        window_width = 800
        window_height = 600
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Eagle Defender")

        self.screen_width = window_width
        self.screen_height = window_height

        self.player1_username = player1_username
        self.player2_username = player2_username
        self.player1_role = player1_role
        self.tank_img = tank_img
        self.game_time = game_time
        self.idioma = idioma

        self.half_time_text_displayed = False

        self.pause_start_time = 0
        self.selected_button_paused = 0

        self.pause_window_active = False
        self.confirmation_window_active = False

        self.player = Player(self.tank_img)
        self.player.update_tank_image(self.tank_img)  # Llama al método para actualizar la imagen
        self.players = pygame.sprite.Group()
        self.players.add(self.player)

        self.defender_turn_over = False
        self.state = "game"

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

        # Crea una instancia del inventario del atacante
        self.attacker_inventory = AttackerInventory()

        # Carga la imagen del águila
        self.eagle_image = pygame.image.load("aguila3.png")
        self.eagle_alive = True

        # Por si quiere que el àguila sea del mismo tamaño que las celdas
        #self.eagle_image = pygame.transform.scale(self.eagle_image, (self.CELDA, self.CELDA))
        self.eagle_rect = self.eagle_image.get_rect()

        # timer
        self.timer_duration = self.game_time * 1000  # 90 segundos

        print(self.timer_duration)

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

    def show_help_popup(self):
        if self.idioma == "spanish":
            help_image = pygame.image.load("assets/help_pygame.png")
        elif self.idioma == "english":
            help_image = pygame.image.load("assets/help_pygame_english.png")

        help_image_rect = help_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        help_popup = pygame.display.set_mode((800, 600))
        if self.idioma == "spanish":
            pygame.display.set_caption("Ayuda")
        if self.idioma == "english":
            pygame.display.set_caption("Help")

        # Posición y dimensiones del botón de cierre
        button_rect = pygame.Rect(700, 10, 80, 30)
        button_color = (255, 0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Verifica eventos de clic del mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True  # Usuario cerró la ventana

            help_popup.blit(help_image, help_image_rect)

            # Dibuja el botón de cierre
            pygame.draw.rect(help_popup, button_color, button_rect)
            font = pygame.font.Font(None, 36)
            if self.idioma == "spanish":
                text = font.render("Cerrar", True, (255, 255, 255))
            elif self.idioma == "english":
                text = font.render("Close", True, (255, 255, 255))
            help_popup.blit(text, button_rect.move(10, 5))

            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return True  # Usuario cerró la ventana

    def draw_pause_button(self):
        button_size = 30
        margin = 10
        button_rect = Rect(self.screen.get_width() - button_size - margin, margin, button_size, button_size)

        pygame.draw.rect(self.screen, (200, 200, 200), button_rect)  # Color gris para el botón
        pygame.draw.line(self.screen, (0, 0, 0), (button_rect.left + 5, button_rect.top + 5),
                         (button_rect.right - 5, button_rect.bottom - 5), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (button_rect.left + 5, button_rect.bottom - 5),
                         (button_rect.right - 5, button_rect.top + 5), 2)

        return button_rect

    def draw_pause_window(self):
        window_width = 300
        window_height = 300  # Aumenté la altura para dejar espacio al botón de ayuda y al texto del volumen
        window_rect = Rect((self.screen.get_width() - window_width) // 2,
                           (self.screen.get_height() - window_height) // 2,
                           window_width, window_height)

        pygame.draw.rect(self.screen, (255, 255, 255), window_rect)  # Color blanco para la ventana

        font = pygame.font.Font(None, 36)
        resume_button_rect = Rect(window_rect.left + 50, window_rect.top + 50, 200, 40)
        quit_button_rect = Rect(window_rect.left + 50, window_rect.top + 100, 200, 40)
        help_button_rect = Rect(window_rect.left + 50, window_rect.top + 150, 200, 40)  # Nuevo botón de ayuda

        pygame.draw.rect(self.screen, (200, 200, 200), resume_button_rect)  # Color gris para el botón
        pygame.draw.rect(self.screen, (200, 200, 200), quit_button_rect)  # Color gris para el botón
        pygame.draw.rect(self.screen, (200, 200, 200), help_button_rect)  # Color gris para el botón de ayuda

        resume_text = font.render("Resume", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))
        help_text = font.render("Help", True, (0, 0, 0))  # Texto para el botón de ayuda

        self.screen.blit(resume_text, resume_button_rect.move(10, 5).topleft)
        self.screen.blit(quit_text, quit_button_rect.move(10, 5).topleft)
        self.screen.blit(help_text, help_button_rect.move(10, 5).topleft)  # Coloca el texto del botón de ayuda

        # Texto de volumen
        volume_text = font.render("Volumen", True, (0, 0, 0))
        self.screen.blit(volume_text, (window_rect.left + 50, window_rect.top + 210))

        # Controlador de volumen
        volume_slider_rect = Rect(window_rect.left + 50, window_rect.top + 250, 200, 20)
        pygame.draw.rect(self.screen, (0, 0, 0), volume_slider_rect)  # Fondo negro
        volume_slider_value = int(self.volume * volume_slider_rect.width)
        pygame.draw.rect(self.screen, (200, 200, 200), (
            volume_slider_rect.left, volume_slider_rect.top, volume_slider_value,
            volume_slider_rect.height))  # Indicador gris

        return [resume_button_rect, quit_button_rect, help_button_rect, volume_slider_rect]

    def draw_player_info(self):
        font = pygame.font.Font(None, 24)
        # Definir las coordenadas y el color del texto
        text_color = (0, 0, 0)

        if self.player1_role == "defender":
            # Si el jugador 1 es el defensor, mostrar sus datos en la esquina inferior izquierda
            if self.idioma == "spanish":
                username_text = font.render(f"Defensor: {self.player1_username}", True, text_color)
            if self.idioma == "english":
                username_text = font.render(f"Defender: {self.player1_username}", True, text_color)
            username_rect = username_text.get_rect(topleft=(20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        else:
            # Si el jugador 1 es el atacante, mostrar sus datos en la esquina inferior derecha
            if self.idioma == "spanish":
                username_text = font.render(f"Atacante: {self.player1_username}", True, text_color)
            if self.idioma == "english":
                username_text = font.render(f"Attacker: {self.player1_username}", True, text_color)
            username_rect = username_text.get_rect(topright=(self.screen.get_width() - 20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        # Muestra la información del jugador 2 (el que no seleccionó el jugador 1)
        if self.player1_role == "defender":
            if self.idioma == "spanish":
                username_text = font.render(f"Atacante: {self.player2_username}", True, text_color)
            if self.idioma == "english":
                username_text = font.render(f"Attacker: {self.player2_username}", True, text_color)
            username_rect = username_text.get_rect(topright=(self.screen.get_width() - 20, self.screen.get_height() - 40))
            self.screen.blit(username_text, username_rect)
        else:
            if self.idioma == "spanish":
                username_text = font.render(f"Defensor: {self.player2_username}", True, text_color)
            if self.idioma == "english":
                username_text = font.render(f"Defender: {self.player2_username}", True, text_color)
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
        global is_paused
        global pause_start_time
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
                    if event.key == pygame.K_p:
                        is_paused = not is_paused
                        if is_paused:
                            pygame.mixer.music.pause()
                            pause_start_time = pygame.time.get_ticks()
                            self.draw_pause_window()
                        else:
                            pygame.mixer.music.unpause()
                            pass

                        # Evitar eventos adicionales mientras se mantiene presionada la tecla
                        pygame.event.clear(pygame.KEYUP)
                        pygame.event.clear(pygame.KEYDOWN)
                        pygame.time.delay(200)

                    if self.defender_turn_over:
                    # Bloquea el movimiento y la selección de bloques si el turno del defensor ha terminado
                        continue

                    if is_paused:
                        continue
                    else:
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
            fondojuego = pygame.image.load("assets/fondojuego.png")
            self.screen.blit(fondojuego, (0,0))


            if self.state == "game":
                self.dibujar_cuadricula()
                self.dibujar_imagenes()
                self.draw_player_info()
                pause_button_rect = self.draw_pause_button()

                if is_paused:

                    elements = self.draw_pause_window()

                    volume_slider_rect = elements[3]
                    quit_button_rect = elements[1]
                    resume_button_rect = elements[0]
                    help_button_rect = elements[2]

                    volume_slider_value = int(self.volume * volume_slider_rect.width)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if resume_button_rect.collidepoint(event.pos):
                                is_paused = False
                                pygame.mixer.music.unpause()
                                self.timer_start += pygame.time.get_ticks() - pause_start_time
                            elif help_button_rect.collidepoint(event.pos):
                                # Si se presiona el botón de ayuda, muestra la ventana emergente y verifica si se cerró
                                if self.show_help_popup():
                                    # Usuario cerró la ventana de ayuda, vuelve a la pantalla principal
                                    is_paused = False
                                    pygame.mixer.music.unpause()
                                    self.timer_start += pygame.time.get_ticks() - pause_start_time
                            elif quit_button_rect.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                # Reducir el volumen con la flecha izquierda
                                volume_slider_value = max(0, volume_slider_value - 20)
                                self.volume = volume_slider_value / volume_slider_rect.width
                                pygame.mixer.music.set_volume(self.volume)
                            elif event.key == pygame.K_RIGHT:
                                # Aumentar el volumen con la flecha derecha
                                volume_slider_value = min(volume_slider_rect.width, volume_slider_value + 20)
                                self.volume = volume_slider_value / volume_slider_rect.width
                                pygame.mixer.music.set_volume(self.volume)
                            elif event.key == pygame.K_DOWN:
                                # Cambia al siguiente botón
                                self.selected_button_paused = (self.selected_button_paused + 1) % len(elements)
                            elif event.key == pygame.K_UP:
                                # Cambia al botón anterior
                                self.selected_button_paused = (self.selected_button_paused - 1) % len(elements)
                            elif event.key == pygame.K_RETURN:
                                # Realiza la acción asociada al botón seleccionado
                                selected_button = elements[self.selected_button_paused]
                                if isinstance(selected_button, pygame.Rect):
                                    # Es un rectángulo (botón), realiza la acción correspondiente
                                    if selected_button == resume_button_rect:
                                        is_paused = False
                                        pygame.mixer.music.unpause()
                                        self.timer_start += pygame.time.get_ticks() - pause_start_time
                                    elif selected_button == help_button_rect:
                                        if self.show_help_popup():
                                            is_paused = False
                                            pygame.mixer.music.unpause()
                                            self.timer_start += pygame.time.get_ticks() - pause_start_time
                                    elif selected_button == quit_button_rect:
                                        pygame.quit()
                                        sys.exit()


                    # Render and display the timer on the screen
                font = pygame.font.Font(None, 36)
                if not is_paused:
                    current_time = pygame.time.get_ticks()
                    elapsed_time = current_time - self.timer_start
                    remaining_time = max(0, self.timer_duration - elapsed_time)
                minutes, seconds = divmod(remaining_time // 1000, 60)

                timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
                timer_rect = timer_text.get_rect(center=(self.screen.get_width() // 2, 30))
                self.screen.blit(timer_text, timer_rect)

                if self.defender_turn_over:

                    global bailabilidad_label
                    global acustica_label
                    global tempo_label
                    global popularidad_label
                    global extra_agua

                    if remaining_time <= self.timer_duration // 2 and not self.half_time_text_displayed:
                        # Pausar el tiempo
                        pause_start_time = pygame.time.get_ticks()
                        self.is_paused = True

                        self.attacker_inventory.adjust_water_bullets(extra_agua)

                        print("Cantidad de balas de agua extra " + str(self.attacker_inventory.bullet_types["agua"]))


                        if self.idioma == "spanish":
                            dynamic_text = f"Beneficio Foráneo! \n Bailabilidad: {str(bailabilidad_label)}\nAcústica: {str(acustica_label)}\nTempo: {str(tempo_label)}\nPopularidad: {str(popularidad_label)}\n Balas de agua extra: {str(extra_agua)}"
                        elif self.idioma == "english":
                            dynamic_text = f"Foreign Benefit! \n Bailability: {str(bailabilidad_label)}\nAcoustic: {str(acustica_label)}\nTempo: {str(tempo_label)}\nPopularity: {str(popularidad_label)}\n Extra Water Balls: {str(extra_agua)}"
  

                        half_time_font = pygame.font.Font(None, 48)
                        half_time_text = half_time_font.render(dynamic_text, True, (255, 0, 0))

                        # Dividir el texto en líneas individuales
                        lines = dynamic_text.split('\n')

                        # Obtener la altura de cada línea de texto
                        line_height = half_time_text.get_height()

                        # Calcular la altura total del bloque de texto
                        total_height = len(lines) * line_height

                        # Calcular la posición y mostrar cada línea por separado
                        for i, line in enumerate(lines):
                            text_surface = half_time_font.render(line, True, (255, 0, 0))
                            text_rect = text_surface.get_rect(
                                center=(self.screen.get_width() // 2,
                                        self.screen.get_height() // 2 - total_height // 2 + i * line_height))
                            self.screen.blit(text_surface, text_rect)

                        pygame.display.flip()  # Actualizar la pantalla para mostrar el texto
                        pygame.time.delay(5000)  # Esperar 5 segundos
                        self.half_time_text_displayed = True

                        # Reanudar el tiempo después de mostrar el mensaje
                        self.is_paused = False
                        self.timer_start += pygame.time.get_ticks() - pause_start_time

                    if remaining_time == 0 and self.eagle_alive == True:
                        self.state = "defender_winner"
                        self.init_music("Songs/Especial")

                    #if gana el tanque
                        #self.state = "attacker_winner"

                if remaining_time == 0 and self.turn_timer_expired == False:
                    self.show_confirmation_screen()
                    self.turn_timer_expired = True


                # Dibuja el águila en la posición deseada basada en las coordenadas de la cuadrícula
                eagle_x = self.POS_X_MARCO + eagle_col * self.CELDA
                eagle_y = self.POS_Y_MARCO + eagle_row * self.CELDA
                self.screen.blit(self.eagle_image, (eagle_x, eagle_y))

                # Dibuja el inventario del defensor
                inventory_x = 20
                inventory_y = 10
                inventory_spacing = 60
                for block_type in BLOCK_TYPES:
                    count = self.inventory_defender.blocks[block_type]
                    self.draw_inventory_block(inventory_x, inventory_y, block_type, count)
                    inventory_x += inventory_spacing

                if message_timer > 0:
                    font = pygame.font.Font(None, 36)
                    if self.idioma == "spanish":
                        text = font.render("No tienes bloques disponibles", True, (0, 0, 0))
                    if self.idioma == "english":
                        text = font.render("No available blocks", True, (0, 0, 0))

                    text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                    self.screen.blit(text, text_rect)
                    message_timer -= 1

                # Dibuja el inventario de balas
                bullet_inventory_x = 600
                bullet_inventory_y = 10
                for bullet_type in BULLETS_TYPES:
                    count_bullets = self.attacker_inventory.bullet_types[bullet_type]
                    self.draw_bullet_inventory(bullet_inventory_x, bullet_inventory_y, bullet_type, count_bullets)
                    bullet_inventory_x += inventory_spacing

                player_instance = self.players.sprites()[0]



                if self.confirmation_received == True:
                    self.players.update()
                    self.players.draw(self.screen)
                    bullets.update()
                    bullets.draw(self.screen)
                    if player_instance.message_timer_balas > 0:  # Accede a message_timer_balas en la instancia del jugador
                        font = pygame.font.Font(None, 36)
                        if self.idioma == "spanish":
                            text = font.render("No tienes balas disponibles", True, (0, 0, 0))
                        if self.idioma == "english":
                            text = font.render("No available bullets", True, (0, 0, 0))
                        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                        self.screen.blit(text, text_rect)
                        player_instance.message_timer_balas -= 1

                pygame.display.flip()


            elif self.state == "defender_winner":
                self.screen.fill((8, 93, 21))
                fondo_winner = pygame.image.load("assets/fondo_sin_cosas.png")
                self.screen.blit(fondo_winner, (0,0))

                pygame.display.flip()

            elif self.state == "attacker_winner":
                self.screen.fill((8, 93, 21))
                fondo_winner = pygame.image.load("assets/fondo_sin_cosas.png")
                self.screen.blit(fondo_winner, (0,0))

                pygame.display.flip()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


    def show_confirmation_screen(self):
        self.defender_turn_over = True
        confirmation_font = pygame.font.Font(None, 40)
        if self.idioma == "spanish":
            confirmation_text = confirmation_font.render("Turno completado. ¿Listo para el siguiente jugador?", True, (0, 0, 0))
        if self.idioma == "english":
            confirmation_text = confirmation_font.render("Turn complete. Ready for the next player?", True, (0, 0, 0))
        confirmation_rect = confirmation_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(confirmation_text, confirmation_rect)
        pygame.mixer.music.stop()

        pygame.display.flip()

        while not self.confirmation_received:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.confirmation_received = True

                    self.attacker_songs = "User_Data/Fav_Songs"
                    self.init_music(self.attacker_songs)

                    self.timer_start = pygame.time.get_ticks()
                    self.turn_timer_expired = False

    def draw_inventory_block(self, x, y, block_type, count):
        block_image = self.inventory_defender.block_images.get(block_type)

        if block_image is not None:
            # Escala la imagen del bloque a un tamaño más pequeño (40x40 píxeles)
            block_image = pygame.transform.scale(block_image, (40, 40))

            block_image.set_alpha(230)

            # Coordenadas para centrar la imagen y el texto
            image_x = x + 5
            image_y = y + 5

            # Dibuja la imagen del bloque
            self.screen.blit(block_image, (image_x, image_y))

            pygame.draw.rect(self.screen, (0, 0, 0), (image_x, image_y, 40, 40), 2)

            font = pygame.font.Font(None, 20)
            text = font.render(block_type.capitalize(), True, (0, 0, 0))

            # Coordenadas para el texto
            text_x = x + 25 - text.get_width() // 2
            text_y = y + 50

            self.screen.blit(text, (text_x, text_y))

            count_text = font.render(str(count), True, (0, 0, 0))

            # Coordenadas para el contador
            count_x = x + 25 - count_text.get_width() // 2
            count_y = y + 25

            self.screen.blit(count_text, (count_x, count_y))

    def draw_bullet_inventory(self, x, y, bullet_type, count_bullets):
        bullet_image = self.attacker_inventory.bullet_images.get(bullet_type)

        if bullet_image is not None:
            # Escala la imagen del proyectil a un tamaño más pequeño (40x40 píxeles)
            bullet_image = pygame.transform.scale(bullet_image, (40, 40))

            bullet_image.set_alpha(200)

            # Coordenadas para centrar la imagen y el texto
            image_x = x + 5
            image_y = y + 5

            # Dibuja la imagen del proyectil
            self.screen.blit(bullet_image, (image_x, image_y))

            pygame.draw.rect(self.screen, (0, 0, 0), (image_x, image_y, 40, 40), 2)

            font = pygame.font.Font(None, 20)
            text = font.render(bullet_type.capitalize(), True, (0, 0, 0))

            # Coordenadas para el texto
            text_x = x + 25 - text.get_width() // 2
            text_y = y + 50

            self.screen.blit(text, (text_x, text_y))

            count_text = font.render(str(count_bullets), True, (0, 0, 0))

            # Coordenadas para el contador
            count_x = x + 25 - count_text.get_width() // 2
            count_y = y + 25

            self.screen.blit(count_text, (count_x, count_y))

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
        global bailabilidad_label
        global acustica_label
        global tempo_label
        global popularidad_label
        global extra_agua
        
        song_path = self.song_list[self.current_song_index]
        print(song_path)

        # Conectar a la base de datos
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        # Obtener datos asociados a la canción desde la base de datos
        cursor.execute("SELECT bailabilidad, acustico, tempo, popularidad FROM users WHERE cancion_favorita=?", (song_path,))
        datos_cancion = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        connection.close()

        if datos_cancion:
            bailabilidad, acustica, tempo, popularidad = datos_cancion

            bailabilidad_label = bailabilidad
            acustica_label = acustica
            tempo_label = tempo
            popularidad_label = popularidad
            extra_agua = (popularidad // bailabilidad * acustica + tempo)
        else:
            print(f"No se encontraron datos para la canción: {song_path}")

        # Cargar la canción en el mezclador de música de pygame
        pygame.mixer.music.load(song_path)

        # Configurar el evento de finalización para activar la reproducción en bucle
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        # Reproducir la canción en bucle
        pygame.mixer.music.play(-1)  # El argumento -1 indica reproducción en bucle