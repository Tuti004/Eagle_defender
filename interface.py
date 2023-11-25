import customtkinter
import pygame
import sqlite3
from tkinter import filedialog
import yt_dlp as youtube_dl
import os
import shutil
from pydub import AudioSegment
from UI.CTkWidgets_Factory import *
from UI.HelpScreen_Builder import *
from game import BlockScreen

from UI.Music_DependencyInversion import ShuffleDI
from tkinter import *
from UI.SkinManager_SingleResponsibility import TankSkinManager

# Variable global para rastrear si hay una partida en curso
game_in_progress = False

defender_role = None
attacker_role = None

player1_data = None
player2_data = None

idioma = "spanish"

tank_skin_manager = TankSkinManager()

# Lee el valor desde el archivo game_config.txt
with open('game_config.txt', 'r') as file:
    # Lee una línea del archivo
    line = file.readline()
    # Encuentra la parte de la línea que contiene el valor numérico
    value_part = line.split('=')[1].strip()
    # Convierte el valor a entero
    game_time = int(value_part)
print("initial gametime: " + str(game_time))

class role_selection_1:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        self.img = PhotoImage(file=tank_skin_manager.get_current_skin_path())
        self.tank_image = self.canvas.create_image(280,330, image=self.img, anchor="nw")

        if idioma == "spanish":
            self.label_role = Label(self.canvas, text=f"Jugador 1, elige tu rol:")
            self.button_attacker = Button(self.canvas, text="Atacante", command=self.set_role_attacker)
            self.button_defender = Button(self.canvas, text="Defensor", command=self.set_role_defender)
            self.button_back = Button(self.canvas, text="Atras", command=self.back)

            

        if idioma == "english":
            self.label_role = Label(self.canvas, text=f"Player 1, choose your role:")
            self.button_attacker = Button(self.canvas, text="Attacker", command=self.set_role_attacker)
            self.button_defender = Button(self.canvas, text="Defender", command=self.set_role_defender)
            self.button_back = Button(self.canvas, text="Back", command=self.back)

        #player 1 role
        self.label_role.place(relx=0.5, rely=0.4, anchor="center")

        #attacker button
        self.button_attacker.place(relx=0.4, rely=0.5, anchor="center")
        
        self.button_skin = Button(self.canvas, text = ">", command=self.counter)
        self.button_skin.place(relx=0.4, rely=0.7, anchor="center")
                
        #defener button
        self.button_defender.place(relx=0.6, rely=0.5, anchor="center")

        #back button
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")

    def counter(self):
        tank_skin_manager.next_skin()  # Cambia el skin al siguiente
        menu_selected_skin = tank_skin_manager.get_current_skin_path()
        self.img = PhotoImage(file=menu_selected_skin)

        # Actualiza la imagen en el canvas
        self.canvas.itemconfig(self.tank_image, image=self.img)

    def set_role_attacker(self):
        global attacker_role
        attacker_role = True
        self.canvas.destroy()
        LogIn_Screen_2(window)
    
    def set_role_defender(self):
        global defender_role
        defender_role = True
        self.canvas.destroy()
        LogIn_Screen_2(window)

    def back(self):
        global player1_data
        player1_data = None
        self.canvas.destroy()
        LogIn_Screen(window)

