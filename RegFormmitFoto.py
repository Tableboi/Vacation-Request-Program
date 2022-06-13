from datetime import datetime, timedelta
from tkinter import *

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
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((150,150))
        self.new_img = ImageTk.PhotoImage(self.img)
# Create a Label Widget to display the text or Image
        self.label = Label(root, image = self.new_img)
        self.label.pack()
        self.Main = Frame(self.master)

        
        # ----- Section 1
 
        self.section1 = Frame(self.Main)
 
        self.L1 = Label(self.section1, text = "Name")
        self.L1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E1 = Entry(self.section1)
        self.E1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L2 = Label(self.section1, text = "Vorname")
        self.L2.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E2 = Entry(self.section1)
        self.E2.pack(padx = 5, pady = 5, side = LEFT)

        self.L3 = Label(self.section1, text = "Abteilung")
        self.L3.pack(padx = 5, pady = 5, side = LEFT)

        self.E3 = Entry(self.section1)
        self.E3.pack(padx = 5, pady = 5, side = LEFT)
        
         
        self.section1.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 1
 

        # ----- Section 2
 
        self.section2 = Frame(self.Main)
        
        self.L4 = Label(self.section2, text = "Personal-Nr:")
        self.L4.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- nEmployee
       
        self.nEmployee = Entry(self.section2)
        self.nEmployee.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- nEmployee

        self.L5 = Label(self.section2, text = "Stellvertreter:")
        self.L5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E5 = Entry(self.section2)
        self.E5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L6 = Label(self.section2, text = "Resturlaub:")
        self.L6.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E6 = Entry(self.section2)
        self.E6.pack(padx = 5, pady = 5, side = LEFT)
        ## ---- nEmployee

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 2


        # ----- Section 3
        
        self.section3 = Frame(self.Main)
    
        self.L7 = Label(self.section3, text = "Urlaub am/vom")
        self.L7.pack(padx = 5, pady = 5, side = LEFT)

        ## ---- dDateStart

        self.dDateStart = Entry(self.section3)
        self.dDateStart.pack(padx = 5, pady = 5, side = LEFT)

        ## ---- dDateStart

        self.L8 = Label(self.section3, text = "bis einschl.")
        self.L8.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- dDateEnd
        
        self.dDateEnd = Entry(self.section3)
        self.dDateEnd.pack(padx = 5, pady = 5, side = LEFT)
               
    
        ## ---- dDateEnd
        
        self.L9 = Label(self.section3, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L9.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E9 = Entry(self.section3, width = 6)
        self.E9.pack(padx = 5, pady = 5, side = LEFT)
         
        self.section3.pack(padx = 5, pady = 5, expand = True, fill = X)
       
        # ----- Section 3
    
       
        # ------ Section 4

        self.section4 = Frame(self.Main)
        
        ## ---- Section 4 sub-frame 1

        self.section4_1 = Frame(self.section4)        
 
        self.L10 = Label(self.section4_1, text = "Urlaubsgrund:")
        self.L10.pack(padx = 5, pady = 5)

        self.T1 = Text(self.section4_1, height = 2, width = 20)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = X)

        self.section4_1.pack(padx = 50, pady = 5, side = LEFT)
 
        ## ---- Section 4 sub-frame 1
 
 
        ## ---- Section 4 sub-frame 2
         
        self.section4_2 = Frame(self.section4)        
 
        self.L12 = Label(self.section4_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
              
        self.Rvar2 = IntVar()

        self.R3 = Radiobutton(self.section4_2, text = "Ja", variable = self.Rvar2, value = 3)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = Radiobutton(self.section4_2, text = "Nein", variable = self.Rvar2, value = 4)
        self.R4.pack(padx = 5, pady = 5)
      
        self.section4_2.pack(padx = 50, pady = 5, side = RIGHT)
         
        ## ---- Section 4 sub-frame 2
         
        self.section4.pack(padx = 5, pady = 5, expand = True, fill = X)
        
        # ----- Section 4


        self.B0 = Button(self.Main, text = "Connect", command = self.connect)
        self.B0.pack(padx = 5, pady = 5, side = LEFT)
        
        self.B1 = Button(self.Main, text = "Submit", command = self.submit)
        self.B1.pack(padx = 5, pady = 5, side = RIGHT)
 
        self.Main.pack(padx = 5, pady = 5, expand = True, fill = X)
 
    def connect(self):
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

    def submit(self):
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            sql = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus)
                    VALUES (?, ?, ?, ?, ?)"""
            values = (start_date, end_date, self.nEmployee.get(), self.T1.get("1.0", "end"), "anhängig")
        
            self.cursor.execute(sql, values)
            self.cnxn.commit() 
            self.cnxn.close()
        
root = Tk()
root.resizable(False, False)
window = Window(root)
root.mainloop()