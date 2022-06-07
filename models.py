import pyodbc


class Model:
        #The following are for all SQL functions within the model
        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                    "Server=SOPCP01DE;"
                    "Database=PulseCoreTest5;"
                    "UID=PCDev2;"
                    "PWD=PCCSDev2PC5_!;")
    
        cnxn = pyodbc.connect(cnxn_str)

        cursor = cnxn.cursor()
    
        #for infofetch in loginbox
        """Parameters
        -----------
        nEmployee : int
        - single element tuple"""
        infofetcher = """SELECT [sFirstName]
                        ,[sName]
                        ,[nEmployee]
                        ,[bStatus]
                        ,[nProduktionsGruppe]
                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                        WHERE [nEmployee] = ?"""

        def infofetch(login_info):
                Model.cursor.execute(Model.infofetcher, login_info)
                user_info = Model.cursor.fetchone()
                user_id = user_info[2]
                print(user_id)
        
        #for submit in request_window
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        nEmployee : int
        sReasons : str
        sStatus : str"""
        new_info = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus)
            VALUES (?, ?, ?, ?, ?)"""

        def submit_request(new_info):
                Model.cursor.execute(Model.new_info, new_info)
                Model.cnxn.commit() 
                Model.cnxn.close()

        #fetch a request by its request number
        request_fetcher = """SELECT * FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"
                            WHERE (xnRequest) = ?"""
        
        def fetch_request(xnRequest):
                Model.cursor.execute(Model.request_fetcher, xnRequest)
                print(Model.cursor.fetchall())