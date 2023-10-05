import customtkinter

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
    
    def play(self):
        self.destroy()
        app.destroy()

    def register(self):
        self.destroy()
        app = register_Screen()
        app.mainloop()

    def login(self):
        print("Login")

class register_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

                # Label de Registro
        self.label_register = customtkinter.CTkLabel(self.canvas, text="Registro")
        self.label_register.place(x=300, y=0, width=200, height=30)

        # Nombre
        self.label_nombre = customtkinter.CTkLabel(self.canvas, text="Nombre: ")
        self.label_nombre.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_nombre = customtkinter.CTkEntry(self.canvas)
        self.entry_nombre.place(relx=0.6, rely=0.4, anchor="center")

        # Nickname
        self.label_nickname = customtkinter.CTkLabel(self.canvas, text="Nickname: ")
        self.label_nickname.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_nickname = customtkinter.CTkEntry(self.canvas)
        self.entry_nickname.place(relx=0.6, rely=0.4, anchor="center")

        # Contraseña
        self.label_password = customtkinter.CTkLabel(self.canvas, text="Contraseña: ")
        self.label_password.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_password = customtkinter.CTkEntry(self.canvas)
        self.entry_password.place(relx=0.6, rely=0.4, anchor="center")

        # Correo
        self.label_correo = customtkinter.CTkLabel(self.canvas, text="Correo: ")
        self.label_correo.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_correo = customtkinter.CTkEntry(self.canvas)
        self.entry_correo.place(relx=0.6, rely=0.4, anchor="center")

        # Edad
        self.label_edad = customtkinter.CTkLabel(self.canvas, text="Edad: ")
        self.label_edad.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_edad = customtkinter.CTkEntry(self.canvas)
        self.entry_edad.place(relx=0.6, rely=0.4, anchor="center")

        # Red Social
        self.label_red_social = customtkinter.CTkLabel(self.canvas, text="Red Social: ")
        self.label_red_social.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_red_social = customtkinter.CTkEntry(self.canvas)
        self.entry_red_social.place(relx=0.6, rely=0.4, anchor="center")

        # Foto
        self.label_foto = customtkinter.CTkLabel(self.canvas, text="Foto (ruta): ")
        self.label_foto.place(relx=0.6, rely=0.4, anchor="center")
        # Arrastar y subir foto
        self.entry_foto = customtkinter.CTkEntry(self.canvas) 
        self.entry_foto.place(relx=0.6, rely=0.4, anchor="center")

        # Canción Favorita
        self.label_cancion = customtkinter.CTkLabel(self.canvas, text="Canción Favorita: ")
        self.label_cancion.place(relx=0.6, rely=0.4, anchor="center")
        self.entry_cancion = customtkinter.CTkEntry(self.canvas)
        self.entry_cancion.place(relx=0.6, rely=0.4, anchor="center")

        # Botón Registrarse
        self.button_register = customtkinter.CTkButton(self.canvas, text="Registrarse", command=self.register)
        self.button_register.place(relx=0.6, rely=0.4, anchor="center")

        # Botón Volver
        self.button_back = customtkinter.CTkButton(self.canvas, text="Volver", command=self.back)
        self.button_back.place(relx=0.6, rely=0.4, anchor="center")



app = LogIn_Screen()
app.title("Eagle Defender")
app.minsize(800, 600)
app.mainloop()
        