class role_selection_2:
    def __init__(self, master):
        global defender_role
        global attacker_role

        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        if idioma == "spanish":
            self.label_role = Label(self.canvas, text=f"Jugador 2, elige tu rol:")
            self.button_attacker = Button(self.canvas, text="Atacante", command=self.set_role_attacker)
            self.button_defender = Button(self.canvas, text="Defensor", command=self.set_role_defender)
            self.button_back = Button(self.canvas, text="Atras", command=self.back)

        if idioma == "english":
            self.label_role = Label(self.canvas, text=f"Player 2, choose your role:")
            self.button_attacker = Button(self.canvas, text="Attacker", command=self.set_role_attacker)
            self.button_defender = Button(self.canvas, text="Defender", command=self.set_role_defender)
            self.button_back = Button(self.canvas, text="Back", command=self.back)

        #player 2 role
        self.label_role.place(relx=0.5, rely=0.4, anchor="center")

        if defender_role == True:
            #attacker role
            self.button_attacker.place(relx=0.5, rely=0.5, anchor="center")

            self.img = PhotoImage(file=tank_skin_manager.get_current_skin_path())
            self.tank_image = self.canvas.create_image(370 ,330, image=self.img, anchor="nw")

            self.button_skin = Button(self.canvas, text = ">", command=self.counter)
            self.button_skin.place(relx=0.5, rely=0.7, anchor="center")


        elif attacker_role == True:
            #defender
            self.button_defender.place(relx=0.5, rely=0.5, anchor="center")
        
        #back button
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")
    
    def set_role_attacker(self):
        global player2_data
        global player1_data
        tank_img = tank_skin_manager.get_current_skin_path()
        self.canvas.destroy()
        window.destroy()
        start_game(player1_data, player2_data, tank_img)
    
    def set_role_defender(self):
        global player2_data
        global player1_data
        tank_img = tank_skin_manager.get_current_skin_path()
        self.canvas.destroy()
        window.destroy()
        start_game(player1_data, player2_data, tank_img)
    
    def counter(self):
        tank_skin_manager.next_skin()  # Cambia el skin al siguiente
        menu_selected_skin = tank_skin_manager.get_current_skin_path()
        self.img = PhotoImage(file=menu_selected_skin)

        # Actualiza la imagen en el canvas
        self.canvas.itemconfig(self.tank_image, image=self.img)
    
    def back(self):
        global player2_data
        player2_data = None
        self.canvas.destroy()
        LogIn_Screen_2(window)
    

class language:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)
        global idioma
        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/background_test.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        self.language1 = PhotoImage(file="assets/language1.png")
        self.canvas.create_image(90, 120, image=self.language1, anchor="nw")

        self.language2 = PhotoImage(file="assets/language2.png")
        self.canvas.create_image(160, 150, image=self.language2, anchor="nw")

        #boton idioma
        self.button_idioma = Button(self.canvas, text="Language/Idioma", command=self.language_change)
        self.button_idioma.place(relx=0.5, rely=0.8, anchor="center")


        self.button_back = Button(self.canvas, text="Empezar/Start", command=self.back)
        self.button_back.place(relx=0.5, rely=0.6, anchor="center")

    def back(self):
        self.canvas.destroy()
        main_Screen(window)    

    def language_change(self):
        global idioma
        if idioma == "spanish":
            idioma = "english"

    



class main_Screen:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)
        global idioma
        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/background_test.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        if idioma == "spanish":
            self.button_login = Button(self.canvas, text="Iniciar sesión", command=self.login, highlightthickness=0, bg="SystemButtonFace")
            self.button_help = Button(self.canvas, text="Ayuda", command=self.help)
            self.button_leaderboard = Button(self.canvas, text="Salon De Fama", command=self.leaderboard)
            

        if idioma == "english":
            self.button_login = Button(self.canvas, text="Sign in", command=self.login, highlightthickness=0, bg="SystemButtonFace")
            self.button_help = Button(self.canvas, text="Help", command=self.help)
            self.button_leaderboard = Button(self.canvas, text="Leaderboard", command=self.leaderboard)
            
        #logo    
        self.img = PhotoImage(file="assets/Eagle_Defender_title.png")
        self.canvas.create_image(100,120, image=self.img, anchor="nw")
        #login
        self.button_login.place(relx=0.5, rely=0.5, anchor="center")
        #help
        self.button_help.place(relx=0.5, rely=0.7, anchor="center")
        #leaderboard
        self.button_leaderboard.place(relx=0.5, rely=0.6, anchor="center")

        self.setup_music_player()

        # Slider de volumen
        self.volume_slider = customtkinter.CTkSlider(self.canvas, from_=0, to=1, number_of_steps=100, orientation="horizontal")
        self.volume_slider.set(self.volume)
        self.volume_slider.place(relx=0.5, rely=0.8, anchor="center")
        self.volume_slider.bind("<Motion>", self.update_volume)

    def login(self):
        LogIn_Screen(window)
        self.canvas.destroy()

    def invite(self): # Restricción de una Partida a la vez
        global game_in_progress
        if not game_in_progress:
            game_in_progress = True

        LogIn_Screen_2(window)
        self.canvas.destroy()
        
    def help(self):
        help_screen_builder = HelpScreenBuilder()
        help_screen_director = HelpScreenDirector(help_screen_builder)
        help_screen_director.construct()
        help_screen = help_screen_builder.get_help_screen()

    def leaderboard(self):
        Leaderboard_Screen(window)
        self.canvas.destroy()

    def setup_music_player(self):
        pygame.mixer.init()
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)

        self.song_directory = "Songs/Menu"
        self.song_list = []

        for root, dirs, files in os.walk(self.song_directory):
            for file in files:
                if file.endswith(".mp3"):
                    self.song_list.append(os.path.join(root, file))
        print(self.song_list)

        self.current_song_index = 0

        self.strategy = ShuffleDI(self.canvas, self.song_list)
        self.strategy.play_next_song()


    def update_volume(self, event):
        # Actualiza el volumen según el valor del slider
        self.volume = self.volume_slider.get()
        pygame.mixer.music.set_volume(self.volume)

