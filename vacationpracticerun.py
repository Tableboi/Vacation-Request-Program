#imports for sql
import pandas as pd
import pyodbc
from datetime import datetime, timedelta

#imports for emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

login = input("nEmployee") #may also be input by the GUI

cursor.execute ("SELECT TOP [sFirstName]"
                ",[sName]"
                ",[nEmployee]"
                ",[bStatus]"
                ",[nProduktionsGruppe]"
                "FROM [PulseCoreTest5].[dbo].[PO_employee]"
                f"WHERE [nEmployee] = {login}")
employee = cursor.fetchone()
employee_id = float(employee[2])

cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]")
print(cursor.fetchall())

#displays all current request info from PC_RequestTable
if employee_id == #manager id :
    current_request = input("nRequest:") #can be handled by GUI
    cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
                   f"WHERE [nRequest] = {current_request};")
    print(cursor.fetchone())
    request = cursor.fetchone()
    nEmployee = request[4]
    dDateStart = datetime(request[1])
    dDateEnd = datetime(request[3])

    #finding the produktionsgruppe of requesting operator
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


    approval = input("Approval:") #can be handled by GUI
    cursor.execute("UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]"
               f"SET [sStatus] = {approval}"
               f"WHERE [nRequest] = {current_request}")
    cnxn.commit()

    if approval == "ja":
        anerkannt = "ist anerkannt"
    elif approval == "ja aber":
        anerkannt = "musst ändern"
    elif approval == "nein":
        anerkannt = "ist nicht anerkannt"
    else:
        print("error")
    
    #retrieves info for confirmation email
    date = datetime.today()
    date = date.strftime("%Y-%m-%d")
    approval = input("Approval?")
    nRequest = input("Request number?")
    cursor.execute("SELECT * FROM [PulseCoreTest5].[dbo].[PC_RequestTable]"
                   f"WHERE [nRequest] = {nRequest}")
    request = cursor.fetchall()
    nEmployee = request[3]
    dDateStart = datetime(request[1])
    dDateEnd = datetime(request[3])
    sReason = request[4]


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

else:
    funktion = input("Neuer Urlaubsantrag oder Aufbereiten?") #can be handled by GUI
    if funktion == "Neuer Urlaubsantrag":
        #creation of new request
        sql_insert_query = ("""INSERT INTO [PulseCoreTest5].[dbo].[PC_RequestTable]
                       VALUES %s, %s, %s, %s""")
        requestinfo = <dDateStart>, <dDateEnd>, <nEmployee>, <sReason> #from GUI
        cursor.execute(sql_insert_query, requestinfo)
        cnxn.commit()
        print("Urlaubsantrag in Bearbeitung")
    elif funktion == "Aufbereiten":
        #updating of a request
        sql_update_query = """UPDATE [PulseCoreTest5].[dbo].[PC_RequestTable]
                   SET [dDateStart]= %s, [dDateEnd]= %s, [sReason]= %s
                   WHERE [nEmployee]= %s"""
        requestupdate = <dDateStart>, <dDateEnd>, <sReason>, <nEmployee> #input from GUI
        cursor.execute(sql_update_query)
        cnxn.commit()
        print("Urlaubsantrag aktualisiert")
    else:
        print("Error")
    
    #calling info for the email
    cursor.execute("""SELECT [PulseCoreTest5].[dbo].[PC_RequestTable]
               [dDateStart], [dDateEnd], [sReason]
               WHERE [nEmployee] = {nEmployee};""")
    request = cursor.fetchone()
    nEmployee = request[3]
    dDateStart = datetime(request[1])
    dDateEnd = datetime(request[2])
    sReason = request[4]

    date = datetime.today()
    date = date.strftime("%Y-%m-%d")
    if funktion == "Neuer Urlaubsantrag" or "Aufhereiten":
        #for sending a confirmation email that their request is made or updated
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
    else:
        date = datetime.today()
        date = date.strftime("%Y-%m-%d")
        #for sending an email regarding an error
        txt = (f"Urlaubsantrag in nicht korrekterweise eingetreten"
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