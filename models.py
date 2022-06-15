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

        #fetch a request by its request number
        """Parameters
        -----------
        xnRequest : int"""
        request_fetcher = """SELECT [dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [xnRequest] = ?"""
        
        def fetch_request(xnRequest):
                Model.cursor.execute(Model.request_fetcher, xnRequest)

        #employee update an existing request
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        sReasons : str
        xnRequest : int"""
        request_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                           SET [dDateStart] = ?,
                           [dDateEnd] = ?,
                           [sReasons] = ?
                           WHERE [xnRequest] = ? AND [nEmployee] = ?"""
        
        def update_request(updated_info):
                Model.cursor.execute(Model.request_updater, updated_info)
                Model.cnxn.commit()

        #manager update, includes sStatus
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        sReasons : str
        xnRequest : int
        sStatus : str"""
        man_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                           SET [dDateStart] = ?,
                           [dDateEnd] = ?,
                           [sReasons] = ?,
                           [sStatus] = ?
                           WHERE [xnRequest] = ?"""
        
        def man_update(man_info):
                Model.cursor.execute(Model.man_updater, man_info)
                Model.cnxn.commit()


        #delete an existing request
        """Parameters
        -----------
        xnRequest : int"""
        request_deleter = """DELETE FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                          WHERE [xnRequest] = ?"""

        def delete_request(xnRequest):
                Model.cursor.execute(Model.request_deleter, xnRequest)
                Model.cnxn.commit()
        
        #search all vacation requests by nEmployee
        """Parameters
        -----------
        nEmployee : int"""
        emp_searcher = """SELECT [dDateStart]
                        ,[dDateEnd]
                        ,[xnRequest]
                        ,[sReasons]
                        ,[sStatus]
                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                        WHERE [nEmployee] = ?"""
        
        def emp_search(nEmployee):
                Model.cursor.execute(Model.emp_searcher, nEmployee)
        
        #fetch all vacation requests
        """Parameters
        -----------
        None"""
        all_searcher = """SELECT *
                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
        def all_search():
                Model.cursor.execute(Model.all_searcher)