class Leaderboard_Screen:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)
        global idioma

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0, 0, image=self.background, anchor="nw")

        # leaderboard_title
        self.help_title = PhotoImage(file="assets/Leaderboard_title.png")
        self.canvas.create_image(190, 120, image=self.help_title, anchor="nw")







        self.button_back = Button(self.canvas, text="Back", command=self.back)
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")

    def back(self):
        self.canvas.destroy()
        main_Screen(window)

class LogIn_Screen:
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)
        global idioma

         # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        if idioma == "spanish":
            self.label_username = Label(self.canvas, text="Nombre de usuario:")
            self.label_password = Label(self.canvas, text="Contraseña:")
            self.button_login = Button(self.canvas, text="Iniciar sesión", command=self.login)
            self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
            self.button_back = Button(self.canvas, text="Atras", command=self.back)

        if idioma == "english":
            self.label_username = Label(self.canvas, text="Username: ")
            self.label_password = Label(self.canvas, text="Password:")
            self.button_login = Button(self.canvas, text="Sign in", command=self.login)
            self.button_register = Button(self.canvas, text="Register", command=self.register)
            self.button_back = Button(self.canvas, text="Back", command=self.back)

        # Login_title
        self.img = PhotoImage(file="assets/login_title.png")
        self.canvas.create_image(300,120, image=self.img, anchor="nw")

        #user input
        self.label_username.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_username = Entry(self.canvas)
        self.entry_username.place(relx=0.6, rely=0.4, anchor="center")

        #password input
        self.label_password.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_password = Entry(self.canvas, show="*")
        self.entry_password.place(relx=0.6, rely=0.5,anchor="center")

        #login button
        self.button_login.place(relx=0.5, rely=0.6, anchor="center")

        #register button
        self.button_register.place(relx=0.5, rely=0.7, anchor="center")

        #back button
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")
  

    def register(self):
        self.canvas.destroy()
        register_Screen(window)

    def login(self):
        global player1_data
        global player1
        if self.entry_username.get() == "admin" and self.entry_password.get() == "123":
            pygame.mixer.music.stop()

            self.canvas.destroy()
            Admin_Screen(window)
        
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
                player1 = True
                player1_data = user
                self.canvas.destroy()
                role_selection_1(window)
            else:
                print("Error en las credenciales")

    def back(self):
        global player1_data
        player1_data = None
        self.canvas.destroy()
        main_Screen(window)
        
