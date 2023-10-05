import customtkinter
import pygame
import sqlite3

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (250,250,51)
GREEN = (180, 212, 181)


#player class
class Player(pygame.sprite.Sprite):
    def __init__(self): #empieza clase Player
        super().__init__() #parent class
        self.sprite_path = pygame.image.load('assets/cohete_jugador.png')
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.x = 40
        self.y = 600/2
        self.x_change = 0
        self.y_change = 0
        self.hearts = 6
        self.speed = 5

    def player_imput(self): #esta funcion permite el moviento con wasd del jugador
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

bullets = pygame.sprite.Group()
last_shot_time = 0
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y): #el x y y aqui permite que cuando se agrege a bullets a su grupo de balas se ponga en las x y y del player
        super().__init__()
        self.sprite_path = pygame.image.load('assets/bala_jugador.png')        
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 400:
            self.kill()

def bullet_cd(player): #cooldown de balas de jugador
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time < 600: #cooldown
        return
    new_bullet = PlayerBullet(player.rect.centerx, player.rect.centery+15) #cada vez que termina el cooldown agrega la clase bala a su grupo. o sea dispara
    bullets.add(new_bullet)
    last_shot_time = current_time #le hace update al ultimo shot reseteando el cooldown

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

    def play(self):
        self.destroy()
        start_game()

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
                    app = main_Screen()
                    app.title("Eagle Defender")
                    app.minsize(800, 600)
                    app.mainloop()

        pygame.display.flip()
        game_Screen.fill((GREEN))
        player.update() 
        player.draw(game_Screen)   
        bullets.update()
        bullets.draw(game_Screen)   



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
        