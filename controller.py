import calendar
import pyodbc
import datetime
from datetime import timedelta

from tkinter import messagebox

from models import Model
import tkinter as tk

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    #get current date info
    current_date = datetime.datetime.now()
    current_month = int(current_date.strftime('%m'))
    current_year = int(current_date.strftime('%Y'))

    # ---- loginbox

    #initialize needed variables
    user_id = int()
    user_name = str
    user_info = []

    #fetch user info
    def login(self, login_info):
        Model.infofetch(self, login_info)
        user_info = Model.cursor.fetchone()
        Controller.user_id = user_info[2]
        Controller.user_name = user_info[1]

    #get stellvertreter personalnummer
    stell_reqs = []
    def get_stell(self):
        try:
            Model.check_stell(self, Controller.user_id)
            Controller.stell_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    stell_info_formatted = []
    def get_stellvertreter_name(self, nStellEmp):
        Controller.stell_info_formatted.clear()
        try:
            Model.get_stellvertreter_name(self, nStellEmp)
            item = Model.cursor.fetchall()
            last_name = item[0][0]
            first_name = item[0][1]
            Controller.stell_info_formatted.append(f'{nStellEmp} {last_name}, {first_name}')
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
    def update_resturlaub(self, login_info):
        holidelta = 0
        
        #get starting vacation days
        Model.get_days_left(self, login_info)
        days_left_row = Model.cursor.fetchone()
        total_days = days_left_row[0]

        #get holidays
        Controller.get_holidays(self)

        #get requests
        Model.get_holidates(self, login_info)
        holidates = Model.cursor.fetchall()
        
        #iterate through dates requested off
        for item in holidates:
            start_str = item[0]
            end_str = item[1]
            self.delta = end_str - start_str
            days = [start_str + timedelta(days = i) for i in range(self.delta.days + 1)]
            Wochenende = set([5, 6])
            days_to_delete = []
            
            #iterate through list of days requested off, and remove those that are holidays and weekends
            for i in days:
                if i.weekday() in Wochenende:
                    days_to_delete.append(i)
                elif i.strftime('%Y.' + '%m.' + '%d') in Controller.list_of_holiday_dates:
                    days_to_delete.append(i)
            for day in days_to_delete:
                days.remove(day)
            time_delta = len(days)
            holidelta = holidelta + time_delta
        #calc remaining days left
        Controller.days_left = total_days - holidelta

    
    #update button in table
    def update(self, updated_info):
        try:
            Model.update_request(self, updated_info)
            Controller.error_window(self, 'Update Successful\n\nPlease note that alterations to the stellvertreter will not be recorded.', 'info', 3000)
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Invalid date format\n\n{error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    # ---- loginbox

    # ---- request_window

    #submit new request
    stellvertreter_values = []
    stellvertreter_info = []
    def get_stellvertreter_number(self, stellvertreter_last_name):
        Model.get_stellvertreter_info(self, stellvertreter_last_name)
        stellvertreter_name_and_number = Model.cursor.fetchall()
        if len(stellvertreter_name_and_number) > 1:
                for item in stellvertreter_name_and_number:
                    Controller.stellvertreter_info.append(item)
                    last_name = item[0]
                    first_name = item[1]
                    stell_number = item[2]
                    Controller.stellvertreter_values.append(f'{last_name}, {first_name} {stell_number}')
        elif len(stellvertreter_name_and_number) == 0:
            Controller.error_window(self, 'Please enter a valid employee name.')
        else:
            Controller.stellvertreter_info.append(stellvertreter_name_and_number[0])
        
       
    def sub_new_info(self, new_info):
        try:
            Model.fetch_name(self, new_info[2])
            first_and_last_names = Model.cursor.fetchall()
            data = tuple(new_info) + tuple(first_and_last_names[0])
            Model.submit_request(self, data)
            Controller.error_window(self, 'Your submission was recorded!', 'info')
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Formatting Error\n\n{error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'Connection Error\n\n{error}', 'error')

    # ---- request_window

    # ---- manager_view

    #load all requests in table
    fetched_reqs = []
    def search_all(self):
        try:
            Model.all_search(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by employee, also used in the loginbox
    def search_emp(self, nEmployee):
        try:
            Model.emp_search(self, nEmployee)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #search by new
    def get_unseen(self):
        try:
            Model.get_unseen(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by bestätigt
    def get_green(self):
        try:
            Model.get_by_green(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by geplant
    def get_yellow(self):
        try:
            Model.get_by_yellow(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #search by denied
    def get_red(self):
        try:
            Model.get_by_red(self)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')
    
    #search by name
    def get_by_name(self, sLastName):
        try:
            Model.get_by_name(self, sLastName)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            Controller.errow_window(self, f'{error}', 'error')

    #update button in table
    def man_update(self, man_info):
        try:
            Model.man_update(self, man_info)
            Controller.error_window(self, 'Update Successful', 'info')
        except pyodbc.DataError as error:
            Controller.error_window(self, f'Incorrect Formatting \n\nError: {error}', 'error')
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #delete button in table
    def delete(self, xnRequest):
        try:
            Model.delete_request(self, xnRequest)
        except pyodbc.Error as error:
            Controller.error_window(self, f'{error}', 'error')

    #mark as seen button in table
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
    ProduktionsGruppe = {0:'WISSENTRÄGER', 1:'PRODUKTIONSGRUPPE 1', 2:'PRODUKTIONSGRUPPE 2', 
                     3:'PRODUKTIONSGRUPPE 3', 4:'PRODUKTIONSGRUPPE 4', 5:'PRODUKTIONSUNTERSTÜTZUNG',
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
    login_empnum = []
    manager_empnums = [905]   

    #starts everything related to schedule building
    
    def create_table(self):
        Controller.get_emp_list(self)
        Controller.get_requests(self)
        Controller.get_dates_for_headers(self)
        Controller.input_default_data(self)
        Controller.edit_data(self)
   
    #find production group of user
    def get_group_from_empnum(self, empnum):
        Controller.selected_group.clear()
        Model.get_group_from_empnum(self, empnum)
        pyodbc_row = Model.cursor.fetchall()
        if (str(pyodbc_row)[2]) == 'N':
            Controller.selected_group.append(6)
            Controller.login_empnum.clear()
        else:
            Controller.selected_group.append(int(str(pyodbc_row)[2]))
            Controller.login_empnum.clear()

    #populates the employee column
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
        #if user is a manager, shows all production groups
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
        #formatting
        for item in Controller.list_of_emp_info:
                if item[1] is not None:
                    emp_last_name = item[0]
                    emp_first_name = item[1]
                    emp_number = item[2]
                    Controller.rows.append('{}, {} {}'.format(emp_last_name, emp_first_name, emp_number)) 
                if item[1] is None:
                    Controller.rows.append(item[0])
    
    #needed for finding days between start and end date
    def date_range(self, start, end):
        delta = end - start
        days = [start + timedelta(days = i) for i in range(delta.days + 1)]
        return days

    #formats requests from the sql table into a request dictionary from the selected production group
    def get_requests(self):
        Model.get_requests(self)
        Controller.request_list_raw = Model.cursor.fetchall()
        for item in Controller.request_list_raw:
            selected_employee = []
            request_number = item[0]
            emp_last_name = item[1]
            emp_first_name = item[2]
            emp_number = item[5]
            date_start = item[3]
            date_end = item[4]
            status = item[7]
            stell_num = item[8]
            stell_status = item[9]
            selected_employee.append('{}, {} {}'.format(emp_last_name, emp_first_name, emp_number))
            if stell_num is not None and stell_num != 0:
                Model.get_stellvertreter_name(self, stell_num)
                raw_stellvertreter_info = Model.cursor.fetchall()
                stell_last_name = raw_stellvertreter_info[0][0]
                stell_first_name = raw_stellvertreter_info[0][1]
                #stell_number = raw_stellvertreter_info[0][2]
                stellvertreter_info = '{}, {} {}'.format(stell_last_name, stell_first_name, stell_num)
            else:
                stellvertreter_info = None         
            if selected_employee[0] in Controller.rows:
                        Controller.request_dictionary[request_number] = [item[3], date_start.strftime('%Y.' + '%m.' + '%d')]
                        daterangelist = Controller.date_range(self, date_start, date_end)
                        for i in range(0, len(daterangelist)):
                            Controller.request_dictionary[request_number + (i * .01)] = [selected_employee, 
                                                daterangelist[i].strftime('%Y.' + '%m.' + '%d'), status, 
                                                stellvertreter_info, stell_status]

    #format holidays from sql
    def get_holidays(self):
        Model.get_holidays(self)
        holidays = Model.cursor.fetchall()
        for holiday in holidays:
            holiday_date = holiday[1]
            Controller.list_of_holiday_dates.append(holiday_date.strftime('%Y.' + '%m.' + '%d'))
    
    #populates row of dates with every day of the month
    def get_dates_for_headers(self):    
        Controller.headers.clear()
        number_of_days = calendar.monthrange(Controller.selected_year[0], Controller.selected_month[0])[1]
        first_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], 1)
        last_date = datetime.date(Controller.selected_year[0], Controller.selected_month[0], number_of_days)
        
        delta = last_date - first_date
        for i in range(delta.days + 1):
            day = (first_date + datetime.timedelta(days = i))
            Controller.headers.append(day.strftime('%a %d'))

    #fills table with weekends, alle gruppe borders, and spaces for 'empty' celss
    def input_default_data(self):
        Controller.get_holidays(self)
        Controller.data_values.clear()    
        for ii in range(0, len(Controller.list_of_emp_info)):
            data_list = []
            for i in range(0, len(Controller.headers)):
                Wochenende = set([5, 6])
                if Controller.list_of_emp_info[ii][1] is None:
                    data_list.append('--------------')
                elif datetime.datetime(int(Controller.selected_year[0]), \
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

    #takes all requests in a selected gorup, month, and year, and populates the table with requests and stellvertreter status indicators
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
                            data_list[int(dayentered) - 1] = f'{employee_info}' 
                        elif stell_status == 0:
                            data_list[int(dayentered) - 1] = f'*{employee_info}'
                        data_tuple = tuple(data_list)
                        Controller.data_values[nameindex] = data_tuple
    # ---- schedule
    
    # ---- popup handler
    def error_window(self, message, type = 'info', timeout = 2000):
        error_window = tk.Tk()
        error_window.withdraw()
        error_window.after(timeout, error_window.destroy)
        if type == 'info':
            messagebox.showinfo('Info', message, master = error_window)
        elif type == 'error':
            messagebox.showerror('Error', message, master = error_window)
