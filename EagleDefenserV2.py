import customtkinter
import pygame
import sqlite3
import sys
from tkinter import filedialog
import yt_dlp as youtube_dl
import os
import shutil
from pydub import AudioSegment

# Variable global para rastrear si hay una partida en curso
game_in_progress = False

# Tipos de bloques disponibles
BLOCK_TYPES = ["concreto", "madera", "acero"]

class main_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.button_login = customtkinter.CTkButton(self, text="Iniciar sesión", command=self.login)
        self.button_login.place(relx=0.5, rely=0.5, anchor="center")

        self.button_play = customtkinter.CTkButton(self, text="Jugar", command=self.play)
        self.button_play.place(relx=0.5, rely=0.6, anchor="center")
        
    def login(self):
        self.destroy()
        app = LogIn_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()

    def play(self): # Restricción de una Partida a la vez
        global game_in_progress
        if not game_in_progress:
            game_in_progress = True
            self.destroy()
            start_game()
        else:
            print("Ya hay una partida en curso")

class LogIn_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.label_username = customtkinter.CTkLabel(self, text="Nombre de usuario:")
        self.label_username.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_username = customtkinter.CTkEntry(self)
        self.entry_username.place(relx=0.6, rely=0.4, anchor="center")

        self.label_password = customtkinter.CTkLabel(self, text="Contraseña:")
        self.label_password.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_password = customtkinter.CTkEntry(self)
        self.entry_password.place(relx=0.6, rely=0.5, anchor="center")

        self.button_login = customtkinter.CTkButton(self, text="Iniciar sesión", command=self.login)
        self.button_login.place(relx=0.5, rely=0.6, anchor="center")

        self.button_register = customtkinter.CTkButton(self, text="Registrarse", command=self.register)
        self.button_register.place(relx=0.5, rely=0.7, anchor="center")

        self.button_back = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")

    def register(self):
        self.destroy()
        app = register_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()

    def login(self):
        if self.entry_username.get() == "admin" and self.entry_password.get() == "123":
            self.destroy()
            app = Admin_Screen()
            app.title("Eagle Defender")
            app.minsize(800, 600)
            app.mainloop()
        
        else:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            cursor.execute('''
            SELECT * FROM users WHERE nickname=? AND password=?
            ''', (self.entry_username.get(), self.entry_password.get()))

            user = cursor.fetchone()
            connection.close()

            if user:
                print("Inicio de sesión exitoso")
                self.play()  # puedes redirigir al juego después de iniciar sesión con éxito
            else:
                print("Error en las credenciales")

    def back(self):
        self.destroy()
        app = main_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()

