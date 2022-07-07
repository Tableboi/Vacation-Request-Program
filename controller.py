import pyodbc
import datetime
from datetime import timedelta
import re

from tkinter import messagebox

from models import Model

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
        try:
            Model.infofetch(login_info)
            user_info = Model.cursor.fetchone()
            Controller.user_id = user_info[2]
            Controller.user_name = user_info[1]
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')
    

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
    
    # ---- loginbox

    # ---- request_window

    #submit
    def sub_new_info(new_info):
        try:
            Model.submit_request(new_info)
            messagebox.showinfo("Success", "Your submission was recorded!")
        except pyodbc.DataError:
            messagebox.showerror('Error', 'Formatting Error')
        except pyodbc.DatabaseError as error:
            messagebox.showerror('Error', f'{error}')

    #update vacation days
    days_left = int()
    def get_days_left(login_info):
        Model.get_days_left(login_info)
        days_left_row = Model.cursor.fetchone()
        Controller.days_left = days_left_row[0]
    
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

    # ---- employee_req_view

    #search by employee, see search_emp in the manager_view section above

    #search by antragsnummer, see search in the manager_view section above

    #update
    def update(updated_info):
        try:
            Model.update_request(updated_info)
        except pyodbc.DataError:
            messagebox.showerror('Error', 'Invalid date format')
        except pyodbc.Error as error:
            messagebox.showerror('Error', f'{error}')

    # ---- employee_req_view

    # ---- schedule

    #initialization list
    ProduktionsGruppe = {0:'Wissenträger', 1:'Produktions Gruppe 1', 2:'Produktions Gruppe 2', 
                     3:'Produktions Gruppe 3', 4:'Produktions Gruppe 4', 5:'Produktionsunterstützung',
                     6: 'Keine Gruppe'}
        
    months = {0:'Januar', 1:'Februar', 2:'März', 3:'April', 4:'Mai', 5:'Juni', 
        6:'Juli', 7:'August', 8:'September', 9:'Oktober', 10:'November', 11:'Dezember'}
    
    years = {0:current_year, 1:current_year + 1, 2: current_year + 2, 3: current_year + 3, 
                 4:current_year + 4, 5:current_year + 5}

    number_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    list_of_number_lists = []
    list_of_holiday_dates = []
    request_list_raw = []
    request_dictionary = {}

    #methods
    def get_holidays():
        Model.get_holidays()
        holidays = Model.cursor.fetchall()
        for holiday in holidays:
            holiday_date = holiday[1]
            Controller.list_of_holiday_dates.append(holiday_date.strftime('%Y.' + '%m.' + '%d'))
    
    def get_emp_list():
        for i in range(0, 6, 1):
            Model.get_emp_list(i)
            column_list = Model.cursor.fetchall()
            column_list.sort()
            column_list.insert(0, 'Date')
            Controller.list_of_number_lists.append(column_list)

            #format emp numbers
            for i in range(1, len(column_list)):
                item = str(column_list[i])
                item = re.sub(r'[(,)]', '', item)
                new_item = item.replace('""',"")
                column_list.remove(column_list[i])
                column_list.insert(i, int(new_item[0:-1]))

    def get_no_group_list():
        Model.get_no_group_list()
        column_list = Model.cursor.fetchall()
        column_list.sort()
        column_list.insert(0, 'Date')
        for i in range(1, len(column_list)):
            item = str(column_list[i])
            item = re.sub(r'[(,)]', '', item)
            new_item = item.replace('"', "")
            column_list.remove(column_list[i])
            column_list.insert(i, int(new_item[0:-1]))
        Controller.list_of_number_lists.append(column_list)
    
    def get_requests():
        Model.get_requests()
        Controller.request_list_raw = Model.cursor.fetchall()
        
        #necessary to make requests between start and end date
        def date_range(start, end):
            delta = end - start
            days = [start + timedelta(days = i) for i in range(delta.days + 1)]
            return days
        
        for item in Controller.request_list_raw:
            selected_employee_number = item [3]
            for numlist in Controller.list_of_number_lists:
                if selected_employee_number in numlist:
                    Controller.request_dictionary[item[0]] = [selected_employee_number, item[1].strftime('%Y.' + '%m.' + '%d')]
                    start_date = item[1]
                    end_date = item[2]
                    date_range_list = date_range(start_date, end_date)
                    for i in range(0, len(date_range_list)):
                        Controller.request_dictionary[item[0] + (i * .01)] = [selected_employee_number, \
                                                date_range_list[i].strftime('%Y.' + '%m.' + '%d'), item[5]]
                else:
                    pass

    # ---- schedule

    #dont know yet

    def reduce_days(nDaysLeft):
        Model.reduce_days(nDaysLeft, Controller.user_id)