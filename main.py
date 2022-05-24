#!/usr/bin/env python
import tkinter
import tkinter.messagebox
import customtkinter
import time
from PIL import Image, ImageTk
import os
from scanner import Scanner

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

PATH = os.path.dirname(os.path.realpath(__file__))

class App(customtkinter.CTk):
    INITIAL_LABEL_COLOR = ("gray70", "gray25")

    APP_NAME = "GUI"
    WIDTH = 900
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.WIDTH = int(width)
        self.HEIGHT = int(height)
        self.scanner=Scanner()
        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # load image with PIL and convert to PhotoImage
        image = Image.open(PATH + "/images/kjlogo.png").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.code = tkinter.StringVar()
        self.code.trace("w", lambda name, index, mode, sv=self.code: self.input_callback())
        self.entry_1 = tkinter.Entry(textvariable=self.code)
        self.entry_1.place(relx=0.5, rely=0.5)

        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label_text = tkinter.StringVar()
        self.label_text.set("Zeskanuj kod QR")
        self.label_1 = customtkinter.CTkLabel(width=200, height=100,
                                              fg_color=App.INITIAL_LABEL_COLOR, textvariable=self.label_text)
        self.label_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        self.entry_1.focus()

    def input_callback(self):
        code = self.code.get()
        length = len(code)
        if length != 128:
            if length > 128:
                self.code.set('')
            return
        if code == 'g':
            self.label_text.set('Zarejestrowano wejście')
            self.label_1.configure(fg_color='green')
            self.label_1.update()
        else:
            self.label_text.set('Brak dostępu')
            self.label_1.configure(fg_color='red')
            self.label_1.update()
        message = self.scanner.scan(code)
        if message != 'OK':
            self.label_text.set(message)
            self.label_1.configure(fg_color='red')
            self.label_1.update()
        else:
            self.label_text.set('Zarejestrowano wejście')
            self.label_1.configure(fg_color='green')
            self.label_1.update()

        print(code)
        time.sleep(1)
        self.code.set('')
        self.label_text.set('Zeskanuj kod QR')
        self.label_1.configure(fg_color=App.INITIAL_LABEL_COLOR)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.attributes('-fullscreen', True)
    app.start()