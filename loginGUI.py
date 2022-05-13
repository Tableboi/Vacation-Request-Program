from tkinter import *
from tkinter import ttk

root = Tk()
class loginbox():
    def __init__(self, master):
        master.title("Core Solution Urlaubsantrag Einloggen")
        self.Main = Frame(master)
        self.Main.pack(side = TOP, pady = 10)
        self.Info = Frame(master)
        self.Info.pack(pady = 10)

        self.label = Label(self.Main, text = "Core Solution Einloggen")
        self.label.pack()
        
        self.L1 = Label(self.Info, text = "Personal Nummer:")
        self.L1.pack(side = TOP)
        E1 = Entry(self.Info)
        E1.pack(side = LEFT)

        self.B1 = Button(self.Info, text = "Submit")
        self.B1.pack(side = RIGHT)
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


window = loginbox(root)
root.mainloop()