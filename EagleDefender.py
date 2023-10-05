from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_FILES
import pygame
import os
import sqlite3

class MainScreen:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        self.label_username = Label(self.canvas, text="Nombre de usuario")
        self.label_username.place(x=300, y=200, width=200, height=50)
        self.entry_username = Entry(self.canvas)
        self.entry_username.place(x=300, y=250, width=200, height=50)

        self.label_password = Label(self.canvas, text="Contraseña")
        self.label_password.place(x=300, y=300, width=200, height=50)
        self.entry_password = Entry(self.canvas)
        self.entry_password.place(x=300, y=350, width=200, height=50)

        self.button_login = Button(self.canvas, text="Iniciar sesión", command=self.login)
        self.button_login.place(x=300, y=400, width=200, height=50)

        self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
        self.button_register.place(x=300, y=450, width=200, height=50)

        self.button_play = Button(self.canvas, text="Jugar", command=self.play)
        self.button_play.place(x=300, y=500, width=200, height=50)

    def play(self):
        self.canvas.destroy()
        window.destroy()
        start_game()

    def login(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute('''
        SELECT * FROM users WHERE nickname=? AND correo=?
        ''', (self.entry_username.get(), self.entry_password.get()))

        user = cursor.fetchone()
        connection.close()

        if user:
            print("Inicio de sesión exitoso")
            self.play()  # puedes redirigir al juego después de iniciar sesión con éxito
        else:
            print("Error en las credenciales")


    def register(self):
        self.canvas.destroy()
        RegisterScreen(window)

class RegisterScreen:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        # Label de Registro
        self.label_register = Label(self.canvas, text="Registro")
        self.label_register.place(x=300, y=0, width=200, height=30)

        # Nombre
        self.label_nombre = Label(self.canvas, text="Nombre: ")
        self.label_nombre.place(x=170, y=50, width=200, height=30)
        self.entry_nombre = Entry(self.canvas)
        self.entry_nombre.place(x=300, y=50, width=200, height=30)

        # Nickname
        self.label_nickname = Label(self.canvas, text="Nickname: ")
        self.label_nickname.place(x=160, y=90, width=200, height=30)
        self.entry_nickname = Entry(self.canvas)
        self.entry_nickname.place(x=300, y=90, width=200, height=30)

        # Contraseña
        self.label_password = Label(self.canvas, text="Contraseña: ")
        self.label_password.place(x=150, y=150, width=200, height=30)
        self.entry_password = Entry(self.canvas)
        self.entry_password.place(x=300, y=150, width=200, height=30)

        # Correo
        self.label_correo = Label(self.canvas, text="Correo: ")
        self.label_correo.place(x=170, y=210, width=200, height=30)
        self.entry_correo = Entry(self.canvas)
        self.entry_correo.place(x=300, y=210, width=200, height=30)

        # Edad
        self.label_edad = Label(self.canvas, text="Edad: ")
        self.label_edad.place(x=170, y=270, width=200, height=30)
        self.entry_edad = Entry(self.canvas)
        self.entry_edad.place(x=300, y=270, width=200, height=30)

        # Red Social
        self.label_red_social = Label(self.canvas, text="Red Social: ")
        self.label_red_social.place(x=140, y=330, width=200, height=30)
        self.entry_red_social = Entry(self.canvas)
        self.entry_red_social.place(x=300, y=330, width=200, height=30)

        # Foto
        self.label_foto = Label(self.canvas, text="Foto (ruta): ")
        self.label_foto.place(x=140, y=390, width=200, height=30)
        # Arrastar y subir foto
        self.entry_foto = Entry(self.canvas) 
        self.entry_foto.place(x=300, y=390, width=200, height=30)

        # Canción Favorita
        self.label_cancion = Label(self.canvas, text="Canción Favorita: ")
        self.label_cancion.place(x=140, y=450, width=200, height=30)
        self.entry_cancion = Entry(self.canvas)
        self.entry_cancion.place(x=300, y=450, width=200, height=30)

        # Botón Registrarse
        self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
        self.button_register.place(x=150, y=500, width=200, height=50)

        # Botón Volver
        self.button_back = Button(self.canvas, text="Volver", command=self.back)
        self.button_back.place(x=450, y=500, width=200, height=50)

    def register(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute('''
            INSERT INTO users (nombre, nickname, correo, edad, red_social, foto, cancion_favorita)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.entry_nombre.get(),
                self.entry_nickname.get(),
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
        self.canvas.destroy()
        MainScreen(window)


def start_game():
    pygame.init()
    game_Screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Eagle Defender")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False
                    global window
                    pygame.quit()
                    window = Tk()
                    MainScreen(window)
                    window.title("Eagle Defender")
                    window.minsize(800, 600)
                    window.mainloop()

        game_Screen.fill((0, 0, 0))
        pygame.display.flip()

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

window = Tk()
main_Screen = MainScreen(window)
window.title("Eagle Defender")
window.minsize(800, 600)
window.mainloop()

    