class LogIn_Screen_2():
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        if idioma == "spanish":
            self.label_username = Label(self.canvas, text="Nombre de usuario:")
            self.label_password = Label(self.canvas, text="Contraseña:")
            self.button_login = Button(self.canvas, text="Iniciar sesión", command=self.login)
            self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
            self.button_back = Button(self.canvas, text="Atras", command=self.back)

        if idioma == "english":
            self.label_username = Label(self.canvas, text="Username: ")
            self.label_password = Label(self.canvas, text="Password:")
            self.button_login = Button(self.canvas, text="Sign in", command=self.login)
            self.button_register = Button(self.canvas, text="Register", command=self.register)
            self.button_back = Button(self.canvas, text="Back", command=self.back)

        # Login_title
        self.img = PhotoImage(file="assets/login_title.png")
        self.canvas.create_image(300,120, image=self.img, anchor="nw")

        #user input
        self.label_username.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_username = Entry(self.canvas)
        self.entry_username.place(relx=0.6, rely=0.4, anchor="center")

        #password input
        self.label_password.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_password = Entry(self.canvas, show="*")
        self.entry_password.place(relx=0.6, rely=0.5,anchor="center")

        #login button
        self.button_login.place(relx=0.5, rely=0.6, anchor="center")

        #register button
        self.button_register.place(relx=0.5, rely=0.7, anchor="center")

        #back button
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")

    def register(self):
        self.destroy()
        register_Screen(window)

    def login(self):
        global player2_data
        global player1_data
        if self.entry_username.get() == "admin" and self.entry_password.get() == "123":
            pygame.mixer.music.stop()
            self.canvas.destroy()
            Admin_Screen(window)
        
        else:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            cursor.execute('''
            SELECT * FROM users WHERE nickname=? AND password=?
            ''', (self.entry_username.get(), self.entry_password.get()))

            user = cursor.fetchone()
            connection.close()

            if user:
                if user[1] == player1_data[1]:
                    print("No puedes jugar contigo mismo")
                    return
                else:
                    print("Inicio de sesión exitoso")
                    player2_data = user
                    self.canvas.destroy()
                    role_selection_2(window)                 
            else:
                print("Error en las credenciales")

    def back(self):
        self.canvas.destroy()
        role_selection_1(window)