class register_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        # Label de Registro
        self.label_register = customtkinter.CTkLabel(self, text="Registro")
        self.label_register.place(relx=0.5, rely=0.2, anchor="center")

        # Nombre
        self.label_nombre = customtkinter.CTkLabel(self, text="Nombre: ")
        self.label_nombre.place(relx=0.4, rely=0.3, anchor="center")
        self.entry_nombre = customtkinter.CTkEntry(self)
        self.entry_nombre.place(relx=0.6, rely=0.3, anchor="center")

        # Nickname
        self.label_nickname = customtkinter.CTkLabel(self, text="Nickname: ")
        self.label_nickname.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_nickname = customtkinter.CTkEntry(self)
        self.entry_nickname.place(relx=0.6, rely=0.4, anchor="center")

        # Contraseña
        self.label_password = customtkinter.CTkLabel(self, text="Contraseña: ")
        self.label_password.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_password = customtkinter.CTkEntry(self)
        self.entry_password.place(relx=0.6, rely=0.5, anchor="center")

        # Correo
        self.label_correo = customtkinter.CTkLabel(self, text="Correo: ")
        self.label_correo.place(relx=0.4, rely=0.6, anchor="center")
        self.entry_correo = customtkinter.CTkEntry(self)
        self.entry_correo.place(relx=0.6, rely=0.6, anchor="center")

        # Edad
        self.label_edad = customtkinter.CTkLabel(self, text="Edad: ")
        self.label_edad.place(relx=0.4, rely=0.7, anchor="center")
        self.entry_edad = customtkinter.CTkEntry(self)
        self.entry_edad.place(relx=0.6, rely=0.7, anchor="center")

        # Red Social
        self.label_red_social = customtkinter.CTkLabel(self, text="Red Social: ")
        self.label_red_social.place(relx=0.4, rely=0.8, anchor="center")
        self.entry_red_social = customtkinter.CTkEntry(self)
        self.entry_red_social.place(relx=0.6, rely=0.8, anchor="center")

        # Foto
        self.label_foto = customtkinter.CTkLabel(self, text="Foto (ruta): ")
        self.label_foto.place(relx=0.2, rely=0.9, anchor="center")
        # Arrastar y subir foto
        self.entry_foto = customtkinter.CTkEntry(self) 
        self.entry_foto.place(relx=0.4, rely=0.9, anchor="center")

        # Canción Favorita
        self.label_cancion = customtkinter.CTkLabel(self, text="Canción Favorita: ")
        self.label_cancion.place(relx=0.6, rely=0.9, anchor="center")
        self.entry_cancion = customtkinter.CTkEntry(self)
        self.entry_cancion.place(relx=0.8, rely=0.9, anchor="center")

        # Botón Registrarse
        self.button_register = customtkinter.CTkButton(self, text="Registrarse", command=self.register)
        self.button_register.place(relx=0.4, rely=0.10, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self, text="Volver", command=self.back)
        self.button_back.place(relx=0.6, rely=0.10, anchor="center")
    
    def register(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute('''
            INSERT INTO users (nombre, nickname, password, correo, edad, red_social, foto, cancion_favorita)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.entry_nombre.get(),
                self.entry_nickname.get(),
                self.entry_password.get(),
                self.entry_correo.get(),
                int(self.entry_edad.get()),  # convertir a entero
                self.entry_red_social.get(),
                self.entry_foto.get(),
                self.entry_cancion.get()
            ))
            connection.commit()
            print("Usuario registrado con éxito")
        except sqlite3.IntegrityError:
            print("El nickname ya está en uso")

        connection.close()
    
    def back(self):
        self.destroy()
        app = LogIn_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()

class Admin_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        # Label de Admin
        self.label_Admin = customtkinter.CTkLabel(self, text="Admin de canciones")
        self.label_Admin.place(relx=0.5, rely=0.1, anchor="center")

         # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=500, height=400)
        self.tabview.place(relx=0.5, rely=0.5, anchor="center")
        self.tabview.add("Menu")
        self.tabview.add("Defensor")
        self.tabview.add("Atacante")
        self.tabview.add("Especial")
        self.tabview.tab("Menu").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Defensor").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Atacante").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Especial").grid_columnconfigure(0, weight=1)

        # Label de Menu
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Menu"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.3, anchor="center")
        self.entry_link_menu = customtkinter.CTkEntry(self.tabview.tab("Menu"), width=200)
        self.entry_link_menu.place(relx=0.4, rely=0.3, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar", command=lambda: self.add_youtube("Menu", self.entry_link_menu.get()))
        self.button_add_menu.place(relx=0.8, rely=0.3, anchor="center")

        # Label de Defensor
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Defensor"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.3, anchor="center")
        self.entry_link_defender = customtkinter.CTkEntry(self.tabview.tab("Defensor"), width=200)
        self.entry_link_defender.place(relx=0.4, rely=0.3, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar", command=lambda: self.add_youtube("Defensor", self.entry_link_defender.get()))
        self.button_add_menu.place(relx=0.8, rely=0.3, anchor="center")

        # Label de Atacante
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Atacante"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.3, anchor="center")
        self.entry_link_attacker = customtkinter.CTkEntry(self.tabview.tab("Atacante"), width=200)
        self.entry_link_attacker.place(relx=0.4, rely=0.3, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Atacante"), text="Agregar", command=lambda: self.add_youtube("Atacante", self.entry_link_attacker.get()))
        self.button_add_menu.place(relx=0.8, rely=0.3, anchor="center")

        # Label de Especial
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Especial"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.3, anchor="center")
        self.entry_link_special = customtkinter.CTkEntry(self.tabview.tab("Especial"), width=200)
        self.entry_link_special.place(relx=0.4, rely=0.3, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Especial"), text="Agregar", command=lambda: self.add_youtube("Especial", self.entry_link_special.get()))
        self.button_add_menu.place(relx=0.8, rely=0.3, anchor="center")

        
        # Botón para agregar canciones por archivo en cada tab
        self.button_add_file_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar desde sistema", command=lambda: self.add_file("Menu"))
        self.button_add_file_menu.place(relx=0.5, rely=0.5, anchor="center")

        self.button_add_file_defensor = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar desde sistema", command=lambda: self.add_file("Defensor"))
        self.button_add_file_defensor.place(relx=0.5, rely=0.5, anchor="center")

        self.button_add_file_atacante = customtkinter.CTkButton(self.tabview.tab("Atacante"), text="Agregar desde sistema", command=lambda: self.add_file("Atacante"))
        self.button_add_file_atacante.place(relx=0.5, rely=0.5, anchor="center")

        self.button_add_file_especial = customtkinter.CTkButton(self.tabview.tab("Especial"), text="Agregar desde sistema", command=lambda: self.add_file("Especial"))
        self.button_add_file_especial.place(relx=0.5, rely=0.5, anchor="center")

        # Variable para almacenar el estado de la subida y los posibles errores
        self.upload_status = customtkinter.StringVar(value="Estado: Esperando archivo o link...")

        # Agregar el label de estado en cada tabview
        self.label_status_menu = customtkinter.CTkLabel(self.tabview.tab("Menu"), textvariable=self.upload_status)
        self.label_status_menu.place(relx=0.5, rely=0.9, anchor="center")

        self.label_status_defensor = customtkinter.CTkLabel(self.tabview.tab("Defensor"), textvariable=self.upload_status)
        self.label_status_defensor.place(relx=0.5, rely=0.9, anchor="center")

        self.label_status_atacante = customtkinter.CTkLabel(self.tabview.tab("Atacante"), textvariable=self.upload_status)
        self.label_status_atacante.place(relx=0.5, rely=0.9, anchor="center")

        self.label_status_especial = customtkinter.CTkLabel(self.tabview.tab("Especial"), textvariable=self.upload_status)
        self.label_status_especial.place(relx=0.5, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self, text="Volver", command=self.back)
        self.button_back.place(relx=0.5, rely=0.9, anchor="center")
    
    def add_file(self, playlist_name):
        try:
            file_path = filedialog.askopenfilename(filetypes=[('MP3 files', '*.mp3')])
            if file_path:
                # Define the destination folder based on the playlist name
                destination_folder = os.path.join("Songs", playlist_name)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                
                # Define the destination path for the mp3 file
                destination_path = os.path.join(destination_folder, os.path.basename(file_path))
                
                # Crop the file to 1:30 minutes if it is longer
                song = AudioSegment.from_mp3(file_path)
                if len(song) > 90000:  # 1:30 minutes in milliseconds
                    song = song[:90000]
                    song.export(destination_path, format="mp3")
                else:
                    # Copy the selected file to the corresponding folder
                    shutil.copy2(file_path, destination_path)
            self.upload_status.set(f"Estado: La canción ha sido agregado a {playlist_name} correctamente.")
            self.after(5000, self.reset_status)
        except Exception as e:
            self.upload_status.set(f"Error: {str(e)}")
            self.after(5000, self.reset_status)

    def add_youtube(self, playlist_name, youtube_link):

        def my_hook(d):
            if d['status'] == 'finished':
                print('\nDescarga completada, convirtiendo...')
            if d['status'] == 'downloading':
                p = d['_percent_str']
                speed = d['_speed_str']
                print("\rDescargando... {0} a {1}".format(p, speed), end='')
        if youtube_link:
            folder_path = os.path.join("Songs", playlist_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {
                        'key': 'ExecAfterDownload',
                        'exec_cmd': 'ffmpeg -i {} -t 90 -c:v copy -c:a copy {}.temp.mp3 && mv {}.temp.mp3 {}'
                    }
                ],
                'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
                'progress_hooks': [my_hook],
                'nocheckcertificate': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(youtube_link, download=True)
                    file_name = ydl.prepare_filename(info)
                    print("Descarga y conversión finalizadas con éxito!")
                    self.upload_status.set(f"Estado: Canción de YouTube agregada a {playlist_name} correctamente.")
                    self.after(5000, self.reset_status)
                except Exception as e:
                    error_msg = f"Error durante la descarga: {str(e)}"
                    print(error_msg)
                    self.upload_status.set(error_msg)
                    self.after(5000, self.reset_status)

    def reset_status(self):
        self.upload_status.set("Estado: Esperando archivo o link...")
    
    def back(self):
        self.destroy()
        app = main_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()


class Block:
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.color = (255, 148, 212)

    def draw(self, screen):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(screen, self.color, (x, y, self.cell_size, self.cell_size))

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
        
class BlockScreen:
    def __init__(self):
        pygame.init()
        window_width = 800
        window_height = 600
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Eagle Defender")

        # Define el tamaño de la celda y las dimensiones de la cuadrícula
        self.cell_size = 50
        self.rows = 12
        self.cols = 16

        # Crea una cuadrícula de bloques inicialmente vacía
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Crea una instancia del inventario del defensor
        self.inventory_defender = Inventory_Defender()

    def main_loop(self):
        running = True
        selected_block = None
        message_timer = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        x, y = event.pos
                        col = (x - grid_x) // self.cell_size
                        row = (y - grid_y) // self.cell_size
                        if 0 <= row < self.rows and 0 <= col < self.cols:
                            # Comprueba si hay un bloque seleccionado en el inventario
                            if self.grid[row][col] is None:
                                if selected_block:
                                    if self.inventory_defender.use_block(selected_block):
                                        self.grid[row][col] = Block(row, col, self.cell_size)
                                    else:
                                        message_timer = 100  # Mostrar mensaje durante 100 ciclos
                                else:
                                    print("Selecciona un tipo de bloque del inventario primero")
                            else:
                                print("La celda ya está ocupada por un bloque")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_block = "concreto"
                    elif event.key == pygame.K_2:
                        selected_block = "madera"
                    elif event.key == pygame.K_3:
                        selected_block = "acero"

            self.screen.fill((255, 255, 255))  # Llena la pantalla de blanco


            # Calcula el tamaño del área de la cuadrícula
            grid_width = self.cols * self.cell_size
            grid_height = self.rows * self.cell_size
            grid_x = (800 - grid_width) // 2
            grid_y = (600 - grid_height) // 2

            # Dibuja la cuadrícula
            for i in range(self.rows + 1):
                y = grid_y + i * self.cell_size
                pygame.draw.line(self.screen, (0, 0, 0), (grid_x, y), (grid_x + grid_width, y), 1)
            for i in range(self.cols + 1):
                x = grid_x + i * self.cell_size
                pygame.draw.line(self.screen, (0, 0, 0), (x, grid_y), (x, grid_y + grid_height), 1)

            # Dibuja los bloques en la cuadrícula
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] is not None:
                        self.grid[row][col].draw(self.screen)

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

            pygame.display.flip()

        pygame.quit()
        sys.exit()

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

#Función para iniciar el juego
def start_game():
    global game_in_progress
    game_in_progress = True
    block_screen_instance = BlockScreen()
    block_screen_instance.main_loop()


def setup_database():
    # Conectar a la base de datos
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        nickname TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        correo TEXT NOT NULL,
        edad INTEGER,
        red_social TEXT,
        foto TEXT,
        cancion_favorita TEXT
    )
    ''')
    
    connection.commit()
    connection.close()
    
if __name__ == "__main__":
    setup_database()
    app = main_Screen()
    app.title("Eagle Defender")
    app.minsize(800, 600)
    app.mainloop()
        