from tkinter import *
import pygame

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
        print("Login")

    def register(self):
        self.canvas.destroy()
        RegisterScreen(window)

class RegisterScreen:
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

        self.button_register = Button(self.canvas, text="Registrarse", command=self.register)
        self.button_register.place(x=300, y=400, width=200, height=50)

        self.button_back = Button(self.canvas, text="Volver", command=self.back)
        self.button_back.place(x=300, y=450, width=200, height=50)

    def register(self):
        print("Register")

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
                    main_Screen = MainScreen(window)
                    window.title("Eagle Defender")
                    window.minsize(800, 600)
                    window.mainloop()

        game_Screen.fill((0, 0, 0))
        pygame.display.flip()



window = Tk()
main_Screen = MainScreen(window)
window.title("Eagle Defender")
window.minsize(800, 600)
window.mainloop()

    