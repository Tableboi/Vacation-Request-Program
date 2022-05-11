#the purpose of this module is to identify if the user is a manager or operator
import pandas as pd
import pyodbc
from datetime import date, timedelta


login = input("xidEmployee") #may also be input by the GUI

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

cursor.execute("SELECT [xidEployee],"
    "FROM [PulseCoreTest5].[dbo].[PO_employee]"
    "WHERE sCompany=90 AND xnEmployee= %s ;", (login))
employee = cursor.fetchone()
employee_id = float(employee[0])

#displays all current request info from PC_RequestTable
if employee_id == #manager id :
    cursor.execute("""SELECT TOP (1000) [nRequest]
      ,[dDateStart]
      ,[dDateEnd]
      ,[nEmployee]
      ,[sReason]
      ,[sStatus]
      FROM [PulseCoreTest5].[dbo].[PC_RequestTable]""")
    print(cursor.fetchall())
elif:
    #prompt requestmod script

