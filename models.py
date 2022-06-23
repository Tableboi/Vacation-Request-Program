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

        # ---- loginbox

        #infofetch
        infofetcher = """SELECT [sFirstName]
                        ,[sName]
                        ,[nEmployee]
                        ,[bStatus]
                        ,[nProduktionsGruppe]
                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                        WHERE [nEmployee] = ?"""
        """Parameters
        -----------
        nEmployee : int
        - single element tuple"""

        def infofetch(login_info):
                Model.cursor.execute(Model.infofetcher, login_info)
        
        # ---- loginbox

        # ---- request_window
        
        #submit
        new_info = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus, sStellvertreter)
            VALUES (?, ?, ?, ?, ?, ?)"""
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        nEmployee : int
        sReasons : str
        sStatus : str
        sStellvertreter : str"""

        def submit_request(new_info):
                Model.cursor.execute(Model.new_info, new_info)
                Model.cnxn.commit()

        #fetch remaining vacation days
        """Parameters
        ---------
        nEmployee : int"""
        days_left_getter = """SELECT [nDaysLeft] FROM [PulseCoreTest5].[dbo].[PO_employee]
                        WHERE [nEmployee] = ?"""

        def get_days_left(login_info):
                Model.cursor.execute(Model.days_left_getter, login_info)

        # ---- request_window

        # ---- manager_view

        #fetch a request by its request number
        request_fetcher = """SELECT [dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [xnRequest] = ?"""
        """Parameters
        -----------
        xnRequest : int"""
        
        def fetch_request(xnRequest):
                Model.cursor.execute(Model.request_fetcher, xnRequest)

        #search all vacation requests by nEmployee
        """Parameters
        -----------
        nEmployee : int"""
        emp_searcher = """SELECT [xnRequest]
                        ,[dDateStart]
                        ,[dDateEnd]
                        ,[sStellvertreter]
                        ,[sReasons]
                        ,[sStatus]
                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                        WHERE [nEmployee] = ?"""
        
        def emp_search(nEmployee):
                Model.cursor.execute(Model.emp_searcher, nEmployee)
        
        #fetch all vacation requests
        all_searcher = """SELECT [xnRequest]
                        ,[dDateStart]
                        ,[dDateEnd]
                        ,[sStellvertreter]
                        ,[sReasons]
                        ,[sStatus]
                        ,[nEmployee]
                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
        """Parameters
        -----------
        None"""
        def all_search():
                Model.cursor.execute(Model.all_searcher)

        #update
        man_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                           SET [dDateStart] = ?,
                           [dDateEnd] = ?,
                           [sReasons] = ?,
                           [sStatus] = ?,
                           [sStellvertreter] = ?
                           WHERE [xnRequest] = ?"""
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        sReasons : str
        xnRequest : int
        sStatus : str
        sStellvertreter : str"""
        
        def man_update(man_info):
                Model.cursor.execute(Model.man_updater, man_info)
                Model.cnxn.commit()

        #delete
        request_deleter = """DELETE FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                          WHERE [xnRequest] = ?"""
        """Parameters
        -----------
        xnRequest : int"""

        def delete_request(xnRequest):
                Model.cursor.execute(Model.request_deleter, xnRequest)
                Model.cnxn.commit()

        # ---- manager_view

        # ---- employee_req_view

        #search by employee, see search_emp in the manager_view section above

        #search by antragsnummer, see search in the manager_view section above

        #update
        request_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                           SET [dDateStart] = ?,
                           [dDateEnd] = ?,
                           [sReasons] = ?,
                           [sStellvertreter] = ?
                           WHERE [xnRequest] = ? AND [nEmployee] = ?"""
        """Parameters
        -----------
        dDateStart : date
        dDateEnd : date
        sReasons : str
        xnRequest : int
        sStellvertreter : str"""
        
        def update_request(updated_info):
                Model.cursor.execute(Model.request_updater, updated_info)
                Model.cnxn.commit()

        # ---- employee_req_view
        
        #SCHEDULE QUERIES
        number_getter = """SELECT [nEmployee]
                            FROM [PulseCoreTest5].[dbo].[PO_employee]
                            WHERE [nProduktionsGruppe] = ?"""
        
        no_group_getter = """ SELECT [nEmployee]
                                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                                        WHERE [nProduktionsGruppe] IS NULL"""
        
        holiday_getter = """SELECT [Feiertag], [Datum] 
                                FROM [PulseCoreTest5].[dbo].[PC_Holidays]"""
                                
        request_getter = """SELECT [xnRequest] 
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
        
        def get_holidays():
                Model.cursor.execute(Model.holiday_getter)

        def get_emp_list(produktionsgruppe):
                Model.cursor.execute(Model.number_getter, produktionsgruppe)
        
        def get_no_group_list():
                Model.cursor.execute(Model.no_group_getter)
        
        def get_requests():
                Model.cursor.execute(Model.request_getter)