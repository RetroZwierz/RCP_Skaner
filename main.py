#!/usr/bin/env python
import tkinter
import tkinter.messagebox
import customtkinter
import time
from PIL import Image, ImageTk
import os
from scanner import Scanner
from scheduler import start_scheduled_jobs


customtkinter.set_appearance_mode("Ligh")
customtkinter.set_default_color_theme("blue")

PATH = os.path.dirname(os.path.realpath(__file__))

class App(customtkinter.CTk):
    INITIAL_LABEL_COLOR = ("gray25")
    INITIAL_WIDTH = 800
    INITIAL_HEIGHT = 50
    INITIAL_FONT = ("Arial", 22, "bold")
    TIME_FONT = ("Arial", 32, "bold")
    RESPONSE_WIDTH = 800
    RESPONSE_HEIGHT = 480
    RESPONSE_FONT = ("Arial", 38, "bold")

    APP_NAME = "GUI"

    def present_time(self):
        display_time = time.strftime("%H:%M:%S")
        self.label_3.config(text=display_time)
        self.label_3.after(1000, self.present_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.WIDTH = int(width)
        self.HEIGHT = int(height)
        self.scanner=Scanner()
        start_scheduled_jobs()

        self.title(App.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # load image with PIL and convert to PhotoImage
        image = Image.open(PATH + "/images/kjlogo.png").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.entry_1 = tkinter.Text()
        self.entry_1.place(relx=0.5, rely=0.5)
        self.entry_1.bind('<Return>',lambda event: self.input_callback())
        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label_text = tkinter.StringVar()
        self.label_text.set("Zeskanuj kod QR")
        self.label_1 = customtkinter.CTkLabel(width=App.INITIAL_WIDTH, height=App.INITIAL_HEIGHT,
                                              fg_color=App.INITIAL_LABEL_COLOR, textvariable=self.label_text)
        self.label_1.place(relx=0.5, rely=1.0, anchor=tkinter.S)
        self.label_1.config(text_color='#bec1c2')
        self.label_1.config(font=App.INITIAL_FONT)

        self.label_3 = customtkinter.CTkLabel(width=200, height=50, fg_color='white')
        self.label_3.place(relx=1.0, rely=0.0, anchor=tkinter.NE)
        self.label_3.config(text_color='black')
        self.label_3.config(font=App.TIME_FONT)

        self.present_time()

        self.entry_1.focus()

    def input_callback(self):
        code = self.entry_1.get("1.0","end")
        if not '\n' in code:
            self.entry_1.delete("1.0","end")
            return
            
        success, message, employee_id = self.scanner.scan(code)
        self.label_text_2 = tkinter.StringVar()
        self.label_text_2.set("")
        self.label_2 = customtkinter.CTkLabel(width=App.INITIAL_WIDTH, height=App.INITIAL_HEIGHT,
                                              fg_color=App.INITIAL_LABEL_COLOR, textvariable=self.label_text_2)
        self.label_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.label_2.config(width=App.RESPONSE_WIDTH, height=App.RESPONSE_HEIGHT)
        self.label_2.config(font=App.RESPONSE_FONT)
        self.label_2.config(text_color='white')
        if success:
            self.label_text_2.set(message + "\n ID: " + employee_id)
            if message == "Zarejestrowano czas wejścia.":
                self.label_2.config(fg_color='green')
                self.label_2.update()
            if message == "Zarejestrowano czas wyjścia.":
                self.label_2.config(fg_color='yellow')
                self.label_2.config(text_color='black')
                self.label_2.update()
        elif "Podwójny skan " in message:
                if "Wejście" in message:
                    self.label_text_2.set(message + "\n ID: " + employee_id)
                    self.label_2.config(fg_color='green')
                    self.label_2.update()
                elif "Wyjście" in message:
                    self.label_text_2.set(message + "\n ID: " + employee_id)
                    self.label_2.config(fg_color='yellow')
                    self.label_2.config(text_color='black')
                    self.label_2.update()
                else:
                    self.label_text_2.set(message + "\n ID: " + employee_id)
                    self.label_2.config(fg_color='gray')
                    self.label_2.config(text_color='black')
                    self.label_2.update()
        else:
            self.label_text_2.set(message)
            self.label_2.config(fg_color='red')
            self.label_2.update()

        self.label_2.after(5000, self.label_2.destroy)
        self.entry_1.delete("1.0","end")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.attributes('-fullscreen', True)
    app.start()
