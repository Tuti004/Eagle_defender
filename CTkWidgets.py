import customtkinter

class song_list(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command1=None, command2=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.command1 = command1  # First button command
        self.command2 = command2  # Second button command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button1_list = []  # List for first set of buttons
        self.button2_list = []  # List for second set of buttons

    def add_item(self, item, image=None):
        
        label = customtkinter.CTkLabel(self, text=item, image=image, width=100, compound="left", padx=5, anchor="w")
        button1 = customtkinter.CTkButton(self, text="<", width=100, height=24,)
        button2 = customtkinter.CTkButton(self, text="X", width=100, height=24)
        
        if self.command1 is not None:
            button1.configure(command=lambda i=item: self.command1(i))
        if self.command2 is not None:
            button2.configure(command=lambda i=item: self.command2(i))

        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button1.grid(row=len(self.button1_list), column=1, pady=(0, 10), padx=5)
        button2.grid(row=len(self.button2_list), column=2, pady=(0, 10), padx=5)

        self.label_list.append(label)
        self.button1_list.append(button1)
        self.button2_list.append(button2)

    def remove_item(self, item):
        for idx, (label, button1, button2) in enumerate(zip(self.label_list, self.button1_list, self.button2_list)):
            if item == label.cget("text"):
                label.destroy()
                button1.destroy()
                button2.destroy()
                self.label_list.pop(idx)
                self.button1_list.pop(idx)
                self.button2_list.pop(idx)
                return