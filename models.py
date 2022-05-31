#The Model consists of pure application logic, which interacts with
# the database. It includes all the informaiton to represent data to
# the user.
#The stored procedures are all the required queries for SQL, formatted to
# match the controller

import pyodbc
from typing import Container
import pandas as pd
from datetime import datetime, timedelta

cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=SOPCP01DE;"
            "Database=PulseCoreTest5;"
            "UID=PCDev2;"
            "PWD=PCCSDev2PC5_!;")

cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor()

#create entry into vacation requests table
entry_creator = """INSERT INTO [PulseCoreTest5].[dbo].[PC_VacationsRequests] (dDateStart, dDateEnd, nEmployee, sReasons)
                        VALUES (?, ?, ?, ?)"""

#fetch employee info from login
infofetcher = """SELECT TOP [sFirstName]
                            ,[sName]
                            ,[nEmployee]
                            ,[bStatus]
                            ,[nProduktionsGruppe]
                            FROM [PulseCoreTest5].[dbo].[PO_employee]
                            WHERE [nEmployee] = ?"""

#fetch all vacation requests
allfetcher = """SELECT TOP (100) [xnRequest],
        [dDateStart],
        [dDateEnd],
        [nEmployee],
        [sReason],
        [sStatus],
        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""

#fetch a request by its request number
request_fetcher = """SELECT * FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                    WHERE [xnRequest] = ?"""

#retrieve the production group of a requesting operator
pg_checker = """SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]"
                   f"WHERE [nEmployee] = ?"""

#find a replacement operator from the same production groupd that is in
# town during the requested time off
pg_replacer = """SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]
                       WHERE [nProduktionsgruppe] = ? AND NOT IN
                       (SELECT [nEmployee] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                       WHERE [dDateStart] >= ? AND [dDateStart] <= ?)"""

#edit the vacation request table and add a string in the approval column
approver = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
               SET [sStatus] = ?
               WHERE [nRequest] = ?"""

#update an existing request
request_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                           SET [dDateStart] = ?,
                           [dDateEnd] = ?,
                           [sReason] = ?,
                           WHERE [nRequest] = ?"""

#delete a request in the vacations requests table
request_deleter = """DELETE FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                     WHERE [nRequest] = ?"""


#FROM VIEWS
#for the request_window
new_info = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus)
            VALUES (?, ?, ?, ?, ?)"""