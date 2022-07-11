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
    def login(login_info):
        Model.infofetch(login_info)
        user_info = Model.cursor.fetchone()
        Controller.user_id = user_info[2]
        Controller.user_name = user_info[1]

    #get stellvertreter personalnummer
    stell_reqs = []
    def get_stell():
        try:
            Model.check_stell(Controller.user_name)
            Controller.stell_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    #update stell status
    def update_stell(nStellStatus, xnRequest):
        try:
            Model.update_stell(nStellStatus, xnRequest)
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    #update vacation days
    days_left = int()
    def get_days_left(login_info):
        Model.get_days_left(login_info)
        days_left_row = Model.cursor.fetchone()
        Controller.days_left = days_left_row[0]
    
    #update
    def update(updated_info):
        try:
            Model.update_request(updated_info)
        except pyodbc.DataError as error:
            Controller.error_window(f'Invalid date format\n\n{error}')
        except pyodbc.Error as error:
            Controller.error_window('Error', f'{error}')
    # ---- loginbox

    # ---- request_window

    #submit
    def sub_new_info(new_info):
        try:
            Model.submit_request(new_info)
            Controller.error_window('Your submission was recorded!', 'Info')
        except pyodbc.DataError as error:
            Controller.error_window(f'Formatting Error\n\n{error}', 'Error')
        except pyodbc.Error as error:
            Controller.error_window(f'Connection Error\n\n{error}', 'Error')

    def reduce_days(nDaysLeft):
        Model.reduce_days(nDaysLeft, Controller.user_id)
    
    # ---- request_window

    # ---- manager_view

    #load all
    fetched_reqs = []
    def search_all():
        try:
            Model.all_search()
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')
    
    #search by employee, also used in the employee_req_view
    def search_emp(nEmployee):
        try:
            Model.emp_search(nEmployee)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')
    
    #search by antragnummer, also used in the employee_req_view
    req_data = []
    def search(xnRequest):
        try:
            Model.fetch_request(xnRequest)
            Controller.req_data = Model.cursor.fetchone()
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    #update
    def man_update(man_info):
        try:
            Model.man_update(man_info)
        except pyodbc.DataError as error:
            messagebox.showerror('Error', f'Incorrect Formatting \n\nError: {error}')
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    #delete
    def delete(xnRequest):
        try:
            Model.delete_request(xnRequest)
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')
    
    #load unseen
    def get_unseen():
        try:
            Model.get_unseen()
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')
    
    #mark as seen
    def set_seen(xnRequest):
        try:
            Model.set_seen(xnRequest)
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    # ---- manager_view

    # ---- schedule

    #initialization list
    current_date = datetime.datetime.now()    
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    ProduktionsGruppe = {0:'Wissenträger', 1:'Produktions Gruppe 1', 2:'Produktions Gruppe 2', 
                     3:'Produktions Gruppe 3', 4:'Produktions Gruppe 4', 5:'Produktionsunterstützung',
                     6: 'Keine Gruppe'}

    years = {0:current_year, 1:current_year + 1, 2: current_year + 2, 3: current_year + 3, 
                 4:current_year + 4, 5:current_year + 5}

    list_of_holiday_dates = []
    list_of_emp_numbers = []
    headers = []
    data_values = [] 
    selected_group = []
    selected_month = [current_month]
    selected_year = [current_year]
    request_list_raw = []
    request_dictionary = {}

    #methods
    login_empnum = []
    manager_empnums = [905] 

    def __init__(self, model, view):
        self.model = model
        self.view = view    

    def get_group_from_empnum(empnum):
        Model.get_group_from_empnum(empnum)
        pyodbc_row = Model.cursor.fetchall()
        if (str(pyodbc_row)[2]) == 'N':
            Controller.selected_group.append(6)
        else:
            Controller.selected_group.append(int(str(pyodbc_row)[2]))

    def date_range(start, end):
            delta = end - start
            days = [start + timedelta(days = i) for i in range(delta.days + 1)]
            return days

    def get_holidays():
        Model.get_holidays()
        holidays = Model.cursor.fetchall()
        for holiday in holidays:
            holiday_date = holiday[1]
            Controller.list_of_holiday_dates.append(holiday_date.strftime('%Y.' + '%m.' + '%d'))
    
    def create_table():
        Controller.get_emp_list()
        Controller.get_requests()
        Controller.get_dates_for_headers()
        Controller.input_default_data()
        Controller.edit_data()

    def get_emp_list():    
        if Controller.selected_group[0] == 6:
            Model.get_no_group_list()
        else:
            Model.get_emp_list(Controller.selected_group[0])
        Controller.list_of_emp_numbers = Model.cursor.fetchall()
        Controller.list_of_emp_numbers.sort()
        for i in range(0, len(Controller.list_of_emp_numbers)):
            item = str(Controller.list_of_emp_numbers[i])
            item = re.sub(r'[(,)]', '', item)
            newitem = item.replace('"', "")
            Controller.list_of_emp_numbers.remove(Controller.list_of_emp_numbers[i])
            Controller.list_of_emp_numbers.insert(i, int(newitem[0:-1]))

    def get_requests():
        Model.get_requests()
        Controller.request_list_raw = Model.cursor.fetchall()
        for item in Controller.request_list_raw:
            selected_employee_number = item[3]
            if item[6] is None:
                pass
            elif item[6] == 'None':
                pass
            else:
                Model.get_stellvertreter_info(item[6])
                selected_stellvertreter_info = str(Model.cursor.fetchall())
                selected_stellvertreter_numberstr = ''
                for m in selected_stellvertreter_info:
                    if m.isdigit():
                        selected_stellvertreter_numberstr = selected_stellvertreter_numberstr + m
                        selected_stellvertreter_number = int(selected_stellvertreter_numberstr)         
                if selected_employee_number in Controller.list_of_emp_numbers:
                            Controller.request_dictionary[item[0]] = [selected_employee_number, item[1].strftime('%Y.' + '%m.' + '%d')]
                            start_date = item[1]
                            end_date = item[2]
                            daterangelist = Controller.date_range(start_date, end_date)
                            for i in range(0, len(daterangelist)):
                                Controller.request_dictionary[item[0] + (i * .01)] = [selected_employee_number, 
                                                    daterangelist[i].strftime('%Y.' + '%m.' + '%d'), item[5], 
                                                    selected_stellvertreter_number, item[7]]
                else:
                        pass

    def get_dates_for_headers():    
        Controller.headers.clear()
        number_of_days = calendar.monthrange(Controller.selected_year[0], Controller.selected_month[0])[1]
        first_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], 1)
        last_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], number_of_days)
        
        delta = last_date - first_date
        for i in range(delta.days + 1):
            day = ((first_date + datetime.timedelta(days = i)))
            Controller.headers.append(day.strftime('%a %d'))

    def input_default_data():
        Controller.get_holidays()
        Controller.data_values.clear()    
        for ii in range(0, len(Controller.list_of_emp_numbers)):
            data_list = []
            for i in range(0, len(Controller.headers)):
                Wochenende = set([5, 6])
                if datetime.datetime(int(Controller.selected_year[0]), 
                                     int(Controller.selected_month[0]), i + 1).weekday() in Wochenende:
                    data_list.append('Wochenende')
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

    def edit_data():
        for key, value in Controller.request_dictionary.items():
            req_list = value
            number_entered = req_list[0]
            dateentered = req_list[1]
            status = req_list[2]
            stell_num = req_list[3]
            stell_status = req_list[4]

            dayentered = (dateentered[8:10:1]).lstrip('0')
            monthentered = (dateentered[5:7:1]).lstrip('0')
            yearentered = dateentered[0:4:1]

            for item in Controller.list_of_emp_numbers:
                if number_entered == item:
                    nameindex = Controller.list_of_emp_numbers.index(number_entered)    
                else:
                    nameindex = None
                if int(monthentered) == Controller.selected_month[0] and int(
                    yearentered) == Controller.selected_year[0] and nameindex != None:
                    data_list = list(Controller.data_values[nameindex])
                    if data_list[int(dayentered) - 1] == ' ':
                        data_list[int(dayentered) - 1] = status
                        data_tuple = tuple(data_list)
                        Controller.data_values[nameindex] = data_tuple
                    else:
                        pass
                else:
                    pass
                if stell_num == item:
                    nameindex = Controller.list_of_emp_numbers.index(stell_num)    
                else:
                    nameindex = None
                if int(monthentered) == Controller.selected_month[0] and int(
                    yearentered) == Controller.selected_year[0] and nameindex != None:
                    data_list = list(Controller.data_values[nameindex])
                    if data_list[int(dayentered) - 1] == ' ':
                        if stell_status == 1:
                            data_list[int(dayentered) - 1] = 'Stellvertreter'  
                        elif stell_status == 0:
                            data_list[int(dayentered) - 1] = 'Stellvertreter?'
                        else:
                            pass
                        data_tuple = tuple(data_list)
                        Controller.data_values[nameindex] = data_tuple
                    else:
                        pass
                else:
                    pass

    # ---- schedule
    
    #error handler
    def error_window(message, type = 'info', timeout = 2500):
        error_window = tk.Tk()
        error_window.withdraw()
        try:
            error_window.after(timeout, error_window.destroy)
            if type == 'info':
                messagebox.showinfo('Info', message, master = error_window)
            elif type == 'error':
                messagebox.showerror('Error', message, master = error_window)
        except:
            pass