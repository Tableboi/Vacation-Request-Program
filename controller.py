#The controller acts as an intermediary between view and model.
#It listens to the events triggered by view and queries model
# for the same.
#The functions below are formatted by their CRUD, followed by the
# functions necessary for the email confirmations
import vacationproject.appfiles.models as models
import vacationproject.appfiles.views as views

from typing import Container
import pandas as pd
import pyodbc
from datetime import datetime, timedelta

#CONNECT
#test connection to sql NEEDS WORK
def connect(cnxn_str):
    try:
        cnxn = pyodbc.connect(cnxn_str)
        print('{c} is working'.format(c = cnxn_str))
        cnxn.close()
    except pyodbc.Error as ex:
        print("{c} is not working".format(c = cnxn_str))

#CREATE
#create entry into vacation requests table NEEDS WORK
new_info = (dDateStart, dDateEnd, nEmployee, sReasons)
def create_entry(cnxn_str, entry_creator, new_info):
    """Parameters
    ----------
    dDateStart : datetime
    dDateEnd : datetime
    nEmployee : int
    sReason : not sure what this is"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(entry_creator, new_info)
        cnxn.commit()
    except pyodbc.Error:
        print('Error, entry not successful')

#READ
#fetch employee info from login
login_info = (nEmployee)
def infofetch(cnxn_str, infofetcher, login_info):
    """Parameters
    -----------
    nEmployee : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(infofetcher, login_info)
    except pyodbc.Error:
        print('Error, info fetch not successful')

#fetch all vacation requests
def allfetch(cnxn_str, allfetcher):
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(allfetcher)
    except pyodbc.Error:
        print('Error, request fetch unsuccessful')

#fetch a request by its request number
spec_request = (xnRequest)
def requestfetch(cnxn_str, request_fetcher, spec_request):
    """Parameters
    ----------
    nRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    cursor.execute(request_fetcher, spec_request)

#retrieves the production group of a requesting operator
pg_tbchecked = (nEmployee)
def pg_check(cnxn_str, pg_checker, pg_tbchecked):
    """Parameters
    ----------
    nEmployee : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(pg_checker, pg_tbchecked)
    except pyodbc.Error:
        print('Error, produktionsgruppe not found')

#find a replacement operator from the same production group that is in
# town during the requested time off
pg_repinfo = (produktionsgruppe, dDateStart, dDateEnd)
def pg_find_replacement(cnxn_str, pg_replacer, pg_repinfo):
    """Parameters
    ----------
    Produktionsgruppe : int
    dDateStart : datetime
    dDateEnd : datetime"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(pg_replacer, pg_repinfo)
    except pyodbc.Error:
        print('Error, replacement find unsuccessful')

#UPDATE
#edit the vacation request table and adds a string in the approval column
approve_info = (sStatus, xnRequest)
def approve(cnxn_str, approver, approve_info):
    """Parameters
    ----------
    approval : str
    xnRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(approver, approve_info)
        cnxn.commit()
    except pyodbc.Error:
        print('Error, request update unsuccessful')

#update an existing request
request_info = (dDateStart, dDateEnd, sReason, xnRequest)
def update_request(cnxn_str, request_updater, request_info):
    """Parameters
    ----------
    nRequest : int
    dDateStart : datetime
    dDateEnd : datetime
    sReason : str"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(request_updater, request_info)
        cnxn.commit()
    except pyodbc.Error:
        print('Error, request update unsucessful')

#DELETE
#delete a request in the vacations requests table
def request_delete(cnxn_str, request_deleter):
    """Parameters
    ----------
    nRequest : int"""
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    try:
        cursor.execute(request_deleter)
        cnxn.commit()
    except pyodbc.Error:
        print('Error, deletion not successful')

#EMAIL
#fetch info for the confirmation email
def email_info(cnxn_str, xnRequest, sStatus):

    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor(prepared = True)
    cursor.execute(models.request_fetcher, models.spec_request)
    request = cursor.fetchall()
    nEmployee = request[3]
    dDateStart = datetime(request[1])
    dDateEnd = datetime(request[3])
    sReasons = request[4]

    txt = (f"Urlaubsantrag {anerkannt}"
           f"Urlaub am/vom: {dDateStart}"
           f"bis: {dDateEnd}"
           f"Grund: {sReasons}"
           f"Tag des Antrags: {date}")
    
    msg = MIMEMultipart()  
    msg["Subject"] = "Automatischer Urlaubsantrag Bestätigung"
    msg.attach(MIMEText(txt))

    smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')
    smtp.ehlo() #say hello to server
    smtp.starttls() #communicate using TLS encryption
    smtp.login('<sending email>', '<password>') #login to email
    smtp.sendmail('<sending email>', '<receiving email>', msg.as_string()) #send email
    smtp.quit #disconnect from mail server