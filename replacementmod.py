#the purpose of this module is to fetch other operators that are part of the 
#same produktionsgruppe that do not have a vacation request for the dates
#
#inputs:
#dDateStart, dDateEnd, nEmployee, nProduktionsgruppe
#
#imports for sql stuff
import pyodbc
import pandas as pd
from datetime import datetime, timedelta

#connect to sql server
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
           "Server=<server_id>;"
           "Database=<database_id>;"
           "UID=<user_id>;"
           "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

#fetching a request after seeing all of them
current_request = input("nRequest:") #can be handled by GUI
cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"WHERE [nRequest] = {current_request};")
request = cursor.fetchone()
nEmployee = request[4]
dDateStart = datetime(request[1])
dDateEnd = datetime(request[3])

#find the produktionsgruppe of missing operator
cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]"
               f"WHERE [nEmployee] = {nEmployee}")
employee = cursor.fetchone()
produktionsgruppe = employee[4]

#now selecting all operators that are in the same produktionsgruppe and
#do not have a current vacation request at the same time
cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]"
               f"WHERE [nProduktionsgruppe] = {produktionsgruppe} AND NOT IN"
               f"(SELECT [nEmployee] FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"WHERE [dDateStart] >= {dDateStart} AND [dDateStart] <= {dDateEnd})")
replacements = cursor.fetchall()
print(replacements)