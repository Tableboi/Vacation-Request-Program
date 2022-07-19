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
        #on login
        def infofetch(self, nEmployee):
                """Parameters
                -----------
                nEmployee : int
                - single element tuple"""
                self.infofetcher = """SELECT [sFirstName]
                                ,[sName]
                                ,[nEmployee]
                                ,[bStatus]
                                ,[nProduktionsGruppe]
                                FROM [PulseCoreTest5].[dbo].[PO_employee]
                                WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.infofetcher, nEmployee)
        
        #check for sName and sStellstatus
        def check_stell(self, sName):
                """Parameters
                ---------
                sName = str"""
                self.stell_checker = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [sStellvertreter] = ? AND [nStellStatus] = 0"""

                Model.cursor.execute(self.stell_checker, sName)

        #update stellstatus
        def update_stell(self, nStellStatus, xnRequest):
                """Parameters
                ---------
                nStellStatus = int (0-2)
                xnRequest = int
                """
                self.stell_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                SET [nStellStatus] = ? WHERE [xnRequest] = ?"""
                Model.cursor.execute(self.stell_updater, nStellStatus, xnRequest)
                Model.cnxn.commit()

        #update requests in scrollframe, autosets stellstatus to 0        
        def update_request(self, updated_info):      
                """Parameters
                -----------
                dDateStart : date
                dDateEnd : date
                sReasons : str
                nStellStatus : int
                xnRequest : int
                nEmployee : int"""
                self.request_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                SET [dDateStart] = ?
                                ,[dDateEnd] = ?
                                ,[sReasons] = ?
                                ,[nStellStatus] = ?
                                ,[sStatus] = 'geplant'
                                WHERE [xnRequest] = ? AND [nEmployee] = ?"""
                Model.cursor.execute(self.request_updater, updated_info)
                Model.cnxn.commit()
        # ---- loginbox

        # ---- request_window
        #submit
        def fetch_name(self, nEmployee):
                """Parameters
                -----------
                nEmployee : int"""

                self.name_from_empnum_getter = """SELECT [sFirstName], [sName]
                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                        WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.name_from_empnum_getter, nEmployee)

        def submit_request(self, data):
                """Parameters
                -----------
                dDateStart : date
                dDateEnd : date
                nEmployee : int
                sReasons : str
                sStatus : str
                sStellvertreter : str
                sFirstName : str
                sLastName : str"""

                self.request_submitter = """INSERT INTO dbo.PC_VacationsRequests (dDateStart, dDateEnd, nEmployee, sReasons, sStatus, sStellvertreter, sFirstName, sLastName)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                Model.cursor.execute(self.request_submitter, data)
                Model.cnxn.commit()

        def reduce_days(self, nDaysLeft, nEmployee):
                """Parameters
                ---------
                nEmployee : int"""
                self.day_reducer = """UPDATE [PulseCoreTest5].[dbo].[PO_employee] SET [nDaysLeft] = ?
                                        WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.day_reducer, nDaysLeft, nEmployee)
                Model.cnxn.commit()
        # ---- request_window

        # ---- manager_view
        #fetch all vacation requests
        def all_search(self):
                """Parameters
                -----------
                None"""
                self.all_searcher = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
                Model.cursor.execute(self.all_searcher)

        #search all vacation requests by nEmployee
        def emp_search(self, nEmployee):
                """Parameters
                -----------
                nEmployee : int"""
                self.emp_searcher = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.emp_searcher, nEmployee)
        
        #load unseen
        def get_unseen(self):
                """Parameters
                ---------
                None"""
                self.unseen_getter = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [nNotify] = 0"""
                Model.cursor.execute(self.unseen_getter)
        
        #fetch approved reqs
        def get_by_green(self):
                """Parameters
                ---------
                None"""
                self.green_getter = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [sStatus] = 'bestätigt'"""
                Model.cursor.execute(self.green_getter)

        #fetch unapproved reqs
        def get_by_yellow(self):
                """Parameters
                ---------
                None"""
                self.yellow_getter = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [sStatus] = 'geplant'"""
                Model.cursor.execute(self.yellow_getter)
        
        #fetch denied reqs
        def get_by_red(self):
                """Parameters
                ---------
                None"""
                self.red_getter = """SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [sStatus] = 'denied'"""
                Model.cursor.execute(self.red_getter)
        
        #fetch reqs by name
        def get_by_name(self, sLastName):
                """Parameters
                ---------
                sLastName : str"""
                self.by_name_getter ="""SELECT [xnRequest]
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                                ,[sStellvertreter]
                                ,[nStellStatus]
                                ,[nNotify]
                                ,[sFirstName]
                                ,[sLastName]
                                FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [sLastName] = ?"""
                Model.cursor.execute(self.by_name_getter, sLastName)

        #update
        def man_update(self, man_info):       
                """Parameters
                -----------
                dDateStart : date
                dDateEnd : date
                sReasons : str
                sStatus : str
                sStellvertreter : str
                nApprover : int
                xnRequest : int"""
                self.man_updater = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                SET [dDateStart] = ?
                                ,[dDateEnd] = ?
                                ,[sReasons] = ?
                                ,[sStatus] = ?
                                ,[sStellvertreter] = ?
                                ,[nApprover] = ?
                                WHERE [xnRequest] = ?"""
                Model.cursor.execute(self.man_updater, man_info)
                Model.cnxn.commit()

        #delete
        def delete_request(self, xnRequest):
                """Parameters
                -----------
                xnRequest : int"""
                self.request_deleter = """DELETE FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                WHERE [xnRequest] = ?"""
                Model.cursor.execute(self.request_deleter, xnRequest)
                Model.cnxn.commit()

        #mark as seen
        def set_seen(self, xnRequest):
                """Parameters
                ---------
                xnRequest : int"""
                self.seen_setter = """UPDATE [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                SET [nNotify] = 1
                                WHERE [xnRequest] = ?"""
                Model.cursor.execute(self.seen_setter, xnRequest)
                Model.cnxn.commit()
        # ---- manager_view
        
        # ---- schedule
        def get_group_from_empnum(self, nEmployee):
                """Parameters
                ---------
                nEmployee : int"""
                self.group_from_empnum_getter = """SELECT [nProduktionsGruppe]
                                FROM [PulseCoreTest5].[dbo].[PO_employee]
                                WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.group_from_empnum_getter, nEmployee)

        def get_emp_list(self, nProduktionsGruppe):
                """Parameters
                ---------
                nProduktionsGruppe : int"""
                self.number_getter = """SELECT [sName], [sFirstName], [nEmployee]
                                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                                                WHERE [nProduktionsGruppe] = ?"""
                Model.cursor.execute(self.number_getter, nProduktionsGruppe)

        def get_all_emp_list(self):
                """Parameters
                ---------
                None"""
                self.all_number_getter = """SELECT [sName], [sFirstName], [nEmployee]
                                        FROM [PulseCoreTest5].[dbo].[PO_employee]"""
                Model.cursor.execute(self.all_number_getter)

        def get_no_group_list(self):
                """Parameters
                ---------
                None"""
                self.no_group_getter = """ SELECT [sName], [sFirstName], [nEmployee]
                                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                                        WHERE [nProduktionsGruppe] IS NULL"""
                Model.cursor.execute(self.no_group_getter)

        def get_requests(self):
                """Parameters
                ---------
                None"""
                self.request_getter = """SELECT [xnRequest] 
                                        ,[sLastName]
                                        ,[sFirstName]
                                        ,[dDateStart]
                                        ,[dDateEnd]
                                        ,[nEmployee]
                                        ,[sReasons]
                                        ,[sStatus]
                                        ,[sStellvertreter]
                                        ,[nStellStatus]
                                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
                Model.cursor.execute(self.request_getter)

        def get_stellvertreter_info(self, sName):
                """Parameters
                ---------
                sName : str"""
                self.empnum_from_name_getter = """SELECT [sName], [sFirstName], [nEmployee]
                                                FROM [PulseCoreTest5].[dbo].[PO_employee]
                                                WHERE [sName] = ?""" 
                Model.cursor.execute(self.empnum_from_name_getter, sName)

        def get_holidays(self):
                """Parameters
                ---------
                None"""
                self.holiday_getter = """SELECT [Feiertag], [Datum] 
                                        FROM [PulseCoreTest5].[dbo].[PC_holidays]"""
                Model.cursor.execute(self.holiday_getter)
        # ---- schedule

        # ---- resturlaub
        def get_holidates(self, nEmployee):
                """Parameters
                ---------
                nEmployee : int"""
                self.holidate_getter = """SELECT [dDateStart]
                                        ,[dDateEnd]
                                        FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]
                                        WHERE [nEmployee] = ? AND [sStatus] != 'denied'"""
                Model.cursor.execute(self.holidate_getter, nEmployee)
        
        #fetch remaining vacation days
        def get_days_left(self, login_info):
                """Parameters
                ---------
                nEmployee : int"""
                self.days_left_getter = """SELECT [nDaysLeft] FROM [PulseCoreTest5].[dbo].[PO_employee]
                                WHERE [nEmployee] = ?"""
                Model.cursor.execute(self.days_left_getter, login_info)
        # ---- resturlaub