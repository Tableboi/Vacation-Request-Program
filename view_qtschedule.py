#The view represents the GUI, which interact with the end
#user. It represents the model's data to the user.
import tkinter as tk
from tkinter import Toplevel, ttk
import tkinter.font
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk
import datetime
from datetime import timedelta
import re

from calendar import month
from msilib.schema import ComboBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from controller import Controller

class loginbox(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        pad_options = {'padx' : 5, 'pady' : 5}
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.top_frame = ttk.Frame(self, padding = 5)
        self.top_frame.pack(side = 'top', fill = 'x')

        # Create an object of tkinter ImageTk
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.top_frame, image = self.new_img)
        #self.label.pack(side = 'right')

        #setting the font types
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 14, weight = "bold", underline = 1)
        
        subheader_font = tkinter.font.Font(\
            family = "Helvertica", size = 12, weight = "normal", underline = 0)

        self.F1 = ttk.Frame(self.top_frame, relief = 'groove', \
            borderwidth = 2, padding = 5)
        self.F1.pack(side = 'left', pady = 20)

        self.label = ttk.Label(self.F1, text = "Einloggen")
        self.label.grid(column = 1, row = 0, **pad_options)
        self.label.configure(font = header_font)
        
        self.L1 = ttk.Label(self.F1, text = "Personal Nummer:")
        self.L1.grid(column = 0, row = 1, sticky = "E", **pad_options)

        logininfo = tk.StringVar()
        self.E1 = ttk.Entry(self.F1, textvariable = logininfo)
        self.E1.grid(column = 1, row = 1, sticky = "W", **pad_options)
        self.E1.focus()
        self.E1.bind('<Return>', self.submit)

        self.B1 = ttk.Button(self.F1, text = "Submit")
        self.B1.bind('<Button-1>', self.submit)
        self.B1.grid(column = 2, row = 1, sticky = "", **pad_options)

        self.vert_frame_cont = ttk.Labelframe(self, text = 'Current Requests', \
            labelanchor = 'n', borderwidth = 4)
        self.vert_frame = VerticalScrolledFrame(self.vert_frame_cont)
        self.vert_frame.pack(fill = 'x')

        self.vert_frame2_cont = ttk.Labelframe(self, text = 'Pending Stellvertreter Status', \
            labelanchor = 'n', borderwidth = 4)
        self.vert_frame2 = VerticalScrolledFrame(self.vert_frame2_cont)
        self.vert_frame2.pack(fill = 'x')

        self.F2 = ttk.Frame(self.top_frame, relief = 'groove', \
            borderwidth = 2, padding = 5)
        self.F2.pack(pady = 20)

        self.B3 = ttk.Button(self.F2, text = "New Request", \
                command = lambda : controller.show_frame(request_window), \
                    state = 'disabled')
        self.B3.grid(column = 0, row = 0, rowspan = 2, **pad_options)
   
        self.B4 = ttk.Button(self.F2, text = "Manager View", \
                command = lambda : controller.show_frame(manager_view), \
                    state = 'disabled')
        self.B4.grid(column = 1, row = 0, rowspan = 2, **pad_options)

        self.B5 = ttk.Button(self.F2, text = 'Schedule', \
                command = lambda : manager_view.open_schedule(self))
        self.B5.grid(column = 3, row = 0, rowspan = 2, **pad_options)
                
        self.Ltage = ttk.Label(self.F2, text = 'Resturlaub:')
        self.Ltage.configure(font = subheader_font)
        self.Ltage.grid(column = 2, row = 0, **pad_options)

        self.Etage_val = tk.IntVar()
        self.Etage = ttk.Entry(self.F2, textvariable = self.Etage_val, \
            justify = 'center', width = 10)
        self.Etage.grid(column = 2, row = 1, **pad_options)

    def submit(self, event):
        #need a global variable here so other classes can easily access it
        global login_info
        login_info = self.E1.get()

        #reset button states
        self.B3.configure(state = 'disable')
        self.B4.configure(state = 'disable')

        try:
            Controller.login(login_info)
            #this is the employee number validator, to check if
            # the user is a manager
            if int(login_info) == 905:
                loginbox.enable_allbuttons(self)
            else:
                loginbox.enable_empbuttons(self)
        except TypeError as error:
            messagebox.showerror('Error', f'Invalid Personalnummer\n\nError: {error}' )
            return

        Controller.get_days_left(login_info)

        self.Etage.config(state = 'enabled')
        self.Etage.delete(0, 'end')
        self.Etage.insert(0, f'{Controller.days_left} Tage')
        self.Etage.config(state = 'disabled')

        self.search_by_employee()

        #reveal vert window
        self.vert_frame_cont.pack(fill = 'x')

        self.start_stell_stuff()

        self.vert_frame2_cont.pack(fill = 'x')
    
    def enable_empbuttons(self):
        self.B3.configure(state = 'enable')
    
    def enable_allbuttons(self):
        self.B3.configure(state = 'enable')
        self.B4.configure(state = 'enable')
    
    def search_by_employee(self, event = None):
        Controller.search_emp(self.E1.get())
        #validating if the input personalnummer has entries associated with it
        if not Controller.fetched_reqs:
            for widget in self.vert_frame.interior.winfo_children():
                widget.destroy()
            self.LE = ttk.Label(self.vert_frame.interior, text = \
                    'No requests associated with this number.')
            self.LE.grid(column = 0, row = 0)
        else:
            self.search_emp()
    
    def start_stell_stuff(self):
        Controller.get_stell()
        #validating if the anyone has the user as stellvertreter
        if not Controller.stell_reqs:
            for widget in self.vert_frame2.interior.winfo_children():
                widget.destroy()
            self.LE = ttk.Label(self.vert_frame2.interior, text = \
                    'You are not listed as Stellvertreter.')
            self.LE.grid(column = 0, row = 0)
        else:
            self.stell_stuff()
    
    def search_emp(self):        
        #lists necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.vert_frame.interior.winfo_children():
            widget.destroy()

        column_headers = {'borderwidth' : 1, 'relief' : 'flat', 'background' : 'white', 'foreground' : 'black'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)

        self.L1 = ttk.Label(self.vert_frame.interior, text = 'Antragsnummer', **column_headers)
        self.L1.config(font = column_font)
        self.L1.grid(column = 0, row = 0)

        self.L2 = ttk.Label(self.vert_frame.interior, text = 'Startdatum', **column_headers)
        self.L2.config(font = column_font)
        self.L2.grid(column = 1, row = 0)

        self.L3 = ttk.Label(self.vert_frame.interior, text = 'Endedatum', **column_headers)
        self.L3.config(font = column_font)
        self.L3.grid(column = 2, row = 0)

        self.L4 = ttk.Label(self.vert_frame.interior, text = 'Stellvertreter', **column_headers)
        self.L4.config(font = column_font)
        self.L4.grid(column = 3, row = 0)

        self.L5 = ttk.Label(self.vert_frame.interior, text = 'Grund', **column_headers)
        self.L5.config(font = column_font)
        self.L5.grid(column = 4, row = 0)

        self.L6 = ttk.Label(self.vert_frame.interior, text = 'Status', **column_headers)
        self.L6.config(font = column_font)
        self.L6.grid(column = 5, row = 0)
        
        #Controller.search_emp(int(login_info))
        row_len = len(Controller.fetched_reqs)

        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        button_list = []

        for i in range(0, row_len, 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            self.entry = Controller.fetched_reqs[i]
            
            #must use tk.Entry instead of ttk because background and foreground
            # colors are not changable with ttk
            antrags_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))

            start_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))
            
            stell_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))

            grund_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'ridge'))

            antrags_list[i].config(state = 'normal')
            antrags_list[i].insert(0, str(self.entry[0]))
            antrags_list[i].grid(row = i + 1, column = 0, **pad_options)
            antrags_list[i].config(state = 'readonly')

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 1, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 2, **pad_options)

            stell_list[i].insert(0, str(self.entry[3]))
            if int(self.entry[6]) == 0:
                stell_list[i].config(background = 'yellow')
            elif int(self.entry[6]) == 1:
                stell_list[i].config(background = '#90EE90')
            elif int(self.entry[6]) == 2:
                stell_list[i].config(background = 'red')
            stell_list[i].grid(row = i + 1, column = 3, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 4, **pad_options)

            status_list[i].insert(0, str(self.entry[5]))
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#90EE90')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = 'yellow')
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            def update_button(i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                new_reason = grund_list[i].get().strip()
                xnRequest = antrags_list[i].get().strip()

                if start_date or end_date:
                    if end_date == '':
                        end_date = start_date
                    updated = (start_date, end_date, new_reason, xnRequest, int(login_info))
                    Controller.update(updated)

            button_list.append(ttk.Button(self.vert_frame.interior, text = 'Update', width = 15, \
                command = lambda i=i : update_button(i)))
            button_list[i].grid(row = i + 1, column = 6, **pad_options)
    
    def stell_stuff(self):
        #lists necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.vert_frame2.interior.winfo_children():
            widget.destroy()

        column_headers = {'borderwidth' : 1, 'relief' : 'flat', 'background' : 'white', 'foreground' : 'black'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)

        self.L1 = ttk.Label(self.vert_frame2.interior, text = 'Antragsnummer', **column_headers)
        self.L1.config(font = column_font)
        self.L1.grid(column = 0, row = 0)

        self.L2 = ttk.Label(self.vert_frame2.interior, text = 'Startdatum', **column_headers)
        self.L2.config(font = column_font)
        self.L2.grid(column = 1, row = 0)

        self.L3 = ttk.Label(self.vert_frame2.interior, text = 'Endedatum', **column_headers)
        self.L3.config(font = column_font)
        self.L3.grid(column = 2, row = 0)

        self.L4 = ttk.Label(self.vert_frame2.interior, text = 'Antragssteller', **column_headers)
        self.L4.config(font = column_font)
        self.L4.grid(column = 3, row = 0)

        self.L5 = ttk.Label(self.vert_frame2.interior, text = 'Grund', **column_headers)
        self.L5.config(font = column_font)
        self.L5.grid(column = 4, row = 0)

        self.L6 = ttk.Label(self.vert_frame2.interior, text = 'Status', **column_headers)
        self.L6.config(font = column_font)
        self.L6.grid(column = 5, row = 0)
        
        #Controller.search_emp(int(login_info))
        row_len = len(Controller.stell_reqs)

        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        yesbutton_list = []
        nobutton_list = []

        for i in range(0, row_len, 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            self.entry = Controller.stell_reqs[i]
            
            #must use tk.Entry instead of ttk because background and foreground
            # colors are not changable with ttk
            antrags_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            start_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))
            
            stell_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            grund_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            antrags_list[i].insert(0, str(self.entry[0]))
            antrags_list[i].grid(row = i + 1, column = 0, **pad_options)

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 1, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 2, **pad_options)

            stell_list[i].insert(0, str(self.entry[3]))
            stell_list[i].grid(row = i + 1, column = 3, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 4, **pad_options)

            status_list[i].insert(0, str(self.entry[5]))
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#90EE90')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = 'yellow')
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            def stell_status_button(i, sStellStatus):
                xnRequest = antrags_list[i].get().strip()
                Controller.update_stell(sStellStatus, xnRequest)
                self.start_stell_stuff()

            yesbutton_list.append(ttk.Button(self.vert_frame2.interior, text = 'Confirm', width = 15, \
                command = lambda i=i : stell_status_button(i, 1)))
            yesbutton_list[i].grid(row = i + 1, column = 6, **pad_options)

            nobutton_list.append(ttk.Button(self.vert_frame2.interior, text = 'Deny', width = 15, \
                command = lambda i=i : stell_status_button(i, 2)))
            nobutton_list[i].grid(row = i + 1, column = 7, **pad_options)

            
