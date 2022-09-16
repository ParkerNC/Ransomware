from tkinter import *
import tkinter
from tkinter.ttk import *

def pop_up_win():
    # creates a Tk() object
    master = Tk()
    master.title = "Hacked!!"
    
    master.geometry("600x600")
    message ='This is a ransomware note!!!\n'
    message += "Enter your bitcoin payment below to get your files back!!"

    l = Label(master, text = message)
    l.config(font =("Courier", 14))
    l.pack()

    # TextBox Creation
    inputtxt = tkinter.Text(master, height = 5, width = 20)
    inputtxt.pack()

    master.mainloop()

