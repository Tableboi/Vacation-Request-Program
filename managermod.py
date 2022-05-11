#the purpose of this module is to allow the manager to view and edit requests
#imports for sql stuff
import pandas as pd
import pyodbc
from datetime import datetime, timedelta

#imports for emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

login = input("xidEmployee") #may also be input by the GUI

#connect to the sql server
cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

#view current requests
cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]")
print(cursor.fetchall())

#update a request (approve or disapprove)
approval = input("Approval?")
nRequest = input("Request number?")
cursor.execute("UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"SET [sStatus] = {approval}"
               f"WHERE [nRequest] = {nRequest}")
cnxn.commit()

#email for approval status
date = datetime.today()
date = date.strftime("%Y-%m-%d")
approval = input("Approval?")
nRequest = input("Request number?")
cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"WHERE [nRequest] = {nRequest}")
request = cursor.fetchall()
nEmployee = request[3]
dDateStart = datetime(request[1])
dDateEnd = datetime(request[2])
sReason = request[4]

#determining approval based off of manager response
if approval == "ja":
    anerkannt = "ist anerkannt"
elif approval == "ja aber":
    anerkannt = "musst ändern"
else:
    anerkannt = "ist nicht anerkannt"

#populating the email with the info from the confirmed request
date = datetime.today()
date = date.strftime("%Y-%m-%d")
txt = (f"Urlaubsantrag {anerkannt}"
       f"Urlaub vom: {dDateStart}"
       f"bis: {dDateEnd}"
       f"Grund: {sReason}"
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

#delete the old request after it has been confirmed or rejected
cursor.execute("DELETE * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"WHERE [nRequest] = {nRequest}")
cnxn.commit()