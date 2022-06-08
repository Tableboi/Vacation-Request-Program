from tkinter import *
from tkcalendar import *

root = Tk()

mycal = Calendar(root, setmode = "day", date_pattern = 'd/m/yy')
mycal.pack(padx = 15, pady = 15)

root.geometry("300x300")
root.title("Urlaubskalendar")
root.configure(bg = "lightblue")



root.mainloop()