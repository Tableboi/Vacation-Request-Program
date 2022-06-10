import pandas as pd
import pyodbc
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import ttk

from views import loginbox, emp_choose, employee_req_view, request_window, manager_view

#this is the main window and application
class App(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        base = ttk.Frame(self)
        base.pack(side = "top", fill = "both", expand = True)
  
        base.grid_rowconfigure(0, weight = 1)
        base.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (loginbox, emp_choose, employee_req_view, request_window, manager_view):
  
            frame = F(base, self)
  
            # initializing frame of each object from
            # views respectively, iterating over a for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(loginbox)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Driver Code
app = App()
app.mainloop()