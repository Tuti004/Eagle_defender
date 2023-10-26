import sqlite3
import tkinter as tk
from tkinter import messagebox
import pygame


first_user = None
# Configuración de la base de datos
def setup_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
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

# Función para validar el inicio de sesión
def login(nickname, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE nickname=? AND password=?", (nickname, password))
    user = cursor.fetchone()
    connection.close()
    return user

def show_pygame_window(first_user, second_user):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Bienvenidos a pygame')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Mostrar información del primer usuario
        font = pygame.font.SysFont(None, 36)
        text = font.render(first_user[2], True, (0, 0, 0))
        screen.blit(text, (100, 50))
        
        user_image1 = pygame.image.load(first_user[7])
        user_image1 = pygame.transform.scale(user_image1, (50, 50))
        screen.blit(user_image1, (50, 100))
        
        # Mostrar información del segundo usuario
        text = font.render(second_user[2], True, (0, 0, 0))
        screen.blit(text, (500, 50))
        
        user_image2 = pygame.image.load(second_user[7])
        user_image2 = pygame.transform.scale(user_image2, (50, 50))
        screen.blit(user_image2, (450, 100))

        pygame.display.flip()

    pygame.quit()

# Función para el botón de inicio de sesión
def on_login_button_clicked():
    global first_user
    user = login(entry_nickname.get(), entry_password.get())
    
    if not user:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return

    if first_user is None:
        first_user = user
        entry_nickname.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        return
    else:
        root.destroy()
        show_pygame_window(first_user, user)

# Crear ventana tkinter
root = tk.Tk()
root.title('Iniciar Sesión')

label_nickname = tk.Label(root, text="Nickname")
label_nickname.pack(pady=10)
entry_nickname = tk.Entry(root)
entry_nickname.pack(pady=10)

label_password = tk.Label(root, text="Password")
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

button_login = tk.Button(root, text="Iniciar Sesión", command=on_login_button_clicked)
button_login.pack(pady=20)

root.mainloop()
