from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox

import pandas as pd
import pyodbc
from PIL import Image, ImageTk


class Window():
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, width=600, height=400)
        self.frame.pack()
        self.frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.PNG'
        self.img = Image.open(self.path)
        self.img.thumbnail((150,150))
        self.new_img = ImageTk.PhotoImage(self.img)
# Create a Label Widget to display the text or Image
        self.label = Label(root, image = self.new_img)
        self.label.pack()
        self.Main = Frame(self.master)

        
        
        # ----- Section 1
 
        self.section1 = Frame(self.Main)
 

        self.L1 = Label(self.section1, text = "Personal-Nr")
        self.L1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.nEmployee = Entry(self.section1)
        self.nEmployee.pack(padx = 5, pady = 5, side = LEFT)
 

        self.L2 = Label(self.section1, text = "Urlaub am/vom")
        self.L2.pack(padx = 5, pady = 5, side = LEFT)
 
        self.dDateStart = Entry(self.section1)
        self.dDateStart.pack(padx = 5, pady = 5, side = LEFT)


        self.section1.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 1
 

        # ----- Section 2
 
        self.section2 = Frame(self.Main)
        

        self.L3 = Label(self.section2, text = "bis einschl.")
        self.L3.pack(padx = 5, pady = 5, side = LEFT)

        self.dDateEnd = Entry(self.section2)
        self.dDateEnd.pack(padx = 5, pady = 5, side = LEFT)
        

        self.L4 = Label(self.section2, text = "Stellvertreter")
        self.L4.pack(padx = 5, pady = 5, side = LEFT)
       
        self.E4 = Entry(self.section2)
        self.E4.pack(padx = 5, pady = 5, side = LEFT)
        

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 2


        # ----- Section 3
        
        self.section3 = Frame(self.Main)
    
        ## ---- Section 3 sub-frame 1
        
        self.section3_1 = Frame(self.section3)

        self.L5 = Label(self.section3_1, text = "Urlaubsgrund")
        self.L5.pack(padx = 5, pady = 5)

        self.Rvar1 = IntVar()

        self.R1 = Radiobutton(self.section3_1, text = "Erholungsurlaub", variable = self.Rvar1, value = 1)
        self.R2 = Radiobutton(self.section3_1, text = "Sonderurlaub", variable = self.Rvar1, value = 2)

        self.R1.pack(padx = 5, pady = 5)
        self.R2.pack(padx = 5, pady = 5)

        self.section3_1.pack(padx = 50, pady = 5, side = LEFT)
        
        ## ---- Section 3 sub-frame 1


        ## ---- Section 3 sub-frame 2
        self.section3_2 = Frame(self.section3)
        
        self.L6 = Label(self.section3_2, text = "Falls Sonderurlaub gewählt, Begründung angeben")
        self.L6.pack(padx = 5, pady = 5)

        self.T1 = Text(self.section3_2, height = 2, width = 20)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = X)


        self.section3_2.pack(padx = 50, pady = 5, side = RIGHT)

         ## ---- Section 3 sub-frame 2

        self.section3.pack(padx = 5, pady = 5, expand = True, fill = X)
       
        # ----- Section 3
        
        self.B0 = Button(self.Main, text = "Submit", command = lambda : [self.submit(), self.click_me()])
        self.B0.pack(padx = 5, pady = 5, side = RIGHT)
 
        self.Main.pack(padx = 5, pady = 5, expand = True, fill = X)
 

    def submit(self):
        try:
            self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                    "Server=SOPCP01DE;"
                                    "Database=PulseCoreTest5;"
                                    "UID=PCDev2;"
                                    "PWD=PCCSDev2PC5_!")
            self.cursor = self.cnxn.cursor()
            print("Connection Succeeded")
        except:
            print("Connection Failed")

        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
        
        
        erholungsurlaub = 'Erholungsurlaub'
        sonderurlaub = self.T1.get("1.0", "end")

        gründe = self.Rvar1.get()
        if gründe == 1:
            output = erholungsurlaub
        elif gründe == 2:
            output = sonderurlaub
        else:
            ...
        
        sql = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus, sStellvertreter)
                    VALUES (?, ?, ?, ?, ?, ?)"""
        values = (start_date, end_date, self.nEmployee.get(), output, "geplant", self.E4.get())
        
        self.cursor.execute(sql, values)
        self.cnxn.commit() 
        self.cnxn.close()
    

    def click_me(self):
        self.mssg = messagebox.showinfo("Success", "Your submission was recorded!")
    
        
root = Tk()
root.resizable(False, False)
window = Window(root)
root.mainloop()
