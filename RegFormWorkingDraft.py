from tkinter import *
import pyodbc 
import pandas as pd  
from datetime import datetime, timedelta
 
class Window():
    def __init__(self, master):
        self.master = master
        master.title("Core Solution Urlaubsantrag")
 
        self.Main = Frame(self.master)
        
        self.label = Label(master, text = "Core Solution Urlaubsantrag", fg = "white", font = "Georgia 20 bold", bg = "navy blue")
        self.label.pack()
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

        
         
        self.section1.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 1
 

        # ----- Section 2
 
        self.section2 = Frame(self.Main)
 
        self.L3 = Label(self.section2, text = "Abteilung")
        self.L3.pack(padx = 5, pady = 5, side = LEFT)

        self.E3 = Entry(self.section2)
        self.E3.pack(padx = 5, pady = 5, side = LEFT)
        
        
        
        self.L4 = Label(self.section2, text = "Personal-Nr:")
        self.L4.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- nEmployee
       
        self.E4 = Entry(self.section2)
        self.E4.pack(padx = 5, pady = 5, side = LEFT)
        
       
        ## ---- nEmployee

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 2

        # ----- Section 3

        self.section3 = Frame(self.Main)      
        
        self.L5 = Label(self.section3, text = "Stellvertreter:")
        self.L5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E5 = Entry(self.section3)
        self.E5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L6 = Label(self.section3, text = "Resturlaub:")
        self.L6.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E6 = Entry(self.section3)
        self.E6.pack(padx = 5, pady = 5, side = LEFT)
 
        self.section3.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 3
 
        # ----- Section 4

        self.section4 = Frame(self.Main)
        
        ## ---- dDateStart

        
        self.Rvar1 = IntVar()
        
                
        self.L7 = Radiobutton(self.section4, text = "Urlaub am", variable = self.Rvar1, value = 1)
        self.L7.pack(padx = 5, pady = 5, side = LEFT)

        self.E7 = Entry(self.section4)
        self.E7.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L8 = Radiobutton(self.section4, text = "Urlaub vom", variable = self.Rvar1, value = 2)
        self.L8.pack(padx = 5, pady = 5, side = LEFT)

        self.E8 = Entry(self.section4)
        self.E8.pack(padx = 5, pady = 5, side = LEFT)


        ## ---- dDateStart
 
        self.section4.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 4

        # ----- Section 5

        self.section5 = Frame(self.Main)

        self.L9 = Label(self.section5, text = "bis einschl.")
        self.L9.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- dDateEnd
        
        self.E9 = Entry(self.section5)
        self.E9.pack(padx = 5, pady = 5, side = LEFT)
   
            
        ## ---- dDateEnd
        
        self.L10 = Label(self.section5, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L10.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E11 = Entry(self.section5, width = 6)
        self.E11.pack(padx = 5, pady = 5, side = LEFT)
         

        self.section5.pack(padx = 5, pady = 5, expand = True, fill = X)
        # ----- Section 5
    
        # ----- Section 6

        self.section6 = Frame(self.Main)
        
        ## ---- Section 6 sub-frame 1
         
        self.section6_1 = Frame(self.section6)        
 
        self.L11 = Label(self.section6_1, text = "Urlaubsgrund:")
        self.L11.pack(padx = 5, pady = 5)
        
        self.Rvar2= IntVar()
    
        self.R1 = Radiobutton(self.section6_1, text = "Erholungsurlaub", variable = self.Rvar2, value = 1)
        self.R2 = Radiobutton(self.section6_1, text = "Sonderurlaub aufgrund von", variable = self.Rvar2, value = 2)

        if (self.Rvar2.get() == 1):
            self.T1 = "Erholungsurlaub"
        
        self.R1.pack(padx = 5, pady = 5)
        self.R2.pack(padx = 5, pady = 5)
        

        self.T1 = Text(self.section6_1, height = 2, width = 8)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = X)
        

        self.section6_1.pack(padx = 50, pady = 5, side = LEFT)
 
        ## ---- Section 6 sub-frame 1
 
 
        ## ---- Section 6 sub-frame 2
         
        self.section6_2 = Frame(self.section6)        
 
        self.L12 = Label(self.section6_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
 
        ## ---- sReason
              
        self.Rvar3 = IntVar()
        
        ## ---- sReason

        self.R3 = Radiobutton(self.section6_2, text = "Ja", variable = self.Rvar3, value = 5)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = Radiobutton(self.section6_2, text = "Nein", variable = self.Rvar3, value = 6)
        self.R4.pack(padx = 5, pady = 5)
      
 
        self.section6_2.pack(padx = 50, pady = 5, side = RIGHT)
         
        ## ---- Section 6 sub-frame 2
         
 
        self.section6.pack(padx = 5, pady = 5, expand = True, fill = X)
        
        # ----- Section 6
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
        sql = """INSERT INTO dbo.PC_RequestTable (nRequest, dDateStart, dDateEnd, nEmployee, sReason, sStatus)
                    VALUES (?, ?, ?, ?, ?, ?)"""
        values = (1, self.E8.get(), self.E9.get(), self.E4.get(), self.T1.get("1.0", "end"), "anhängig")
 
        self.cursor.execute(sql, values)
        self.cnxn.commit() 

root = Tk()
root.resizable(False, False)
window = Window(root)
root.mainloop()