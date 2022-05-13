#imports for sql
import pandas as pd
import pyodbc
from datetime import datetime, timedelta

#imports for emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

#imports for GUI
from tkinter import *

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=<server_id>;"
            "Database=<database_id>;"
            "UID=<user_id>;"
            "PWD=<password>;")
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor(prepared=True)

#GUI for login
global root
root = Tk()
class loginbox():
    def __init__(self, master):
        self.master = master
        master.title("Core Solution Urlaubsantrag Einloggen")
        self.Main = Frame(self.master)
        self.Main.pack(side = TOP, padx = 10, pady = 10)
        self.Info = Frame(master)
        self.Info.pack(pady = 10)

        self.label = Label(self.Main, text = "Core Solution Einloggen")
        self.label.pack()
        
        self.L1 = Label(self.Info, text = "Personal Nummer:")
        self.L1.pack(side = TOP)
        self.E1 = Entry(self.Info)
        self.E1.pack(side = LEFT)
        global nEmployee
        nEmployee = self.E1.get()

        self.B1 = Button(self.Info, text = "Submit")
        self.B1.pack(side = RIGHT)

        window_width = 300
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    def submit(self):
        cursor.execute ("SELECT TOP [sFirstName]"
                        ",[sName]"
                        ",[nEmployee]"
                        ",[bStatus]"
                        ",[nProduktionsGruppe]"
                        "FROM [PulseCoreTest5].[dbo].[PO_employee]"
                        f"WHERE [nEmployee] = {nEmployee}")
        employeeinfo = cursor.fetchone()
        nEmployee = float(employeeinfo[2])
window = loginbox(root)
root.mainloop()

