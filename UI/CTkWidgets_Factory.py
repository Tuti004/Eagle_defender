import customtkinter

class SongList:
    def __init__(self, master, command1=None, command2=None, widget_factory=None, **kwargs):
        self.master = master
        self.command1 = command1
        self.command2 = command2
        self.widget_factory = widget_factory or DefaultWidgetFactory()
        self.items = []

    def add_item(self, item, image=None):
        label = self.widget_factory.create_label(self.master, item, image)
        button1 = self.widget_factory.create_button(self.master, "<", lambda i=item: self.command1(i))
        button2 = self.widget_factory.create_button(self.master, "X", lambda i=item: self.command2(i))

        label.grid(row=len(self.items), column=0, pady=(0, 10), sticky="w")
        button1.grid(row=len(self.items), column=1, pady=(0, 10), padx=5)
        button2.grid(row=len(self.items), column=2, pady=(0, 10), padx=5)

        self.items.append((label, button1, button2))

    def remove_item(self, item):
        for idx, (label, button1, button2) in enumerate(self.items):
            if item == label.cget("text"):
                label.destroy()
                button1.destroy()
                button2.destroy()
                self.items.pop(idx)
                return

class WidgetFactory:
    def create_label(self, master, text, image):
        raise NotImplementedError

    def create_button(self, master, text, command):
        raise NotImplementedError

class DefaultWidgetFactory(WidgetFactory):
    def create_label(self, master, text, image):
        return customtkinter.CTkLabel(master, text=text, image=image, width=80, compound="left", padx=5, anchor="w")

    def create_button(self, master, text, command):
        return customtkinter.CTkButton(master, text=text, width=50, height=24, command=command)
