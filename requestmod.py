#the purpose of this module is to take input from employees and input them into the requests table
#
#inputs:
#dDateStart, dDateEnd, nEmployee, sReason, sStatus
#
#use sql INSERT INTO or UPDATE functions

#imports for sql stuff
import pyodbc
import pandas as pd
from datetime import datetime, timedelta

#imports for sending confirmation emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

#connect to sql server
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

#to insert a new row of info
sql_insert_query = ("""INSERT INTO [PulseCoreTest5].[dbo].[PC_RequestTable]
               VALUES %s, %s, %s, %s""")
#tuple retrieved from the GUI input
requestinfo = <dDateStart>, <dDateEnd>, <nEmployee>, <sReason>
cursor.execute(sql_insert_query, requestinfo)
cnxn.commit()
print("Urlaubsantrag in Bearbeitung")

#to update a request
sql_update_query = """UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]
                   SET [dDateStart]= %s, [dDateEnd]= %s, [sReason]= %s
                   WHERE [nEmployee]= %s"""
#tuple retrieved from the GUI inut
requestupdate = <dDateStart>, <dDateEnd>, <sReason>, <nEmployee>
cursor.execute(sql_update_query)
cnxn.commit()
print("Urlaubsantrag aktualisiert")

#set request inputs as variables, requires nEmployee from login 
cursor.execute("""SELECT [PulseCoreTest5].[dbo].[PC_RequestTable]
               [dDateStart], [dDateEnd], [sReason]
               WHERE [nEmployee] = {nEmployee};""")
request = cursor.fetchone()
nEmployee = request[3]
dDateStart = datetime(request[1])
dDateEnd = datetime(request[2])
sReason = request[4]


#now to have a confirmation email sent
date = datetime.today()
date = date.strftime("%Y-%m-%d")

txt = (f"Urlaubsantrag in Bearbeitung"
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