class register_Screen():
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')   
        self.canvas.place(x=0, y=0)

        # EJEMPLO DE FONDO

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")

        # Obtiene el tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtiene el tamaño de la imagen de fondo
        image_width = self.background.width()
        image_height = self.background.height()

        # Escala la imagen de fondo al tamaño de la ventana
        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0,0, image=self.background, anchor="nw")

        # Cargar la imagen
        self.default_user = PhotoImage(file="assets/default_user.png")

        # Cambiar el tamaño de la imagen
        width = 180  # Ancho deseado
        height = 180  # Alto deseado
        self.default_user = self.default_user.zoom(width // self.default_user.width(), height // self.default_user.height())

        # Mostrar la imagen en el lienzo
        self.canvas.create_image(60, 120, image=self.default_user, anchor="nw")
        self.uploaded_files = []

        # register title
        self.img = PhotoImage(file="assets/Register_title.png")
        self.canvas.create_image(240,30, image=self.img, anchor="nw")

        if idioma == "spanish":
            self.label_nombre = Label(self.canvas, text="Nombre: ")
            self.label_nickname = Label(self.canvas, text="Pronombre: ")
            self.label_password = Label(self.canvas, text="Contraseña: ")
            self.label_correo = Label(self.canvas, text="Correo: ")
            self.label_edad = Label(self.canvas, text="Edad: ")
            self.label_red_social = Label(self.canvas, text="Red Social: ")
            self.button_upload_photo = Button(self.canvas, text="Subir Foto", command=self.upload_photo)
            self.button_upload_song = Button(self.canvas, text="Subir Canción", command=self.upload_song)
            self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
            self.button_back = Button(self.canvas, text="Atras", command=self.back)

        if idioma == "english":
            self.label_nombre = Label(self.canvas, text="Name: ")
            self.label_nickname = Label(self.canvas, text="Nickname: ")
            self.label_password = Label(self.canvas, text="Password: ")
            self.label_correo = Label(self.canvas, text="Email: ")
            self.label_edad = Label(self.canvas, text="Age: ")
            self.label_red_social = Label(self.canvas, text="Social Media: ")
            self.button_upload_photo = Button(self.canvas, text="Upload Picture", command=self.upload_photo)
            self.button_upload_song = Button(self.canvas, text="Upload Song", command=self.upload_song)
            self.button_register = Button(self.canvas, text="Register", command=self.register)
            self.button_back = Button(self.canvas, text="Back", command=self.back)


        # Nombre
        self.label_nombre.place(relx=0.5, rely=0.3, anchor="center")
        self.entry_nombre = Entry(self.canvas)
        self.entry_nombre.place(relx=0.7, rely=0.3, anchor="center")

        # Nickname
        self.label_nickname.place(relx=0.5, rely=0.4, anchor="center")
        self.entry_nickname = Entry(self.canvas)
        self.entry_nickname.place(relx=0.7, rely=0.4, anchor="center")

        # Contraseña
        self.label_password.place(relx=0.5, rely=0.5, anchor="center")
        self.entry_password = Entry(self.canvas)
        self.entry_password.place(relx=0.7, rely=0.5, anchor="center")

        # Correo
        self.label_correo.place(relx=0.5, rely=0.6, anchor="center")
        self.entry_correo = Entry(self.canvas)
        self.entry_correo.place(relx=0.7, rely=0.6, anchor="center")

        # Edad
        self.label_edad.place(relx=0.5, rely=0.7, anchor="center")
        self.entry_edad = Entry(self.canvas)
        self.entry_edad.place(relx=0.7, rely=0.7, anchor="center")

        # Red Social
        self.label_red_social.place(relx=0.5, rely=0.8, anchor="center")
        self.entry_red_social = Entry(self.canvas)
        self.entry_red_social.place(relx=0.7, rely=0.8, anchor="center")

        #Foto
        self.entry_foto = Entry(self.canvas)
        self.button_upload_photo.place(x=150, y=300, anchor="center")

        #Canción favorita
        self.entry_cancion = Entry(self.canvas)
        self.button_upload_song.place(x=150, y=400, anchor="center")

        # Botón Registrarse
        self.button_register.place(relx=0.55, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back.place(relx=0.7, rely=0.9, anchor="center")

        self.warning_messages = {
            "password_length": "La contraseña debe tener al menos 8 caracteres",
            "invalid_email": "Correo inválido",
            "invalid_age": "Edad inválido",
            "nickname_exists": "Nickname usado",
            "email_exists": "Correo usado"
        }

   
    
    def add_user_file(self, folder_name):
        if folder_name == "Photos":
            filetypes = [('JPEG files', '*.jpeg'), ('JPG files', '*.jpg'), ('PNG files', '*.png')]
        elif folder_name == "Fav_Songs":
            filetypes = [('MP3 files', '*.mp3')]
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            destination_folder = os.path.join("User_Data", folder_name)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            destination_path = os.path.join(destination_folder, os.path.basename(file_path))
            self.uploaded_files.append(destination_path)  # Agrega la ruta al archivo
            
            if file_path.endswith(('.jpg', '.jpeg', '.png')):
                shutil.copy2(file_path, destination_path)
            elif file_path.endswith('.mp3'):
                song = AudioSegment.from_mp3(file_path)
                if len(song) > 240000:  # 1:30 minutes in milliseconds
                    song = song[:240000]
                    song.export(destination_path, format="mp3")
                else:
                    shutil.copy2(file_path, destination_path)
            return destination_path
        return None
    
    def upload_photo(self):
        photo_path = self.add_user_file("Photos")
        if photo_path:
            self.entry_foto.delete(0, "end")
            self.entry_foto.insert(0, photo_path)
        
    def upload_song(self):
        song_path = self.add_user_file("Fav_Songs")
        if song_path:
            self.entry_cancion.delete(0, "end")
            self.entry_cancion.insert(0, song_path)

            # Habilitar las entradas y etiquetas relacionadas con los datos de la canción

            # Lables para la cancion
            self.popularidad = Label(self.canvas, text="Popularidad: ")
            self.bailabilidad = Label(self.canvas, text="Bailabilidad: ")
            self.acustico = Label(self.canvas, text="Acústico: ")
            self.tempo = Label(self.canvas, text="Tempo: ")

            self.popularidad.place(x=130, y=450, anchor="center")
            self.bailabilidad.place(x=130, y=480, anchor="center")
            self.acustico.place(x=130, y=510, anchor="center")
            self.tempo.place(x=130, y=540, anchor="center")

            #Entrys para cada dato de cancion
            self.popularidad_entry = Entry(self.canvas, width=3)
            self.bailabilidad_entry = Entry(self.canvas, width=3)
            self.acustico_entry = Entry(self.canvas, width=3)
            self.tempo_entry = Entry(self.canvas, width=3)
            
            self.popularidad_entry.place(x=200, y=450, anchor="center")
            self.bailabilidad_entry.place(x=200, y=480, anchor="center")
            self.acustico_entry.place(x=200, y=510, anchor="center")
            self.tempo_entry.place(x=200, y=540, anchor="center")


    def cleanup_uploaded_files(self):
        for file_path in self.uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        self.uploaded_files = []  # Reset the list
    
    def register(self):
        if not self.entry_nombre.get() or not self.entry_nickname.get() or not self.entry_password.get() or not self.entry_correo.get() or not self.entry_edad.get():
            if idioma == "spanish":
                self.show_warning("Por favor, complete todos los campos.")
            if idioma == "english":
                self.show_warning("Please, complete all spaces")
            return
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        for case, warning_message in self.warning_messages.items():
            if case == "password_length" and len(self.entry_password.get()) < 8:
                self.show_warning(warning_message)
                connection.close()
                return
            elif case == "invalid_email" and (self.entry_correo.get().find("@") == -1 or self.entry_correo.get().find(".") == -1):
                self.show_warning(warning_message)
                connection.close()
                return
            elif case == "invalid_age":
                try:
                    edad = int(self.entry_edad.get())
                except ValueError:
                    self.show_warning(warning_message)
                    connection.close()
                    return
            elif case == "nickname_exists":
                cursor.execute("SELECT * FROM users WHERE nickname=?", (self.entry_nickname.get(),))
                if cursor.fetchone():
                    self.show_warning(warning_message)
                    connection.close()
                    return
            elif case == "email_exists":
                cursor.execute("SELECT * FROM users WHERE correo=?", (self.entry_correo.get(),))
                if cursor.fetchone():
                    self.show_warning(warning_message)
                    connection.close()
                    return
                
        if self.entry_foto.get() and os.path.exists(self.entry_foto.get()):
            user_photo_path = self.entry_foto.get()
        else:
            user_photo_path = "assets/default_user.png"

        if self.entry_cancion.get():  # Verifica si se proporciona una canción

            # Verifica si se proporcionan los datos de la canción
            if not self.bailabilidad_entry.get() or not self.acustico_entry.get() or not self.tempo_entry.get() or not self.popularidad_entry.get():
                if idioma == "spanish":
                    self.show_warning("Por favor, complete todos los campos.")
                if idioma == "english":
                    self.show_warning("Please, complete all spaces")
                connection.close()
                return

            try:
                cursor.execute('''
                INSERT INTO users (nombre, nickname, password, correo, edad, red_social, foto, cancion_favorita, bailabilidad, acustico, tempo, popularidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.entry_nombre.get(),
                    self.entry_nickname.get(),
                    self.entry_password.get(),
                    self.entry_correo.get(),
                    int(self.entry_edad.get()),  # convertir a entero
                    self.entry_red_social.get(),
                    user_photo_path,
                    self.entry_cancion.get(),
                    int(self.bailabilidad_entry.get()),  # convertir a entero
                    int(self.acustico_entry.get()),  # convertir a entero
                    int(self.tempo_entry.get()),  # convertir a entero
                    int(self.popularidad_entry.get())  # Convertir a entero
                ))
                connection.commit()
                print("Usuario registrado con éxito")
                self.uploaded_files = []  # Reset the list after successful registration
            except sqlite3.IntegrityError:
                print("El nickname ya está en uso")
        else:
            try:
                cursor.execute('''
                INSERT INTO users (nombre, nickname, password, correo, edad, red_social, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.entry_nombre.get(),
                    self.entry_nickname.get(),
                    self.entry_password.get(),
                    self.entry_correo.get(),
                    int(self.entry_edad.get()),  # convertir a entero
                    self.entry_red_social.get(),
                    user_photo_path
                ))
                connection.commit()
                print("Usuario registrado con éxito")
                self.uploaded_files = []  # Reset the list after successful registration
            except sqlite3.IntegrityError:
                print("El nickname ya está en uso")

        connection.close()

        self.back()

    def show_warning(self, warning_message):
        if hasattr(self, "warning_label"):
            self.warning_label.destroy()  # Elimina el Label de advertencia anterior si existe
        self.warning_label = Label(self.canvas, text=warning_message, fg="red")
        self.warning_label.place(relx=0.65, rely=0.95, anchor="center")
        self.canvas.after(5000, self.clear_warning)
    def clear_warning(self):
        if hasattr(self, "warning_label"):
            self.warning_label.destroy()
    
    def back(self):
        self.cleanup_uploaded_files()  # Limpia los archivos subidos
        self.canvas.destroy()
        LogIn_Screen(window)

class Admin_Screen(customtkinter.CTk):
    def __init__(self, master):
        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)

        self.songs_frames = {}
        self.players = {}
        pygame.mixer.init()
        self.current_song = None  # Almacena el nombre de la canción actual
        self.song_paused = False  # Indica si la canción está pausada o no

        # Label de Admin
        self.label_Admin = customtkinter.CTkLabel(self.canvas, text="Admin de canciones")
        self.label_Admin.place(relx=0.5, rely=0.05, anchor="center")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self.canvas, width=600, height=500)
        self.tabview.place(relx=0.5, rely=0.5, anchor="center")
        self.tab_names = ["Menu", "Defensor", "Config"]
        for tab_name in self.tab_names:
            self.tabview.add(tab_name)
            self.tabview.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.add_scrollable_frame_to_tab(tab_name)
        
        # Label de Menu
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Menu"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_menu = customtkinter.CTkEntry(self.tabview.tab("Menu"), width=200)
        self.entry_link_menu.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar", command=lambda: self.add_youtube("Menu", self.entry_link_menu.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Label de Defensor
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Defensor"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_defender = customtkinter.CTkEntry(self.tabview.tab("Defensor"), width=200)
        self.entry_link_defender.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar", command=lambda: self.add_youtube("Defensor", self.entry_link_defender.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        self.label_time = customtkinter.CTkLabel(self.tabview.tab("Config"), text="Tiempo de juego: ")
        self.label_time.place(relx=0.5, rely=0.1, anchor="center")

        self.time_90 = customtkinter.CTkButton(self.tabview.tab("Config"), text="1:30 min", command=lambda: self.set_time(90))
        self.time_90.place(relx=0.5, rely=0.2, anchor="center")

        self.time_120 = customtkinter.CTkButton(self.tabview.tab("Config"), text="2:00 min", command=lambda: self.set_time(120))
        self.time_120.place(relx=0.5, rely=0.3, anchor="center")

        self.time_150 = customtkinter.CTkButton(self.tabview.tab("Config"), text="2:30 min", command=lambda: self.set_time(150))
        self.time_150.place(relx=0.5, rely=0.4, anchor="center")

        self.time_180 = customtkinter.CTkButton(self.tabview.tab("Config"), text="3:00 min", command=lambda: self.set_time(180))
        self.time_180.place(relx=0.5, rely=0.5, anchor="center")

        self.time_210 = customtkinter.CTkButton(self.tabview.tab("Config"), text="3:30 min", command=lambda: self.set_time(210))
        self.time_210.place(relx=0.5, rely=0.6, anchor="center")

        self.time_240 = customtkinter.CTkButton(self.tabview.tab("Config"), text="4:00 min", command=lambda: self.set_time(240))
        self.time_240.place(relx=0.5, rely=0.7, anchor="center")

        # Botón para agregar canciones por archivo en cada tab
        self.button_add_file_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar desde sistema", command=lambda: self.add_file("Menu"))
        self.button_add_file_menu.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_defensor = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar desde sistema", command=lambda: self.add_file("Defensor"))
        self.button_add_file_defensor.place(relx=0.85, rely=0.1, anchor="center")

        # Variable para almacenar el estado de la subida y los posibles errores
        self.upload_status = customtkinter.StringVar(value="Estado: Esperando archivo o link...")
        for tab_name in self.tab_names:
            if tab_name == "Config":
                continue
            self.label_status = customtkinter.CTkLabel(self.tabview.tab(tab_name), textvariable=self.upload_status)
            self.label_status.place(relx=0.5, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self.canvas, text="Volver", command=self.back)
        self.button_back.place(relx=0.9, rely=0.05, anchor="center")

    def set_time(self, time):
        global game_time
        game_time = time
        # Escribe el nuevo valor en el archivo game_config.txt
        with open('game_config.txt', 'w') as file:
            file.write(f'game_time = {game_time}')

        print(f"Game Time set to: {game_time}")

    def add_scrollable_frame_to_tab(self, tab_name):
        if tab_name == "Config":
            return

        songs = self.load_songs_from_folder(tab_name)

        # Create a Tkinter frame
        frame = customtkinter.CTkFrame(self.tabview.tab(tab_name))
        frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.5, anchor="center")

        # Create an instance of SongList and place it inside the frame
        song_list = SongList(frame,
                             command1=lambda song_name, tn=tab_name: self.play_song(tn, song_name),
                             command2=lambda song_name, tn=tab_name: self.delete_song(tn, song_name)
                             )
        self.songs_frames[tab_name] = song_list
        for song in songs:
            song_list.add_item(song)

    def load_songs_from_folder(self, playlist):
        folder_path = os.path.join("Songs", playlist)
        songs = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        return songs
    
    def play_song(self, tab_name, song_name):
        # Comprueba si una canción ya está en reproducción
        if pygame.mixer.music.get_busy():
            if song_name == self.current_song:  # Si es la misma canción que ya está en reproducción
                if self.song_paused:
                    pygame.mixer.music.unpause()  # Si está pausada, reanudar la canción
                    self.song_paused = False
                else:
                    pygame.mixer.music.pause()   # Si está en reproducción, pausar la canción
                    self.song_paused = True
            else:  # Si es una canción diferente, detener la canción actual y comenzar a reproducir la nueva
                pygame.mixer.music.stop()
                self.load_and_play(tab_name, song_name)
        else:  # Si no hay ninguna canción en reproducción, comenzar a reproducir la canción seleccionada
            self.load_and_play(tab_name, song_name)

    def load_and_play(self, tab_name, song_name):
        song_path = os.path.join("Songs", tab_name, song_name)
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.current_song = song_name
        self.song_paused = False

    def delete_song(self, tab_name, song_name):
        # Stop the song if it's currently playing
        if tab_name in self.players and self.players[tab_name].get_busy():
            self.players[tab_name].stop()
            del self.players[tab_name]

        # Delete the song from the storage (disk)
        song_path = os.path.join("Songs", tab_name, song_name)
        if os.path.exists(song_path):
            os.remove(song_path)

        # Update the UI
        self.songs_frames[tab_name].remove_item(song_name)


    def update_song_buttons(self, playlist):
        pass  # Update song control buttons (e.g., disable if no song is selected)
    
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
                
                # Crop the file to 4:00 minutes if it is longer
                song = AudioSegment.from_mp3(file_path)
                if len(song) > 240000:  # 4:00 minutes in milliseconds
                    song = song[:240000]
                    song.export(destination_path, format="mp3")
                else:
                    # Copy the selected file to the corresponding folder
                    shutil.copy2(file_path, destination_path)
            self.upload_status.set(f"Estado: La canción ha sido agregado a {playlist_name} correctamente.")
            self.after(5000, self.reset_status)
            shutil.copy2(file_path, destination_path)
            self.songs_frames[playlist_name].add_item(os.path.basename(file_path))  # Update the song list in the UI
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
                        'exec_cmd': 'ffmpeg -i {} -t 240 -c:v copy -c:a copy {}.temp.mp3 && mv {}.temp.mp3 {}'
                    }
                ],
                'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
                'progress_hooks': [my_hook],
                'nocheckcertificate': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    print("Descarga y conversión finalizadas con éxito!")
                    info = ydl.extract_info(youtube_link, download=True)
                    file_name = ydl.prepare_filename(info)
                    file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
                    self.songs_frames[playlist_name].add_item(file_name_without_ext + ".mp3")
                    self.upload_status.set(f"Estado: Canción de YouTube agregada a {playlist_name} correctamente.")
                    self.canvas.after(5000, self.reset_status)
                except Exception as e:
                    error_msg = f"Error durante la descarga: {str(e)}"
                    print(error_msg)
                    self.upload_status.set(error_msg)
                    self.canvas.after(5000, self.reset_status)

    def reset_status(self):
        self.upload_status.set("Estado: Esperando archivo o link...")

    def back(self):
        self.canvas.destroy()
        main_Screen(window)


#Función para iniciar el juego
def start_game(player1, player2, tank_img):
    global game_in_progress
    global defender_role
    global attacker_role
    global game_time

    time = game_time

    print("Time before: " + str(time))
    
    player1_username = player1[2]
    player2_username = player2[2]

    if defender_role:
        player1_role = "defender"
    elif attacker_role:
        player1_role = "attacker"

    game_in_progress = True
    block_screen_instance = BlockScreen(player1_username, player2_username, player1_role, tank_img, time, idioma)
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
        cancion_favorita TEXT,
        bailabilidad INTEGER,
        acustico INTEGER,
        tempo INTEGER,
        popularidad INTEGER
    )
    ''')
    
    connection.commit()
    connection.close()

window = Tk()
setup_database()
Main_Screen = language(window)
window.title("Eagle Defender")
window.minsize(800, 600)
window.resizable(False, False)
window.mainloop()