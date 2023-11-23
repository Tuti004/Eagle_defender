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

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar",
                                                       command=lambda: self.add_youtube("Menu",
                                                                                        self.entry_link_menu.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Label de Defensor
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Defensor"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_defender = customtkinter.CTkEntry(self.tabview.tab("Defensor"), width=200)
        self.entry_link_defender.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Defensor"), text="Agregar",
                                                       command=lambda: self.add_youtube("Defensor",
                                                                                        self.entry_link_defender.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Label de Atacante
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Atacante"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_attacker = customtkinter.CTkEntry(self.tabview.tab("Atacante"), width=200)
        self.entry_link_attacker.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Atacante"), text="Agregar",
                                                       command=lambda: self.add_youtube("Atacante",
                                                                                        self.entry_link_attacker.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Label de Especial
        self.label_link = customtkinter.CTkLabel(self.tabview.tab("Especial"), text="Link: ")
        self.label_link.place(relx=0.1, rely=0.1, anchor="center")
        self.entry_link_special = customtkinter.CTkEntry(self.tabview.tab("Especial"), width=200)
        self.entry_link_special.place(relx=0.3, rely=0.1, anchor="center")

        self.button_add_menu = customtkinter.CTkButton(self.tabview.tab("Especial"), text="Agregar",
                                                       command=lambda: self.add_youtube("Especial",
                                                                                        self.entry_link_special.get()))
        self.button_add_menu.place(relx=0.6, rely=0.1, relwidth=0.15, anchor="center")

        # Botón para agregar canciones por archivo en cada tab
        self.button_add_file_menu = customtkinter.CTkButton(self.tabview.tab("Menu"), text="Agregar desde sistema",
                                                            command=lambda: self.add_file("Menu"))
        self.button_add_file_menu.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_defensor = customtkinter.CTkButton(self.tabview.tab("Defensor"),
                                                                text="Agregar desde sistema",
                                                                command=lambda: self.add_file("Defensor"))
        self.button_add_file_defensor.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_atacante = customtkinter.CTkButton(self.tabview.tab("Atacante"),
                                                                text="Agregar desde sistema",
                                                                command=lambda: self.add_file("Atacante"))
        self.button_add_file_atacante.place(relx=0.85, rely=0.1, anchor="center")

        self.button_add_file_especial = customtkinter.CTkButton(self.tabview.tab("Especial"),
                                                                text="Agregar desde sistema",
                                                                command=lambda: self.add_file("Especial"))
        self.button_add_file_especial.place(relx=0.85, rely=0.1, anchor="center")

        # Variable para almacenar el estado de la subida y los posibles errores
        self.upload_status = customtkinter.StringVar(value="Estado: Esperando archivo o link...")
        for tab_name in self.tab_names:
            self.label_status = customtkinter.CTkLabel(self.tabview.tab(tab_name), textvariable=self.upload_status)
            self.label_status.place(relx=0.5, rely=0.9, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self.canvas, text="Volver", command=self.back)
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
                    pygame.mixer.music.pause()  # Si está en reproducción, pausar la canción
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