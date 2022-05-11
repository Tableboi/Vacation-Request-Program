import pandas as pd
import pyodbc
from datetime import datetime, timedelta

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)


#GUI practice
import tkinter
from tkinter import *
from typing import *

#login GUI
top = tkinter.Tk()
top.title("Vacation Request")

L1 = Label(top, text = "nEmployee:")
L1.grid(column = 0, row = 0)

def login():
    nEmployee = E1.get()
    print(nEmployee)

E1 = Entry(top)
E1.grid(column =1 , row = 0)
S1 = Button(top, text = "Submit", command = login)
S1.grid(column = 1, row = 1)
top.mainloop()

#request fetch GUI
top = tkinter.Tk()
top.title("Request View")
L1 = Label(top, text = "Request Number:")
L1.grid(column = 0, row = 0)

def fetch():
    cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
                   f"WHERE [nRequest] = {E1.get()}")
    print(cursor.fetchone())
    request = cursor.fetchone()
    nEmployee = request[4]
    dDateStart = datetime(request[1])
    dDateEnd = datetime(request[3])

E2 = Entry(top)
E2.grid(column = 1, row = 0)
B1 = Button(top, text = "fetch data", command = fetch)
B1.grid(column = 1, row = 1)

#GUI approval for requests
top = tkinter.Tk()
top.title("Request Approval")
L2 = Label(top, text = "Request Number:")
L2.grid(column = 0, row = 0)
E3 = Entry(top)
E3.grid(coloumn = 1, row = 0)
L3 = Label(top, text = "Approval:")
L3.grid(column = 0, row = 1)
E4 = Entry(top)
E4.grid(column = 1, row = 1)

def approve():
    cursor.execute("UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"SET [sStatus] = {E4.get()}"
               f"WHERE [nRequest] = {E3.get()}")
    cnxn.commit()

