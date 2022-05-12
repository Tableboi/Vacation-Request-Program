#submit function for the login button
def submit(self):
    cursor.execute ("SELECT TOP [sFirstName]"
                        ",[sName]"
                        ",[nEmployee]"
                        ",[bStatus]"
                        ",[nProduktionsGruppe]"
                        "FROM [PulseCoreTest5].[dbo].[PO_employee]"
                        f"WHERE [nEmployee] = {login}")
    employeeinfo = cursor.fetchone()
    nEmployee = float(employeeinfo[2])

#isChecked() function for inout request
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

#connect function for conneting to the database
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

#submit for the vacation request info input
def submit(self):
        sql = """INSERT INTO [PulseCoreTest5].[dbo].[PC_RequestTable] (dDateStart, dDateEnd, nEmployee, sReason)
                    VALUES (%s, %s, %s, %s,%s)"""
        values = (self.dDateStart.get(), self.dDateEnd.get(), self.E4.get(), str(self.Rvar1.get()) + self.T1.get("1.0", "end"))
        self.cursor.execute(sql, values)
        self.conn.commit()