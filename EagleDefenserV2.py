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
import time
import threading

# Variable global para rastrear si hay una partida en curso
game_in_progress = False

# Tipos de bloques disponibles
BLOCK_TYPES = ["concreto", "madera", "acero"]

class main_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.button_login = customtkinter.CTkButton(self, text="Iniciar sesión", command=self.login,fg_color="transparent")
        self.button_login.place(relx=0.5, rely=0.5, anchor="center")

        self.button_play = customtkinter.CTkButton(self, text="Jugar", command=self.register, fg_color="transparent")
        self.button_play.place(relx=0.5, rely=0.6, anchor="center")
        
        self.song_directory = "Songs/Menu"  # Carpeta donde se encuentran las canciones
        self.song_list = []  # Lista de canciones en la carpeta

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

    def register(self): # Restricción de una Partida a la vez
        #global game_in_progress
        #if not game_in_progress:
        #    game_in_progress = True
        self.destroy()
        app = LogIn_Screen_2()
        app.title("Eagle Defender")
        app.minsize(900, 600)
        app.mainloop()
        #    start_game()
            
        #else:
        #    print("Ya hay una partida en curso")

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
                start_game()
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
        
        self.button_play = customtkinter.CTkButton(self, text="Play",command=self.play)
        self.button_play.place(relx=0.5, rely=0.8, anchor="center")

        self.button_back = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.button_back.place(relx=0.5, rely=0.9, anchor="center")

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
                start_game()
            else:
                print("Error en las credenciales")
                
    def play(self): # Restricción de una Partida a la vez
        global game_in_progress
        if not game_in_progress:
            game_in_progress = True
            self.destroy()
            start_game()
        else:
            print("Ya hay una partida en curso")           
    
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

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self): #empieza clase Player
        super().__init__() #parent class
        self.sprite_path = pygame.image.load('assets/tank.png')
        self.rect = self.sprite_path.get_rect()
        self.image = self.sprite_path
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 200
        self.x_change = 0
        self.y_change = 0
        self.hearts = 6
        self.speed = 1

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
        self.speed = -4

    def update(self):
        self.rect.move_ip(self.speed, 0)
        global last_shot_time
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 320:
            self.kill()

def bullet_cd(player): #cooldown de balas de jugador
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time < 600: #cooldown
        return
    new_bullet = PlayerBullet(player.rect.centerx-32, player.rect.centery+15) #cada vez que termina el cooldown agrega la clase bala a su grupo. o sea dispara
    bullets.add(new_bullet)
    last_shot_time = current_time #le hace update al ultimo shot reseteando el cooldown

class BlockScreen:
    def __init__(self):
        pygame.init()
        window_width = 800
        window_height = 600
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Eagle Defender")

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

        self.confirmation_button_color = (200, 200, 200)  # Color gris
        self.confirmation_button_rect = pygame.Rect(650, 530, 120, 40) 
        self.confirmation_button_font = pygame.font.Font(None, 25)
        self.confirmation_button_text = "Confirmar Turno"

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
        if 0 <= fila < self.NUM_CELDAS and 0 <= columna < self.NUM_CELDAS:
            return bool(self.matriz_celdas[fila][columna])
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
                 
            self.draw_confirmation_button()     

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
        