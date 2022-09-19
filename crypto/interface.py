from tkinter import *
import tkinter
from tkinter.ttk import *
import threading

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    payment = ""
    def pop_up_win(self):
        def get_input():
            global payment
            payment = inputtxt.get(1.0, END)

        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title = "Hacked!!"
    
        self.root.geometry("600x600")
        message ='This is a ransomware note!!!\n'
        message += "Enter your bitcoin payment below to get your files back!!"

        l = Label(self.root, text = message)
        l.config(font =("Courier", 14))
        l.pack()

        # TextBox Creation
        inputtxt = tkinter.Text(self.root, height = 5, width = 20)
        inputtxt.pack()

        button_frame = Frame(self.root)
        button_frame.pack()
        get_inp_b = Button(button_frame, text = "submit", command = get_input)
        get_inp_b.pack()


        self.root.mainloop()

