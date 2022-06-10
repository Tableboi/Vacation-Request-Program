import pyodbc

from models import Model

class Controller:
    #Variables called by the views
    req_data = [] #this is for the employee_req_view
    user_id = int()
    fetched_reqs = []
    def __init__(self, model, view):
        self.model = model
        self.view = view

    #for the loginbox submit button
    def login(login_info):
        try:
            Model.infofetch(login_info)
            user_info = Model.cursor.fetchone()
            Controller.user_id = user_info[2]
        except pyodbc.Error as error:
            print(error)
    #for the request_window submit button
    def sub_new_info(new_info):
        try:
            Model.submit_request(new_info)
        except pyodbc.Error as error:
            print(error)
    
    #for the employee_req_view search button
    def search(xnRequest):
        try:
            Model.fetch_request(xnRequest)
            Controller.req_data = Model.cursor.fetchone()
        except pyodbc.Error as error:
            print(error)
    
    #for the employee_req_view update button
    def update(updated_info):
        try:
            Model.update_request(updated_info)
        except pyodbc.Error as error:
            print(error)
    
    #for the employee_req_view delete button
    def delete(xnRequest):
        try:
            Model.delete_request(xnRequest)
        except pyodbc.Error as error:
            print(error)
    
    #for the manager_view search by employee
    def search_emp(nEmployee):
        try:
            Model.emp_search(nEmployee)
            Controller.fetched_reqs = Model.cursor.fetchall()
        except pyodbc.Error as error:
            print(error)