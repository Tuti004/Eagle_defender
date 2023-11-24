from tkinter import *

class HelpScreenBuilder:
    def __init__(self):
        self.help_screen = HelpScreen()

    def build_background(self):
        self.help_screen.build_background()

    def build_sections(self):
        self.help_screen.build_sections()

    def build_buttons(self):
        self.help_screen.build_buttons()

    def get_help_screen(self):
        return self.help_screen

class HelpScreenDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_background()
        self.builder.build_sections()
        self.builder.build_buttons()

class HelpScreen:
    def __init__(self):
        self.master = None
        self.canvas = None

    def create_master(self):
        if self.master is None:
            self.master = Toplevel()

    def build_background(self):
        self.create_master()
        self.canvas = Canvas(self.master, width=800, height=600, highlightthickness=0, relief='ridge')
        self.canvas.pack()

        self.background = PhotoImage(file="assets/fondo_sin_cosas.png")
        window_width = 800
        window_height = 600
        image_width = self.background.width()
        image_height = self.background.height()

        if image_width != window_width or image_height != window_height:
            self.background = self.background.subsample(image_width // window_width, image_height // window_height)

        self.canvas.create_image(0, 0, image=self.background, anchor="nw")

    def build_sections(self):
        self.help_title = PhotoImage(file="assets/HELP_title.png")
        self.canvas.create_image(325, 120, image=self.help_title, anchor="nw")

        self.label_info_eagle = Label(self.canvas, text="Movimiento del águila")
        self.label_info_eagle.place(relx=0.2, rely=0.2, anchor="center")

        self.aguila_foto = PhotoImage(file="assets/ss_aguila.png")
        self.canvas.create_image(100, 150, image=self.aguila_foto, anchor="nw")

        self.tuto_eagle = Label(self.canvas, text="Usar flechas para mover águila")
        self.tuto_eagle.place(relx=0.2, rely=0.46, anchor="center")

        self.label_info_blocks = Label(self.canvas, text="Bloques")
        self.label_info_blocks.place(relx=0.2, rely=0.6, anchor="center")

        self.bloque_foto = PhotoImage(file="assets/ss_blocks.png")
        self.canvas.create_image(65, 390, image=self.bloque_foto, anchor="nw")

        self.tuto_blocks = Label(self.canvas, text="Para elegir tipo presionar 1, 2 y 3")
        self.tuto_blocks.place(relx=0.2, rely=0.87, anchor="center")

        self.tuto_blocks2 = Label(self.canvas, text="Para colocar usar mouse")
        self.tuto_blocks2.place(relx=0.2, rely=0.91, anchor="center")

        self.label_info_tank = Label(self.canvas, text="Movimiento del tanque")
        self.label_info_tank.place(relx=0.8, rely=0.2, anchor="center")

        self.tanque_foto = PhotoImage(file="assets/ss_tanque.png")
        self.canvas.create_image(580, 150, image=self.tanque_foto, anchor="nw")

        self.tuto_tank = Label(self.canvas, text="Usar WASD para mover tanque")
        self.tuto_tank.place(relx=0.8, rely=0.46, anchor="center")

        self.label_info_shoot = Label(self.canvas, text="Disparos")
        self.label_info_shoot.place(relx=0.8, rely=0.6, anchor="center")

        self.balas_foto = PhotoImage(file="assets/ss_bala.png")
        self.canvas.create_image(570, 390, image=self.balas_foto, anchor="nw")

        self.tuto_shoot = Label(self.canvas, text="Para disparar presione espacio")
        self.tuto_shoot.place(relx=0.8, rely=0.87, anchor="center")

    def build_buttons(self):
        self.button_back = Button(self.canvas, text="Back", command=self.back)
        self.button_back.place(relx=0.5, rely=0.8, anchor="center")

    def back(self):
        if self.master:
            self.master.destroy()