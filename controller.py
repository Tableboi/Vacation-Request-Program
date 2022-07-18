import calendar
import pyodbc
import datetime
from datetime import timedelta
import re

from tkinter import messagebox
from calendar import month

from models import Model
import tkinter as tk

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    current_date = datetime.datetime.now()
    current_month = int(current_date.strftime('%m'))
    current_year = int(current_date.strftime('%Y'))

    # ---- loginbox

    #submit button
    user_id = int()
    user_name = str
    user_info = []

    def login(self, login_info):
        Model.infofetch(self, login_info)
        user_info = Model.cursor.fetchone()
        Controller.user_id = user_info[2]
        Controller.user_name = user_info[1]

    #get stellvertreter personalnummer
    stell_reqs = []
    def get_stell(self):
        try:
            Model.check_stell(self, Controller.user_name)
            Controller.stell_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #update stell status
    def update_stell(self, nStellStatus, xnRequest):
        try:
            Model.update_stell(self, nStellStatus, xnRequest)
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #update vacation days
    days_left = int()
    def get_days_left(self, login_info):
        Model.get_days_left(self, login_info)
        days_left_row = Model.cursor.fetchone()
        Controller.days_left = days_left_row[0]
    
    #update
    def update(self, updated_info):
        try:
            Model.update_request(self, updated_info)
            Controller.error_window(self, 'Update Successful', 'info')
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Invalid date format\n\n{error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    # ---- loginbox

    # ---- request_window

    #submit
    def sub_new_info(self, new_info):
        try:
            Model.submit_request(self, new_info)
            Controller.error_window(self, 'Your submission was recorded!', 'info')
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Formatting Error\n\n{error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'Connection Error\n\n{error}', 'error')

    def reduce_days(self, nDaysLeft):
        Model.reduce_days(self, nDaysLeft, Controller.user_id)
    
    # ---- request_window

    # ---- manager_view

    #load all
    fetched_reqs = []
    def search_all(self):
        try:
            Model.all_search(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by employee, also used in the employee_req_view
    def search_emp(self, nEmployee):
        try:
            Model.emp_search(self, nEmployee)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by antragnummer, also used in the employee_req_view
    req_data = []
    def search(self, xnRequest):
        try:
            Model.fetch_request(self, xnRequest)
            Controller.req_data = Model.cursor.fetchone()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #update
    def man_update(self, man_info):
        try:
            Model.man_update(self, man_info)
            Controller.error_window(self, 'Update Successful', 'info')
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Incorrect Formatting \n\nError: {error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #delete
    def delete(self, xnRequest):
        try:
            Model.delete_request(self, xnRequest)
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #load unseen
    def get_unseen(self):
        try:
            Model.get_unseen(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #mark as seen
    def set_seen(self, xnRequest):
        try:
            Model.set_seen(self, xnRequest)
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    # ---- manager_view

    # ---- schedule

    #initialization list
    current_date = datetime.datetime.now()    
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    ProduktionsGruppe = {0:'WISSENTRÄGER', 1:'PRODUKTIONS GRUPPE 1', 2:'PRODUKTIONS GRUPPE 2', 
                     3:'PRODUKTIONS GRUPPE 3', 4:'PRODUKTIONS GRUPPE 4', 5:'PRODUKTIONSUNTERSTÜTZ',
                     6: 'KEINE GRUPPE'}

    years = {0:current_year, 1:current_year + 1, 2: current_year + 2, 3: current_year + 3, 
                 4:current_year + 4, 5:current_year + 5}

    list_of_holiday_dates = []
    list_of_emp_info = []
    rows = []
    headers = []
    data_values = [] 
    selected_group = []
    selected_month = [current_month]
    selected_year = [current_year]
    request_list_raw = []
    request_dictionary = {}

    def date_range(self, start, end):
        delta = end - start
        days = [start + timedelta(days = i) for i in range(delta.days + 1)]
        return days

    #methods
    login_empnum = []
    manager_empnums = [905]   

    def get_group_from_empnum(self, empnum):
        Model.get_group_from_empnum(self, empnum)
        pyodbc_row = Model.cursor.fetchall()
        if (str(pyodbc_row)[2]) == 'N':
            Controller.selected_group.append(6)
            Controller.login_empnum.clear()
        else:
            Controller.selected_group.append(int(str(pyodbc_row)[2]))
            Controller.login_empnum.clear()
    
    def get_emp_list(self):    
        def get_group():
            if Controller.selected_group[0] == 6:
                Model.get_no_group_list(self)
            else:
                Model.get_emp_list(self, Controller.selected_group[0])
            raw_list_of_emp_info = Model.cursor.fetchall()
            raw_list_of_emp_info.sort()
            for item in raw_list_of_emp_info:
                Controller.list_of_emp_info.append(item)             
        Controller.list_of_emp_info.clear()
        Controller.rows.clear()
        if Controller.selected_group[0] == 7:
            for i in range(0,7):
                Controller.list_of_emp_info.append([Controller.ProduktionsGruppe[i], None])
                Controller.selected_group.clear()
                Controller.selected_group.append(i)
                get_group()
            Controller.selected_group.clear()
            Controller.selected_group.append(7)
                
        else:
            get_group()
        
        for item in Controller.list_of_emp_info:
                if item[1] is not None:
                    emp_last_name = item[0]
                    emp_first_name = item[1]
                    emp_number = item[2]
                    Controller.rows.append('{}, {} {}'.format(emp_last_name, emp_first_name, emp_number)) 
                if item[1] is None:
                    Controller.rows.append(item[0])
   
    def get_requests(self):
        Model.get_requests(self)
        Controller.request_list_raw = Model.cursor.fetchall()
        for item in Controller.request_list_raw:
            selected_employee = []
            request_number = item[0]
            emp_last_name = item[1]
            emp_first_name = item[2]
            emp_number = item[3]
            date_start = item[4]
            date_end = item[5]
            status = item[6]
            stell_name = item[7]
            stell_status = item[8]
            selected_employee.append('{}, {} {}'.format(emp_last_name, emp_first_name, emp_number))
            if stell_name is not None and stell_name != 'None' and stell_name != '':
                Model.get_stellvertreter_info(self, stell_name)
                raw_stellvertreter_info = Model.cursor.fetchall()
                stell_last_name = raw_stellvertreter_info[0][0]
                stell_first_name = raw_stellvertreter_info[0][1]
                stell_number = raw_stellvertreter_info[0][2]
                stellvertreter_info = '{}, {} {}'.format(stell_last_name, stell_first_name, stell_number)
            else:
                stellvertreter_info = None         
            if selected_employee[0] in Controller.rows:
                        Controller.request_dictionary[request_number] = [item[3], date_start.strftime('%Y.' + '%m.' + '%d')]
                        daterangelist = Controller.date_range(self, date_start, date_end)
                        for i in range(0, len(daterangelist)):
                            Controller.request_dictionary[request_number + (i * .01)] = [selected_employee, 
                                                daterangelist[i].strftime('%Y.' + '%m.' + '%d'), status, 
                                                stellvertreter_info, stell_status]

    def get_holidays(self):
        Model.get_holidays(self)
        holidays = Model.cursor.fetchall()
        for holiday in holidays:
            holiday_date = holiday[1]
            Controller.list_of_holiday_dates.append(holiday_date.strftime('%Y.' + '%m.' + '%d'))
    
    def create_table(self):
        Controller.get_emp_list(self)
        Controller.get_requests(self)
        Controller.get_dates_for_headers(self)
        Controller.input_default_data(self)
        Controller.edit_data(self)

    def get_dates_for_headers(self):    
        Controller.headers.clear()
        number_of_days = calendar.monthrange(Controller.selected_year[0], Controller.selected_month[0])[1]
        first_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], 1)
        last_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], number_of_days)
        
        delta = last_date - first_date
        for i in range(delta.days + 1):
            day = ((first_date + datetime.timedelta(days = i)))
            Controller.headers.append(day.strftime('%a %d'))

    def input_default_data(self):
        Controller.get_holidays(self)
        Controller.data_values.clear()    
        for ii in range(0, len(Controller.list_of_emp_info)):
            data_list = []
            for i in range(0, len(Controller.headers)):
                Wochenende = set([5, 6])
                if Controller.list_of_emp_info[ii][1] is None:
                    data_list.append('______________')
                elif datetime.datetime(int(Controller.selected_year[0]), 
                                     int(Controller.selected_month[0]), i + 1).weekday() in Wochenende:
                    data_list.append('   ')
                else:
                    data_list.append(' ')
            for item in Controller.list_of_holiday_dates:
                dayentered = (item[8:10:1]).lstrip('0')
                monthentered = (item[5:7:1]).lstrip('0')
                yearentered = item[0:4:1]
                if int(monthentered) == Controller.selected_month[0]:
                    if int(yearentered) == Controller.selected_year[0]:
                        data_list[int(dayentered) - 1] = 'Feiertag'
            data_tuple = tuple(data_list)
            Controller.data_values.append(data_tuple)
         
    def edit_data(self):
        for key, value in Controller.request_dictionary.items():
            req_info = value
            employee_info = req_info[0][0]
            date_entered = req_info[1]
            status = req_info[2]
            stell_info = req_info[3]
            stell_status = req_info[4]

            dayentered = (date_entered[8:10:1]).lstrip('0')
            monthentered = (date_entered[5:7:1]).lstrip('0')
            yearentered = date_entered[0:4:1]

            for item in Controller.rows:
                if employee_info == item:
                    nameindex = Controller.rows.index(employee_info)    
                else:
                    nameindex = None
                if int(monthentered) == Controller.selected_month[0] and int(
                    yearentered) == Controller.selected_year[0] and nameindex != None:
                    data_list = list(Controller.data_values[nameindex])
                    if data_list[int(dayentered) - 1] == ' ':
                        data_list[int(dayentered) - 1] = status
                        data_tuple = tuple(data_list)
                        Controller.data_values[nameindex] = data_tuple
                if stell_info == item:
                    nameindex = Controller.rows.index(stell_info)    
                else:
                    nameindex = None
                if int(monthentered) == Controller.selected_month[0] and int(
                    yearentered) == Controller.selected_year[0] and nameindex != None:
                    data_list = list(Controller.data_values[nameindex])
                    if data_list[int(dayentered) - 1] == ' ':
                        if stell_status == 1:
                            data_list[int(dayentered) - 1] = 'Sv.: {}'.format(employee_info)  
                        elif stell_status == 0:
                            data_list[int(dayentered) - 1] = 'Sv.?: {}'.format(employee_info)
                        data_tuple = tuple(data_list)
                        Controller.data_values[nameindex] = data_tuple
    # ---- schedule
    
    #popup handler
    def error_window(self, message, type = 'info', timeout = 2500):
        error_window = tk.Tk()
        error_window.withdraw()
        error_window.after(timeout, error_window.destroy)
        if type == 'info':
            messagebox.showinfo('Info', message, master = error_window)
        elif type == 'error':
            messagebox.showerror('Error', message, master = error_window)