class request_window(ttk.Frame):
    def __init__(self, parent, controller):

        ttk.Frame.__init__(self, parent)
        
        self.Main = ttk.Frame(self)

        frame_options = {'relief' : 'groove', 'borderwidth' : 2, 'padding' : 5}

        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 16, weight = "bold", underline = 1)

        self.title_label= ttk.Label(self.Main, text = 'Urlaubsantrag', font = header_font)
        self.title_label.grid(column = 0, row = 0, padx = 5, pady = 5)

        # Create an object of tkinter ImageTk
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.Main, image = self.new_img)
        #self.label.grid(column = 1, row = 0, padx = 5, pady = 5)

        # ----- Section 1
        # pack options for section 1
        s1options = {'padx' : 5, 'pady' : 5}

        self.section1 = ttk.Frame(self.Main, **frame_options)

        """self.L1 = ttk.Label(self.section1, text = "Personal-Nr")
        self.L1.pack(side = 'left', **s1options)
 
        self.nEmployee = ttk.Entry(self.section1)
        self.nEmployee.pack(side = 'left', **s1options)"""

        self.L2 = ttk.Label(self.section1, text = "Urlaub am/vom")
        self.L2.pack(side = 'left', **s1options)

        self.dDateStart = ttk.Entry(self.section1, foreground = 'grey')
        self.dDateStart.insert(0, 'YYYY-MM-DD')
        self.dDateStart.pack(side = 'left', **s1options)

        self.L3 = ttk.Label(self.section1, text = "bis einschl.")
        self.L3.pack(side = 'left', **s1options)

        self.dDateEnd = ttk.Entry(self.section1, foreground = 'grey')
        self.dDateEnd.insert(0, 'YYYY-MM-DD')
        self.dDateEnd.pack(side = 'left', **s1options)
         
        self.section1.grid(columnspan = 2, column = 0, row = 1, padx = 5, pady = 5, sticky = 'ns')
 
        # ----- Section 1
 

        # ----- Section 2
        # pack options for section 2
        s2options = {'padx' : 5, 'pady' : 5}

        self.section2 = ttk.Frame(self.Main, **frame_options)

        self.L4 = ttk.Label(self.section2, text = "Stellvertreter")
        self.L4.grid(column = 0, row = 0, **s2options)
       
        self.E4 = ttk.Entry(self.section2)
        self.E4.grid(column = 0, row = 1, **s2options)

        self.L5 = ttk.Label(self.section2, text = "Urlaubsgrund")
        self.L5.grid(column = 1, row = 0, **s2options)

        self.T1 = ttk.Entry(self.section2, width = 20)
        self.T1.grid(column = 1, row = 1, **s2options)

        self.section2.grid(columnspan = 2, column = 0, row = 2, padx = 5, pady = 5, sticky = 'ns')
        # ----- Section 2

        self.bottom = ttk.Frame(self.Main)
        
        self.B1 = ttk.Button(self.bottom, text = "Submit", \
            command = lambda : [request_window.submit(self), request_window.update_nDaysLeft(self)])
        self.B1.pack(padx = 5, pady = 5, side = 'right')
        
        self.B2 = ttk.Button(self.bottom, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.B2.pack(padx = 5, pady = 5, side = 'left')

        self.bottom.grid(columnspan = 2, column = 0, row = 4, sticky = 'ns')
 
        self.Main.pack(fill = 'y')

    def update_nDaysLeft(self):
        start_str = self.dDateStart.get().strip()
        end_str = self.dDateEnd.get().strip()
        if end_str == '' or 'YYYY-MM-DD':
            end_str = start_str

        try:
            start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
            self.delta = (end_date - start_date).days
            Controller.get_days_left(login_info)
            self.nDaysLeft = Controller.days_left - (self.delta + 1)

            Controller.reduce_days(self.nDaysLeft)

            Controller.get_days_left(login_info)

            messagebox.showinfo(title = None, message = f'Resturlaub : {Controller.days_left} Tage')
        
        except ValueError as error:
            messagebox.showerror('Error', f'Date must be in YYYY-MM-DD format.\n\nError: {error}')

    def submit(self):
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '' or 'YYYY-MM-DD':
                end_date = start_date
            data = (start_date, end_date, int(login_info), self.T1.get(), "geplant", self.E4.get())

        if type(self.T1.get()) != str:
            messagebox.showerror('Error', 'Invalid Grund Format')
        if type(self.E4.get()) != str:
            messagebox.showerror('Error', 'Invalid Stellvertreter Format')
        else:
            pass

        Controller.sub_new_info(data)

class manager_view(ttk.Frame):
    def __init__(self, parent, controller):

        ttk.Frame.__init__(self, parent)

        #setting the font for headers
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 16, weight = "bold", underline = 1)
        
        #top frame for header widgets
        self.Headerframe = ttk.Frame(self)
        self.Headerframe.pack(side = 'top', fill = 'x')
        self.Headerframe.configure(relief = 'groove', \
            borderwidth = 2, padding = 5)
        self.Headerframe.columnconfigure(6, weight = 2)

        # Create an object of tkinter ImageTk
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.Headerframe, image = self.new_img)
        #self.label.grid(rowspan = 2, column = 7, row = 0, \
        #    padx = 10, pady = 20, sticky = 'e')

        self.label = ttk.Label(self.Headerframe, text = "Manager Request Search")
        self.label.configure(font = header_font)
        self.label.grid( columnspan = 2, column = 0, row = 0, padx = 10, pady = 20)

        self.L0 = ttk.Label(self.Headerframe, text = 'Personalnummer:')
        self.L0.grid(column = 0, row = 1)

        self.E1_var = tk.StringVar()
        self.E1 = ttk.Entry(self.Headerframe, textvariable = self.E1_var)
        self.E1.focus()
        self.E1.bind('<Return>', self.search_by_employee)
        self.E1.grid(column = 1, row = 1)

        self.B1 = ttk.Button(self.Headerframe, text = "Search", \
            command = lambda : [manager_view.search_by_employee(self), self.F1.canvas.yview_moveto(0)])
        self.B1.grid(column = 2, row = 1)

        self.Bhf2 = ttk.Button(self.Headerframe, text = "Load All", \
            command = lambda : [manager_view.all_view(self), self.F1.canvas.yview_moveto(0)])
        self.Bhf2.grid(column = 3, row = 1)

        self.Bhf4 = ttk.Button(self.Headerframe, text = 'Load New', \
            command = lambda : [manager_view.unseen_view(self), self.F1.canvas.yview_moveto(0)])
        self.Bhf4.grid(column = 4, row = 1)
        
        self.Bhf3 = ttk.Button(self.Headerframe, text = "View Schedule", \
            command = lambda : manager_view.open_schedule(self))
        self.Bhf3.grid(column = 5, row = 1, padx = 10, pady = 10)
        
        self.Bhf4 = ttk.Button(self.Headerframe, text = 'Return', \
            command = lambda : controller.show_frame(loginbox))
        self.Bhf4.grid(column = 6, row = 1, padx = 10, pady = 10)

        #entry box master frame
        self.F1 = VerticalScrolledFrame(self)
        self.F1.pack(fill = 'both', expand = True)

    def open_schedule(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        schedule = Ui_Form()
        schedule.setupUi(Form, empnum = int(login_info))
        Form.show()
        app.exec_()

    def all_view(self):
        Controller.search_all()
        row_len = len(Controller.fetched_reqs)
        #list necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        column_headers = {'borderwidth' : 1, 'relief' : 'flat', 'background' : 'white', 'foreground' : 'black'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)
        
        self.Nu = ttk.Label(self.F1.interior, text = 'Antragsnummer', **column_headers)
        self.Nu.config(font = column_font)
        self.Nu.grid(column = 0, row = 0)
        
        self.L1 = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.L1.config(font = column_font)
        self.L1.grid(column = 1, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.L2.config(font = column_font)
        self.L2.grid(column = 2, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Stellvertreter', **column_headers)
        self.L3.config(font = column_font)
        self.L3.grid(column = 3, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.L4.config(font = column_font)
        self.L4.grid(column = 4, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.L5.config(font = column_font)
        self.L5.grid(column = 5, row = 0)

        self.L6 = ttk.Label(self.F1.interior, text = 'Personalnummer', **column_headers)
        self.L6.config(font = column_font)
        self.L6.grid(column = 6, row = 0)

        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        emp_list = []
        button_list = []
        delete_button_list = []

        for i in range(0, row_len, 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            self.entry = Controller.fetched_reqs[i]

            antrags_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            start_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))
            
            stell_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            grund_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            emp_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            antrags_list[i].insert(0, str(self.entry[0]))
            antrags_list[i].grid(row = i + 1, column = 0, **pad_options)

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 1, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 2, **pad_options)

            stell_list[i].insert(0, str(self.entry[3]))
            if int(self.entry[7]) == 0:
                stell_list[i].config(background = 'yellow')
            elif int(self.entry[7]) == 1:
                stell_list[i].config(background = '#90EE90')
            elif int(self.entry[7]) == 2:
                stell_list[i].config(background = 'red')
            stell_list[i].grid(row = i + 1, column = 3, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 4, **pad_options)

            status_list[i].insert(0, str(self.entry[5]))
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#90EE90')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = 'yellow')
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            emp_list[i].insert(0, str(self.entry[6]))
            emp_list[i].grid(row = i + 1, column = 6)

            def update_button(i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                new_reason = grund_list[i].get().strip()
                sStatus = status_list[i].get().strip()
                sStellvertreter = stell_list[i].get().strip()
                xnRequest = antrags_list[i].get().strip()

                if start_date or end_date:
                    if end_date == '':
                        end_date = start_date
                    updated = (start_date, end_date, new_reason, sStatus, sStellvertreter, xnRequest)
                    Controller.man_update(updated)

            button_list.append(ttk.Button(self.F1.interior, text = 'Update', width = 10, \
                command = lambda i=i : update_button(i)))
            button_list[i].grid(row = i + 1, column = 7, **pad_options)

            def delete_button(i):
                Controller.delete(int(antrags_list[i].get()))
                self.all_view()
            
            delete_button_list.append(ttk.Button(self.F1.interior, text = 'Delete', \
                width = 10, command = lambda i=i : delete_button(i)))
            delete_button_list[i].grid(row = i + 1, column = 8, **pad_options)
    
    def unseen_view(self):
        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()
        
        Controller.get_unseen()

        if not Controller.fetched_reqs:
            messagebox.showinfo(title = 'Error', message = 'No new requests')
            return
        else:
            pass

        row_len = len(Controller.fetched_reqs)
        #list necessary for entries
        self.entries = []

        column_headers = {'borderwidth' : 1, 'relief' : 'flat', 'background' : 'white', 'foreground' : 'black'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)
        
        self.Nu = ttk.Label(self.F1.interior, text = 'Antragsnummer', **column_headers)
        self.Nu.config(font = column_font)
        self.Nu.grid(column = 0, row = 0)
        
        self.L1 = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.L1.config(font = column_font)
        self.L1.grid(column = 1, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.L2.config(font = column_font)
        self.L2.grid(column = 2, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Stellvertreter', **column_headers)
        self.L3.config(font = column_font)
        self.L3.grid(column = 3, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.L4.config(font = column_font)
        self.L4.grid(column = 4, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.L5.config(font = column_font)
        self.L5.grid(column = 5, row = 0)

        self.L6 = ttk.Label(self.F1.interior, text = 'Personalnummer', **column_headers)
        self.L6.config(font = column_font)
        self.L6.grid(column = 6, row = 0)

        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        emp_list = []
        button_list = []
        mark_seen_button_list = []

        for i in range(0, row_len, 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            self.entry = Controller.fetched_reqs[i]

            antrags_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            start_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))
            
            stell_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            grund_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            emp_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            antrags_list[i].insert(0, str(self.entry[0]))
            antrags_list[i].grid(row = i + 1, column = 0, **pad_options)

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 1, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 2, **pad_options)

            stell_list[i].insert(0, str(self.entry[3]))
            if int(self.entry[7]) == 0:
                stell_list[i].config(background = 'yellow')
            elif int(self.entry[7]) == 1:
                stell_list[i].config(background = '#90EE90')
            elif int(self.entry[7]) == 2:
                stell_list[i].config(background = 'red')
            stell_list[i].grid(row = i + 1, column = 3, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 4, **pad_options)

            status_list[i].insert(0, str(self.entry[5]))
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#90EE90')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = 'yellow')
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            emp_list[i].insert(0, str(self.entry[6]))
            emp_list[i].grid(row = i + 1, column = 6)

            def update_button(i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                new_reason = grund_list[i].get().strip()
                sStatus = status_list[i].get().strip()
                sStellvertreter = stell_list[i].get().strip()
                xnRequest = antrags_list[i].get().strip()

                if start_date or end_date:
                    if end_date == '':
                        end_date = start_date
                    updated = (start_date, end_date, new_reason, sStatus, sStellvertreter, xnRequest)
                    Controller.man_update(updated)

            button_list.append(ttk.Button(self.F1.interior, text = 'Update', width = 10, \
                command = lambda i=i : update_button(i)))
            button_list[i].grid(row = i + 1, column = 7, **pad_options)

            def mark_seen_button(i):
                Controller.set_seen(int(antrags_list[i].get()))
                self.unseen_view()
            
            mark_seen_button_list.append(ttk.Button(self.F1.interior, text = 'Mark as Seen', \
                width = 15, command = lambda i=i : mark_seen_button(i)))
            mark_seen_button_list[i].grid(row = i + 1, column = 8, **pad_options)
            


    def search_by_employee(self, event = None):
        try:
            Controller.search_emp(int(self.E1.get()))
            #validating if the input personalnummer has entries associated with it
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                messagebox.showerror('Error', 'No requests associated with this number.')
            else:
                self.specific_view()
        except ValueError as error:
            messagebox.showerror('Error', f'Invalid Personalnummer Format \n\nError: {error}')


    def specific_view(self):
        #list necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        column_headers = {'borderwidth' : 1, 'relief' : 'flat', 'background' : 'white', 'foreground' : 'black'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)
        
        self.L1 = ttk.Label(self.F1.interior, text = 'Antragsnummer', **column_headers)
        self.L1.config(font = column_font)
        self.L1.grid(column = 0, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.L2.config(font = column_font)
        self.L2.grid(column = 1, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.L3.config(font = column_font)
        self.L3.grid(column = 2, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Stellvertreter', **column_headers)
        self.L4.config(font = column_font)
        self.L4.grid(column = 3, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.L5.config(font = column_font)
        self.L5.grid(column = 4, row = 0)

        self.L6 = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.L6.config(font = column_font)
        self.L6.grid(column = 5, row = 0)

        row_len = len(Controller.fetched_reqs)

        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        button_list = []
        delete_button_list = []

        for i in range(0, row_len, 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            self.entry = Controller.fetched_reqs[i]

            antrags_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            start_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))
            
            stell_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            grund_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'ridge'))

            antrags_list[i].insert(0, str(self.entry[0]))
            antrags_list[i].grid(row = i + 1, column = 0, **pad_options)

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 1, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 2, **pad_options)

            stell_list[i].insert(0, str(self.entry[3]))
            if int(self.entry[6]) == 0:
                stell_list[i].config(background = 'yellow')
            elif int(self.entry[6]) == 1:
                stell_list[i].config(background = '#90EE90')
            elif int(self.entry[6]) == 2:
                stell_list[i].config(background = 'red')
            stell_list[i].grid(row = i + 1, column = 3, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 4, **pad_options)

            status_list[i].insert(0, str(self.entry[5]))
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#90EE90')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = 'yellow')
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            def update_button(i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                sStellvertreter = stell_list[i].get().strip()
                new_reason = grund_list[i].get().strip()
                xnRequest = antrags_list[i].get().strip()

                if start_date or end_date:
                    if end_date == '':
                        end_date = start_date
                    updated = (start_date, end_date, new_reason, sStellvertreter, xnRequest, int(login_info))
                    Controller.update(updated)

            button_list.append(ttk.Button(self.F1.interior, text = 'Update', width = 10, \
                command = lambda i=i : update_button(i)))
            button_list[i].grid(row = i + 1, column = 6, **pad_options)

            def delete_button(i):
                Controller.delete(int(antrags_list[i].get()))
                self.search_by_employee()
            
            delete_button_list.append(ttk.Button(self.F1.interior, text = 'Delete', \
                width = 10, command = lambda i=i : delete_button(i)))
            delete_button_list[i].grid(row = i + 1, column = 8, **pad_options)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        Controller.create_table()
    
    def data(self, index, role):
        #index gives location in the table for which info is currently being requested. .row() and .column()
        #role describes what kind of info the method should return on thi call. QtDisplayRole expects a str.
        if role == Qt.DisplayRole:
            #.row() indexes into the outer list
            #.column() indexes into the sub-list
            value = self._data[index.row()][index.column()]
            return value
            #if isinstance(value, datetime.datetime):
                #return value.strftime('%d-%m-%Y')
        if role == Qt.BackgroundRole:
            value = self._data[index.row()][index.column()]
            if value == 'Wochenende':
                return QtGui.QColor('light gray')
            if value == 'Feiertag':
                return QtGui.QColor('light blue')
            if value == 'geplant':
                return QtGui.QColor('yellow')
            if value == 'bestätigt':
                return QtGui.QColor('light green')
            if value == 'Stellvertreter':
                return QtGui.QColor('#dcd0ff')
            if value == 'Stellvertreter?':
                return QtGui.QColor('#ffb6c1')
            else:
                return value
            #return value #default anything else
        #if role == Qt.BackgroundRole:
            #return QtGui.QColor('gray')
         
    def rowCount(self, index):
        return len(Controller.list_of_emp_numbers)
        
    
    def columnCount(self, index = None):
        return len(Controller.headers)
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return Controller.headers[section]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return 'Employee {}'.format(Controller.list_of_emp_numbers[section])
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)
    
class Ui_Form(object):
    #def __init__(self):
        #Form.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    def setupUi(self, Form, empnum):
        Form.setObjectName("Form")
        Form.resize(917, 743)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 901, 721))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.comboBox_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_3)
        
        #inserting my code for my table from another file
        
        #connect comboboxes to methods
        self.comboBox.activated[str].connect(self.change_group) 
        self.comboBox_2.activated[str].connect(self.change_month)
        self.comboBox_3.activated[str].connect(self.change_year)
        
        #use empnum to bring up production group
        if empnum not in Controller.manager_empnums:
            Controller.get_group_from_empnum(empnum)
        if empnum in Controller.manager_empnums:
            Controller.selected_group.append(0)
          
        self.tableWidget = QtWidgets.QTableView(self.layoutWidget) 
        self.tableWidget.setObjectName("tableWidget")
        
        data = Controller.data_values
        self.model = TableModel(data) 
        self.verticalLayout.addWidget(self.tableWidget) 
        self.verticalLayout_2.addLayout(self.verticalLayout) 
        self.tableWidget.setModel(self.model) 
        for i in range(TableModel.columnCount(TableModel)):
            self.tableWidget.setColumnWidth(i, 80)
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'hello', QtCore.Qt.DisplayRole)
        
        
        self.retranslateUi(Form, empnum)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, empnum):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Schedule"))
        self.comboBox.setItemText(0, _translate("Form", "Wissenträger"))
        self.comboBox.setItemText(1, _translate("Form", "Produktions Gruppe 1"))
        self.comboBox.setItemText(2, _translate("Form", "Produktions Gruppe 2"))
        self.comboBox.setItemText(3, _translate("Form", "Produktions Gruppe 3"))
        self.comboBox.setItemText(4, _translate("Form", "Produktions Gruppe 4"))
        self.comboBox.setItemText(5, _translate("Form", "Produktionsunterstützung"))
        self.comboBox.setItemText(6, _translate("Form", "Keine Gruppe"))
        self.comboBox.setCurrentIndex(Controller.selected_group[0])
        self.comboBox_2.setItemText(0, _translate("Form", "Jan"))
        self.comboBox_2.setItemText(1, _translate("Form", "Feb"))
        self.comboBox_2.setItemText(2, _translate("Form", "Mar"))
        self.comboBox_2.setItemText(3, _translate("Form", "Apr"))
        self.comboBox_2.setItemText(4, _translate("Form", "May"))
        self.comboBox_2.setItemText(5, _translate("Form", "Jun"))
        self.comboBox_2.setItemText(6, _translate("Form", "Jul"))
        self.comboBox_2.setItemText(7, _translate("Form", "Aug"))
        self.comboBox_2.setItemText(8, _translate("Form", "Sep"))
        self.comboBox_2.setItemText(9, _translate("Form", "Oct"))
        self.comboBox_2.setItemText(10, _translate("Form", "Nov"))
        self.comboBox_2.setItemText(11, _translate("Form", "Dec"))
        self.comboBox_2.setCurrentIndex(Controller.selected_month[0] - 1)
        self.comboBox_3.setItemText(0, _translate("Form", str(Controller.years[0])))
        self.comboBox_3.setItemText(1, _translate("Form", str(Controller.years[1])))
        self.comboBox_3.setItemText(2, _translate("Form", str(Controller.years[2])))
        self.comboBox_3.setItemText(3, _translate("Form", str(Controller.years[3])))
        self.comboBox_3.setItemText(4, _translate("Form", str(Controller.years[4])))
        
        if empnum not in Controller.manager_empnums:
            self.comboBox.setEnabled(False)
        if empnum in Controller.manager_empnums:
            pass
        
    def change_group(self):
        group_selection = int(self.comboBox.currentIndex())
        data = Controller.data_values
        Controller.selected_group.clear()
        Controller.selected_group.append(group_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model) #needed to put table into frame
        #print('changing group')
         
    def change_month(self):
        month_selection = int(self.comboBox_2.currentIndex()) + 1
        data = Controller.data_values
        Controller.selected_month.clear()
        Controller.selected_month.append(month_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model) #needed to put table into frame
        #print('changing month')
        
    def change_year(self):
        year_selection = int(self.comboBox_3.currentText())
        #print(year_selection)
        data = Controller.data_values
        Controller.selected_year.clear()
        Controller.selected_year.append(year_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model)
        #print('changing year')

#The below frame is needed for the manager_view and employee_req_view
# scrollbar frames
class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        self.canvas.pack(side = 'left', fill = 'both', expand = True)
        vscrollbar.config(command=self.canvas.yview)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Reset the View
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

    def _on_mousewheel(self, event):
            self.canvas.yview_scroll(int(-1*(event.delta/100)), "units")

#below is for scrolling horizontally in the Schedule treeview
class HorizontalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        hscrollbar = ttk.Scrollbar(self, orient='horizontal')
        hscrollbar.pack(fill = 'y', side = 'bottom', expand = False)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           xscrollcommand=hscrollbar.set)
        self.canvas.pack(side = 'left', fill = 'both', expand = True)
        hscrollbar.config(command=self.canvas.xview)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Reset the View
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

    def _on_mousewheel(self, event):
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