#GUI for employee submission
class Window():
    def __init__(self, master):
        self.master = master
        master.title("Core Solution Urlaubsantrag")
 
        self.Main = Frame(self.master)
        
        self.label = Label(master, text = "Core Solution Urlaubsantrag", fg = "white", font = "Georgia 20 bold", bg = "navy blue")
        self.label.pack()
        # ----- Section 1
 
        self.section1 = Frame(self.Main)
 
        self.L1 = Label(self.section1, text = "Name")
        self.L1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E1 = Entry(self.section1)
        self.E1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L2 = Label(self.section1, text = "Vorname")
        self.L2.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E2 = Entry(self.section1)
        self.E2.pack(padx = 5, pady = 5, side = LEFT)

        self.section1.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 1
 

        # ----- Section 2
 
        self.section2 = Frame(self.Main)
 
        self.L3 = Label(self.section2, text = "Abteilung")
        self.L3.pack(padx = 5, pady = 5, side = LEFT)

        self.E3 = Entry(self.section2)
        self.E3.pack(padx = 5, pady = 5, side = LEFT)
        
        self.L4 = Label(self.section2, text = "Personal-Nr:")
        self.L4.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- nEmployee
       
        self.E4 = Entry(self.section2)
        self.E4.pack(padx = 5, pady = 5, side = LEFT)
        global nEmployee
        nEmployee = self.E4.get()
       
        ## ---- nEmployee

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 2

        # ----- Section 3

        self.section3 = Frame(self.Main)      
        
        self.L5 = Label(self.section3, text = "Stellvertreter:")
        self.L5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E5 = Entry(self.section3)
        self.E5.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L6 = Label(self.section3, text = "Resturlaub:")
        self.L6.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E6 = Entry(self.section3)
        self.E6.pack(padx = 5, pady = 5, side = LEFT)
 
        self.section3.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 3
 
        # ----- Section 4

        self.section4 = Frame(self.Main)
        
        ## ---- dDateStart

        self.Cvar1 = IntVar()
        self.Cvar2 = IntVar()
                
        self.L7 = Checkbutton(self.section4, text = "Urlaub am", variable = self.Cvar1)
        self.L7.pack(padx = 5, pady = 5, side = LEFT,)

        self.E7 = Entry(self.section4)
        self.E7.pack(padx = 5, pady = 5, side = LEFT)
 
        self.L8 = Checkbutton(self.section4, text = "Urlaub vom", variable = self.Cvar2)
        self.L8.pack(padx = 5, pady = 5, side = LEFT)

        self.E8 = Entry(self.section4)
        self.E8.pack(padx = 5, pady = 5, side = LEFT)

        def isChecked():
            global dDateStart
            global dDateEnd
            if self.L7.variable == self.Cvar1:
                dDateStart = self.E7
                dDateEnd = dDateStart 
            elif self.L8.variable == self.Cvar2:
                dDateStart, dDateEnd = self.E8, self.E9
            else:
                pass
        ## ---- dDateStart
 
        self.section4.pack(padx = 5, pady = 5, expand = True, fill = X)
 
        # ----- Section 4

        # ----- Section 5

        self.section5 = Frame(self.Main)

        self.L9 = Label(self.section5, text = "bis einschl.")
        self.L9.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- dDateEnd
        
        self.E9 = Entry(self.section5)
        self.E9.pack(padx = 5, pady = 5, side = LEFT)
        
        ## ---- dDateEnd
        
        self.L10 = Label(self.section5, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L10.pack(padx = 5, pady = 5, side = LEFT)
 
        self.E11 = Entry(self.section5, width = 6)
        self.E11.pack(padx = 5, pady = 5, side = LEFT)
        
        self.section5.pack(padx = 5, pady = 5, expand = True, fill = X)
        # ----- Section 5
    
        # ----- Section 6

        self.section6 = Frame(self.Main)
        
        ## ---- Section 6 sub-frame 1
         
        self.section6_1 = Frame(self.section6)        
 
        self.L11 = Label(self.section6_1, text = "Urlaubsgrund:")
        self.L11.pack(padx = 5, pady = 5)
        
        self.Rvar1= IntVar()
 
        self.R1 = Radiobutton(self.section6_1, text = "Erholungsurlaub", variable = self.Rvar1, value = 1)
        self.R1.pack(padx = 5, pady = 5)
        self.R2 = Radiobutton(self.section6_1, text = "Sonderurlaub aufgrund von", variable = self.Rvar1, value = 2)
        self.R2.pack(padx = 5, pady = 5)
        
        self.T1 = Text(self.section6_1, height = 2, width = 8)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = X)

        self.section6_1.pack(padx = 50, pady = 5, side = LEFT)
 
        ## ---- Section 6 sub-frame 1
 
        ## ---- Section 6 sub-frame 2
         
        self.section6_2 = Frame(self.section6)        
 
        self.L12 = Label(self.section6_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
 
        ## ---- sReason
              
        self.Rvar2 = IntVar()
        
        ## ---- sReason

        self.R3 = Radiobutton(self.section6_2, text = "Ja", variable = self.Rvar2, value = 1)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = Radiobutton(self.section6_2, text = "Nein", variable = self.Rvar2, value = 2)
        self.R4.pack(padx = 5, pady = 5)
 
        self.section6_2.pack(padx = 50, pady = 5, side = RIGHT)
         
        ## ---- Section 6 sub-frame 2
         
        self.section6.pack(padx = 5, pady = 5, expand = True, fill = X)
        
        # ----- Section 6
        self.B0 = Button(self.Main, text = "Connect", command = self.connect)
        self.B0.pack(padx = 5, pady = 5, side = LEFT)
 
        
        self.B1 = Button(self.Main, text = "Submit", command = self.submit)
        self.B1.pack(padx = 5, pady = 5, side = RIGHT)
 
        self.Main.pack(padx = 5, pady = 5, expand = True, fill = X)
 
    def connect(self):
        try:
            self.conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                    "Server=SOPCP01DE;"
                                    "Database=PulseCoreTest5;"
                                    "UID=PCDev2;"
                                    "PWD=PCCSDev2PC5_!")
            self.cursor = self.conn.cursor()
            print("Connection Succeeded")
        except:
            print("Connection Failed")
 
    def submit(self):
        sql = """INSERT INTO [PulseCoreTest5].[dbo].[PC_RequestTable] (dDateStart, dDateEnd, nEmployee, sReason)
                    VALUES (%s, %s, %s, %s)"""
        values = (dDateStart, dDateEnd, nEmployee, str(self.Rvar1.get()) + self.T1.get())
        self.cursor.execute(sql, values)
        self.conn.commit()       
root = Tk()
root.resizable(False, False)
window = Window(root)
root.mainloop()




#displays all current request info from PC_RequestTable
if nEmployee == #manager id :
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