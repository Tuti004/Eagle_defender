import customtkinter

class main_Screen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.button_play = customtkinter.CTkButton(self, text="Jugar", command=None, fg_color="transparent")
        self.button_play.place(relx=0.5, rely=0.6, anchor="center")

if __name__ == "__main__":
    app = main_Screen()
    app.title("Eagle Defender")
    app.minsize(800, 600)
    app.mainloop()