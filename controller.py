import pyodbc

from models import Model

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    #for the loginbox submit button
    def login(login_info):
        try:
            Model.infofetch(login_info)
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
        except pyodbc.Error as error:
            print(error)