import customtkinter
import pygame
import sqlite3
import sys
import threading

# Variable global para rastrear si hay una partida en curso
game_in_progress = False

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

    def play(self): #Restricción de una Partida a la vez
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



def start_game():
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

    class BlockScreen:
        def __init__(self):
            pygame.init()
            window_width = 800
            window_height = 600
            self.screen = pygame.display.set_mode((window_width, window_height))
            pygame.display.set_caption("Eagle Defender")

            # Define the grid cell size and dimensions
            cell_size = 50
            rows = 12  # Number of rows
            cols = 16  # Number of columns

            # Create a 2D grid to represent the blocks
            self.grid = [[None for _ in range(cols)] for _ in range(rows)]

            # Main loop
            placing_block = False
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            x, y = event.pos
                            col = x // cell_size
                            row = y // cell_size
                            if 0 <= row < rows and 0 <= col < cols:
                                self.grid[row][col] = Block(row, col, cell_size)
                                placing_block = True
                    elif event.type == pygame.MOUSEMOTION:
                        if placing_block:
                            x, y = event.pos
                            col = x // cell_size
                            row = y // cell_size
                            if 0 <= row < rows and 0 <= col < cols:
                                self.grid[row][col] = Block(row, col, cell_size)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:  # Left mouse button
                            placing_block = False

                self.screen.fill((255, 255, 255))  # Fill the screen with white

                # Calculate the size of the grid area
                grid_width = cols * cell_size - 100
                grid_height = rows * cell_size - 100
                grid_x = (window_width - grid_width) // 2
                grid_y = (window_height - grid_height) // 2

                # Draw the grid
                for i in range(rows + 1):
                    y = grid_y + i * cell_size
                    pygame.draw.line(self.screen, (0, 0, 0), (grid_x, y), (grid_x + grid_width, y), 1)
                for i in range(cols + 1):
                    x = grid_x + i * cell_size
                    pygame.draw.line(self.screen, (0, 0, 0), (x, grid_y), (x, grid_y + grid_height), 1)

                # Draw the blocks on the grid
                for row in range(rows):
                    for col in range(cols):
                        if self.grid[row][col] is not None:
                            self.grid[row][col].draw(self.screen)   

                pygame.display.flip()

            pygame.quit()
            sys.exit()

    if __name__ == "__main__":
        main_Screen = BlockScreen()

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
    
setup_database()

app = main_Screen()
app.title("Eagle Defender")
app.minsize(800, 600)
app.mainloop()
        