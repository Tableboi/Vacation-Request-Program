import tkinter as tk
from tkinter import ttk

import sv_ttk

from views import loginbox, request_window, manager_view

#this is the main window and application
class App(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Urlaubsanträge')
        
        self.geometry('1050x600')
        
        sv_ttk.set_theme('dark')

        # creating a container
        base = ttk.Frame(self)
        base.pack(side = "top", fill = "both", expand = True)
  
        base.grid_rowconfigure(0, weight = 1)
        base.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (loginbox, request_window, manager_view):
  
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
