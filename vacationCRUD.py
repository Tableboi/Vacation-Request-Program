#this file contains the create, read, update, and delete functions of the application

from typing import Container
import pandas as pd
from pyodbc import *
from datetime import datetime, timedelta

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=SOPCP01DE;"
            "Database=PulseCoreTest5;"
            "UID=PCDev2;"
            "PWD=PCCSDev2PC5_!;")


#CONNECT
def connect(cnxn_str):
    try:
        cnxn = pyodbc.connect(cnxn_str)
        print('{c} is working'.format(c = cnxn_str))
        cnxn.close()
    except pyodbc.Error as ex:
        print("{c} is not working".format(c = cnxn_str))

#CREATE
def create_entry(cnxn_str, dDateStart, dDateEnd, nEmployee, sReasons):
    """Creates a new row in the requests table.
    Parameters
    ----------
    dDateStart : datetime
    dDateEnd : datetime
    nEmployee : int
    sReason : not sure what this is"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("INSERT INTO [PulseCoreTest5].[dbo].[PC_VacationsRequests] (dDateStart, dDateEnd, nEmployee, sReasons)"
                        f"VALUES ({dDateStart}, {dDateEnd}, {nEmployee}, {sReasons})")
        cnxn.commit()
    except pyodbc.Error:
        print('Error, entry not successful')

#READ
def infofetch(cnxn_str, nEmployee):
    """Fetches employee info when logging in.
    Parameters
    -----------
    nEmployee : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("SELECT TOP [sFirstName]"
                            ",[sName]"
                            ",[nEmployee]"
                            ",[bStatus]"
                            ",[nProduktionsGruppe]"
                            "FROM [PulseCoreTest5].[dbo].[PO_employee]"
                            f"WHERE [nEmployee] = {nEmployee}")
    except pyodbc.Error:
        print('Error, info fetch not successful')

def allfetch(cnxn_str):
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("""SELECT TOP (100) [xnRequest],
        [dDateStart],
        [dDateEnd],
        [nEmployee],
        [sReason],
        [sStatus],
        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]""")
    except pyodbc.Error:
        print('Error, request fetch unsuccessful')

def requestfetch(cnxn_str, xnRequest):
    """Fetches a specific request from the request table
    Parameters
    ----------
    nRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                   f"WHERE [nRequest] = {xnRequest};")

def pg_check(cnxn_str, nEmployee):
    """Retrieves the production group of a requesting operator
    Parameters
    ----------
    nEmployee : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]"
                   f"WHERE [nEmployee] = {nEmployee}")
    except pyodbc.Error:
        print('Error, produktionsgruppe not found')

def pg_find_replacement(cnxn_str, produktionsgruppe, dDateStart, dDateEnd):
    """Finds a replacement operator from the same production group
    that is in town during the requested time off.
    Parameters
    ----------
    Produktionsgruppe : int
    dDateStart : datetime
    dDateEnd : datetime"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PO_employee]"
                       f"WHERE [nProduktionsgruppe] = {produktionsgruppe} AND NOT IN"
                       f"(SELECT [nEmployee] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                       f"WHERE [dDateStart] >= {dDateStart} AND [dDateStart] <= {dDateEnd})")
    except pyodbc.Error:
        print('Error, replacement find unsuccessful')

#UPDATE
def approve(cnxn_str, approval, xnRequest):
    """Edits the request table and adds a string in the approval column.
    Parameters
    ----------
    approval : str
    nRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"SET [sStatus] = {approval}"
               f"WHERE [nRequest] = {xnRequest}")
        cnxn.commit()
    except pyodbc.Error:
        print('Error, request update unsuccessful')

def update_request(cnxn_str, xnRequest, dDateStart, dDateEnd, sReason):
    """Updates an existing request, calls the request by its number.
    Parameters
    ----------
    nRequest : int
    dDateStart : datetime
    dDateEnd : datetime
    sReason : str"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                           f"SET [dDateStart]= {dDateStart},"
                           f"[dDateEnd] = {dDateEnd},"
                           f"[sReason] = {sReason},"
                           f"WHERE [nRequest] = {xnRequest}")
        cnxn.commit()
    except pyodbc.Error:
        print('Error, request update unsucessful')

#DELETE
def request_delete(cnxn_str, xnRequest):
    """Deletes a request in the requests table
    Parameters
    ----------
    nRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute("DELETE FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
                       f"WHERE [nRequest] = {xnRequest}")
        cnxn.commit()
    except pyodbc.Error:
        print('Error, deletion not successful')
