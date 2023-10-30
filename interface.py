import customtkinter
import pygame
import sqlite3
from pygame.locals import *
import sys
from tkinter import filedialog
import yt_dlp as youtube_dl
import os
import shutil
from pydub import AudioSegment
from CTkWidgets import song_list
import random
from game import BlockScreen

# Variable global para rastrear si hay una partida en curso
game_in_progress = False


class main_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.button_login = customtkinter.CTkButton(self, text="Iniciar sesión", command=self.login,fg_color="transparent")
        self.button_login.place(relx=0.5, rely=0.5, anchor="center")
        
        self.song_directory = "Songs/Menu"  # Carpeta donde se encuentran las canciones
        self.song_list = []  # Lista de canciones en la carpeta
        
        self.button_help = customtkinter.CTkButton(self, text="Ayuda", command=self.help, fg_color="transparent")
        self.button_help.place(relx=0.5, rely=0.7, anchor="center")

        self.button_play = customtkinter.CTkButton(self, text="Play", command=self.play, fg_color="transparent")
        self.button_play.place(relx=0.5, rely=0.2, anchor="center")

        # Inicializar pygame para la reproducción de música
        pygame.mixer.init()
        self.volume = 0.5  # Volumen inicial
        pygame.mixer.music.set_volume(self.volume)  # Ajusta el volumen según tus preferencias

        # Llena la lista de canciones
        for root, dirs, files in os.walk(self.song_directory):
            for file in files:
                if file.endswith(".mp3"):
                    self.song_list.append(os.path.join(root, file))
        print(self.song_list)
        
        random.shuffle(self.song_list)
        self.current_song_index = 0
        self.play_next_song()

        # Slider de volumen
        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=1, number_of_steps=100, orientation="horizontal")
        self.volume_slider.set(self.volume)
        self.volume_slider.place(relx=0.5, rely=0.8, anchor="center")
        self.volume_slider.bind("<Motion>", self.update_volume)

    def login(self):
        self.destroy()
        app = LogIn_Screen()
        app.title("Eagle Defender")
        app.minsize(900, 600)
        app.mainloop()

    def invite(self): # Restricción de una Partida a la vez
        global game_in_progress
        if not game_in_progress:
            game_in_progress = True
            
        self.destroy()
        app = LogIn_Screen_2()
        app.title("Eagle Defender")
        app.minsize(900, 600)
        app.mainloop()
        
    def help(self):
        self.destroy()
        app = Help_Screen()
        app.title("Eagle Defender")
        app.minsize(900,600)
        app.mainloop()

    def play_next_song(self):
        """Reproduce la siguiente canción y establece un callback para cuando termine."""
        pygame.mixer.music.load(self.song_list[self.current_song_index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Establece un evento para el final de la canción
        
        song_length_ms = pygame.mixer.Sound(self.song_list[self.current_song_index]).get_length() * 1000  # Duración de la canción en milisegundos
        self.after(int(song_length_ms), self.play_next_song)  # Programa el callback para cuando termine la canción

        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)  # Ajusta el índice de la canción

    def update_volume(self, event):
        # Actualiza el volumen según el valor del slider
        self.volume = self.volume_slider.get()
        pygame.mixer.music.set_volume(self.volume)

class Help_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        
        self.label_info_eagle = customtkinter.CTkLabel(self, text="Movimiento del águila")
        self.label_info_eagle.place(relx=0.2, rely=0.2, anchor="center")
        
        self.label_info_blocks = customtkinter.CTkLabel(self, text="Bloques")
        self.label_info_blocks.place(relx=0.2, rely=0.6, anchor="center")
        
        self.label_info_tank = customtkinter.CTkLabel(self, text="Movmimiento del tanque")
        self.label_info_tank.place(relx=0.8, rely=0.2, anchor="center")
        
        self.label_info_shoot = customtkinter.CTkLabel(self, text="Disparos")
        self.label_info_shoot.place(relx=0.8, rely=0.6, anchor="center")
        
        self.button_back = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")
        
    def back(self):
        self.destroy()
        app = main_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()
            

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
        self.entry_password = customtkinter.CTkEntry(self, show="*")
        self.entry_password.place(relx=0.6, rely=0.5,anchor="center")

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
            pygame.mixer.music.stop()
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
                self.destroy()
                app = main_Screen()
                app.title("Eagle Defender")
                app.minsize(800,600)
                app.mainloop()
            else:
                print("Error en las credenciales")

    def back(self):
        self.destroy()
        app = main_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()
        
class LogIn_Screen_2(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.label_username = customtkinter.CTkLabel(self, text="Nombre de usuario:")
        self.label_username.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_username = customtkinter.CTkEntry(self)
        self.entry_username.place(relx=0.6, rely=0.4, anchor="center")

        self.label_password = customtkinter.CTkLabel(self, text="Contraseña:")
        self.label_password.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_password = customtkinter.CTkEntry(self, show="*")
        self.entry_password.place(relx=0.6, rely=0.5,anchor="center")

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
            pygame.mixer.music.stop()
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
                self.withdraw()
                start_game()                    
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

        self.uploaded_files = []

        # Label de Registro
        self.label_register = customtkinter.CTkLabel(self, text="Registro")
        self.label_register.place(relx=0.5, rely=0.1, anchor="center")

        # Nombre
        self.label_nombre = customtkinter.CTkLabel(self, text="Nombre: ")
        self.label_nombre.place(relx=0.4, rely=0.2, anchor="center")
        self.entry_nombre = customtkinter.CTkEntry(self)
        self.entry_nombre.place(relx=0.6, rely=0.2, anchor="center")

        # Nickname
        self.label_nickname = customtkinter.CTkLabel(self, text="Nickname: ")
        self.label_nickname.place(relx=0.4, rely=0.3, anchor="center")
        self.entry_nickname = customtkinter.CTkEntry(self)
        self.entry_nickname.place(relx=0.6, rely=0.3, anchor="center")

        # Contraseña
        self.label_password = customtkinter.CTkLabel(self, text="Contraseña: ")
        self.label_password.place(relx=0.4, rely=0.4, anchor="center")
        self.entry_password = customtkinter.CTkEntry(self)
        self.entry_password.place(relx=0.6, rely=0.4, anchor="center")

        # Correo
        self.label_correo = customtkinter.CTkLabel(self, text="Correo: ")
        self.label_correo.place(relx=0.4, rely=0.5, anchor="center")
        self.entry_correo = customtkinter.CTkEntry(self)
        self.entry_correo.place(relx=0.6, rely=0.5, anchor="center")

        # Edad
        self.label_edad = customtkinter.CTkLabel(self, text="Edad: ")
        self.label_edad.place(relx=0.4, rely=0.6, anchor="center")
        self.entry_edad = customtkinter.CTkEntry(self)
        self.entry_edad.place(relx=0.6, rely=0.6, anchor="center")

        # Red Social
        self.label_red_social = customtkinter.CTkLabel(self, text="Red Social: ")
        self.label_red_social.place(relx=0.4, rely=0.7, anchor="center")
        self.entry_red_social = customtkinter.CTkEntry(self)
        self.entry_red_social.place(relx=0.6, rely=0.7, anchor="center")

        #Foto
        self.entry_foto = customtkinter.CTkEntry(self)
        self.button_upload_photo = customtkinter.CTkButton(self, text="Subir Foto", command=self.upload_photo)
        self.button_upload_photo.place(relx=0.4, rely=0.8, anchor="center")

        #Canción favorita
        self.entry_cancion = customtkinter.CTkEntry(self)
        self.button_upload_song = customtkinter.CTkButton(self, text="Subir Canción Favorita", command=self.upload_song)
        self.button_upload_song.place(relx=0.6, rely=0.8, anchor="center")

        # Botón Registrarse
        self.button_register = customtkinter.CTkButton(self, text="Registrarse", command=self.register)
        self.button_register.place(relx=0.5, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self, text="Volver", command=self.back)
        self.button_back.place(relx=0.9, rely=0.1, anchor="center")
    
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
                if len(song) > 90000:  # 1:30 minutes in milliseconds
                    song = song[:90000]
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

    def cleanup_uploaded_files(self):
        for file_path in self.uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        self.uploaded_files = []  # Reset the list
    
    def register(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        # Validar password
        password = self.entry_password.get()
        if (len(password) < 8):
            print("La contrasena debe tener al menos 8 caracteres")
            connection.close()
            return
        
        #Validar que el correo tenga un formato adecuado
        correo = self.entry_correo.get()
        if (correo.find("@") == -1 and correo.find(".") == -1):
            print("El correo debe tener un formato adecuado")
            connection.close()
            return
        
        #Validad edad
        try:
            edad = int(self.entry_edad.get())
        except ValueError:
            print("La edad debe ser un número entero")
            connection.close()
            return
        
        # Verificar que se haya subido tanto una foto como una canción favorita
        if not self.entry_foto.get() or not self.entry_cancion.get():
            print("Debes subir tanto una foto como una canción favorita.")
            connection.close()
            return

        #Validar que el nickname y correo no estén en la base de datos
        cursor.execute("SELECT * FROM users WHERE nickname=?", (self.entry_nickname.get(),))
        if cursor.fetchone():
            print("El nickname ya está en uso")
            connection.close()
            return
        
        cursor.execute("SELECT * FROM users WHERE correo=?", (self.entry_correo.get(),))
        if cursor.fetchone():
            print("El correo ya está en uso")
            connection.close()
            return

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
            self.uploaded_files = []  # Reset the list after successful registration
        except sqlite3.IntegrityError:
            print("El nickname ya está en uso")

        connection.close()

        self.back()
    
    def back(self):
        self.cleanup_uploaded_files()  # Limpia los archivos subidos
        self.destroy()
        app = LogIn_Screen()
        app.title("Eagle Defender")
        app.minsize(800, 600)
        app.mainloop()

class Admin_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.songs_frames = {}
        self.players = {}
        pygame.mixer.init()
        self.current_song = None  # Almacena el nombre de la canción actual
        self.song_paused = False  # Indica si la canción está pausada o no

        # Label de Admin
        self.label_Admin = customtkinter.CTkLabel(self, text="Admin de canciones")
        self.label_Admin.place(relx=0.5, rely=0.05, anchor="center")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=600, height=500)
        self.tabview.place(relx=0.5, rely=0.5, anchor="center")
        self.tab_names = ["Menu", "Defensor", "Atacante", "Especial"]
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

        # Label de Atacante
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Atacante"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_attacker = customtkinter.CTkEntry(self.tabview.tab("Atacante"), width=200)
        self.entry_link_attacker.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Atacante"), text="Agregar", command=lambda: self.add_youtube("Atacante", self.entry_link_attacker.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Label de Especial
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Especial"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_special = customtkinter.CTkEntry(self.tabview.tab("Especial"), width=200)
        self.entry_link_special.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Especial"), text="Agregar", command=lambda: self.add_youtube("Especial", self.entry_link_special.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        
        # Botón para agregar canciones por archivo en cada tab
        self.button_add_file_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar desde sistema", command=lambda: self.add_file("Menu"))
        self.button_add_file_menu.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_defensor = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar desde sistema", command=lambda: self.add_file("Defensor"))
        self.button_add_file_defensor.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_atacante = customtkinter.CTkButton(self.tabview.tab("Atacante"), text="Agregar desde sistema", command=lambda: self.add_file("Atacante"))
        self.button_add_file_atacante.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_especial = customtkinter.CTkButton(self.tabview.tab("Especial"), text="Agregar desde sistema", command=lambda: self.add_file("Especial"))
        self.button_add_file_especial.place(relx=0.85, rely=0.1, anchor="center")

        # Variable para almacenar el estado de la subida y los posibles errores
        self.upload_status = customtkinter.StringVar(value="Estado: Esperando archivo o link...")

        # Agregar el label de estado en cada tabview
        self.upload_status = customtkinter.StringVar(value="Estado: Esperando archivo o link...")
        for tab_name in self.tab_names:
            label_status = customtkinter.CTkLabel(self.tabview.tab(tab_name), textvariable=self.upload_status)
            label_status.place(relx=0.5, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self, text="Volver", command=self.back)
        self.button_back.place(relx=0.9, rely=0.05, anchor="center")

    def add_scrollable_frame_to_tab(self, tab_name):
        songs = self.load_songs_from_folder(tab_name)
        frame = song_list(self.tabview.tab(tab_name),
                                           command1=lambda song_name, tn=tab_name: self.play_song(tn, song_name),
                                           command2=lambda song_name, tn=tab_name: self.delete_song(tn, song_name))
        frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.5, anchor="center")
        self.songs_frames[tab_name] = frame
        for song in songs:
            frame.add_item(song)

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
                        'exec_cmd': 'ffmpeg -i {} -t 90 -c:v copy -c:a copy {}.temp.mp3 && mv {}.temp.mp3 {}'
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
        