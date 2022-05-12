from tkinter import *
import pandas as pd
import pyodbc

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor(prepared = True)

class loginbox():
    def __init__(self, master):
        self.master = master
        master.title("Core Solution Urlaubsantrag Einloggen")
        self.Main = Frame(self.master)
        self.Main.pack(padx = 10, pady = 10, expand = True, fill = X)
        
        self.label = Label(self.Main, text = "Core Solution Einloggen")
        self.label.pack()
        
        self.L1 = Label(self.Main, text = "Personal Nummer:")
        self.L1.pack(side = TOP)
        self.E1 = Entry(self.Main)
        self.E1.pack(side = LEFT)

        self.B1 = Button(self.Main, text = "Submit")
        self.B1.pack(side = RIGHT)
    def submit(self):
        cursor.execute ("SELECT TOP [sFirstName]"
                        ",[sName]"
                        ",[nEmployee]"
                        ",[bStatus]"
                        ",[nProduktionsGruppe]"
                        "FROM [PulseCoreTest5].[dbo].[PO_employee]"
                        f"WHERE [nEmployee] = {login}")
        employeeinfo = cursor.fetchone()
        nEmployee = float(employeeinfo[2])
        #insert if else statement that determines if user is a manager or operator




root = Tk()
root.resizable(False, False)
window = loginbox(root)
root.mainloop()