#The view represents the GUI, which interact with the end
#user. It represents the model's data to the user.
import tkinter as tk
from tkinter import ttk, IntVar
import tkinter.font

from PIL import Image, ImageTk

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

import qdarktheme

from datetime import datetime
from controller import Controller

class loginbox(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        pad_options = {'padx' : 5, 'pady' : 5}
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        #Create a frame to contain top widgets
        self.top_frame = ttk.Frame(self, padding = 5)
        self.top_frame.pack(side = 'top', fill = 'x')

        
        # Create an object of tkinter ImageTk
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB_negativ.png'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.top_frame, image = self.new_img)
        #self.label.pack(side = 'right')
        # ---- logo

        #setting the font types
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 14, weight = "bold", underline = 1)
        subheader_font = tkinter.font.Font(\
            family = "Helvertica", size = 12, weight = "normal", underline = 0)

        #frame for login widgets
        self.F1 = ttk.Frame(self.top_frame, padding = 5)
        self.F1.pack(side = 'left', pady = 20)

        # ---- login widgets
        self.login_label = ttk.Label(self.F1, text = "Einloggen")
        self.login_label.grid(column = 1, row = 0, **pad_options)
        self.login_label.configure(font = header_font)
        
        self.pnummer_label = ttk.Label(self.F1, text = "Personal Nummer:")
        self.pnummer_label.grid(column = 0, row = 1, sticky = "E", **pad_options)

        logininfo = tk.StringVar()
        self.login_entry = ttk.Entry(self.F1, textvariable = logininfo)
        self.login_entry.grid(column = 1, row = 1, sticky = "W", **pad_options)
        self.login_entry.focus()
        self.login_entry.bind('<Return>', self.submit_click)

        self.login_button = ttk.Button(self.F1, text = "Submit")
        self.login_button.bind('<Button-1>', self.submit_click)
        self.login_button.grid(column = 2, row = 1, sticky = "", **pad_options)
        # ---- login widgets

        #frame for current request table
        self.vert_frame_cont = ttk.Labelframe(self, text = 'Current Requests', \
            labelanchor = 'n', borderwidth = 4)
        self.vert_frame = VerticalScrolledFrame(self.vert_frame_cont)
        self.vert_frame.pack(fill = 'x')

        #frame for pending stell request table
        self.vert_frame2_cont = ttk.Labelframe(self, text = 'Pending Stellvertreter Status', \
            labelanchor = 'n', borderwidth = 4)
        self.vert_frame2 = VerticalScrolledFrame(self.vert_frame2_cont)
        self.vert_frame2.pack(fill = 'x')

        #frame for buttons and resturlaub counter
        self.F2 = ttk.Frame(self.top_frame, padding = 5)
        self.F2.pack(pady = 20)

        # ---- resturlaub and button widgets
        self.tage_label = ttk.Label(self.F2, text = 'Resturlaub:')
        self.tage_label.configure(font = subheader_font)
        self.tage_label.grid(column = 0, row = 0, **pad_options)

        self.tage_val = tk.IntVar()
        self.tage_entry = ttk.Entry(self.F2, textvariable = self.tage_val, \
            justify = 'center', width = 10)
        self.tage_entry.grid(column = 0, row = 1, **pad_options)

        self.new_req_button = ttk.Button(self.F2, text = "New Request", \
                command = lambda : controller.show_frame(request_window), \
                    state = 'disabled')
        self.new_req_button.grid(column = 1, row = 0, rowspan = 2, **pad_options)

        self.schedule_button = ttk.Button(self.F2, text = 'Schedule', \
                command = lambda : manager_view.open_schedule(self), \
                    state = 'disabled')
        self.schedule_button.grid(column = 2, row = 0, rowspan = 2, **pad_options)
   
        self.man_view_button = ttk.Button(self.F2, text = "Manager View", \
                command = lambda : controller.show_frame(manager_view), \
                    state = 'disabled')
        self.man_view_button.grid(column = 3, row = 0, rowspan = 2, **pad_options)
        # ---- resturlaub and button widgets
        
    #on submit button click
    def submit_click(self, event):
        #need a global variable here so other classes can easily access it
        global login_info
        try:
            login_info = int(self.login_entry.get())
        except ValueError as error: #checks if login_info is an int
            Controller.error_window(self, f'Invalid Personalnummer Format\n\n{error}', type = 'error')
            for widget in self.vert_frame.interior.winfo_children():
                widget.destroy()
            for widget in self.vert_frame2.interior.winfo_children():
                widget.destroy()
            return

        #reset button states
        self.new_req_button.configure(state = 'disabled')
        self.schedule_button.configure(state = 'disabled')
        self.man_view_button.configure(state = 'disabled')

        #validate user info
        try:
            Controller.login(self, login_info)
            if login_info in Controller.manager_empnums: #checks if user is a manager
                loginbox.enable_manbuttons(self)
            else:
                loginbox.enable_buttons(self)
        except TypeError as error: #checks if personalnummer exists
            Controller.error_window(self, f'Invalid Personalnummer \n\n{error}', type = 'error')
            for widget in self.vert_frame.interior.winfo_children():
                widget.destroy()
            for widget in self.vert_frame2.interior.winfo_children():
                widget.destroy()
            return

        #updates resturlaub counter
        self.update_days_entry()

        #starts loading current request table
        self.search_by_employee()
        self.vert_frame_cont.pack(fill = 'x')

        #starts loading pending stell request table
        self.start_stell_stuff()
        self.vert_frame2_cont.pack(fill = 'x')
    
    #updates resturlaub method
    def update_days_entry(self):
        Controller.update_resturlaub(self, login_info)

        self.tage_entry.config(state = 'enabled')
        self.tage_entry.delete(0, 'end')
        self.tage_entry.insert(0, f'{Controller.days_left} Tage')
        self.tage_entry.config(state = 'disabled')
    
    #enables buttons to user
    def enable_buttons(self):
        self.new_req_button.configure(state = 'enabled')
        self.schedule_button.configure(state = 'enabled')
    
    #enables buttons to manager
    def enable_manbuttons(self):
        self.new_req_button.configure(state = 'enabled')
        self.schedule_button.configure(state = 'enabled')
        self.man_view_button.configure(state = 'enabled')
    
    #first checks personalnummer
    def search_by_employee(self, event = None):
        Controller.search_emp(self, self.login_entry.get())
        #checking if the input personalnummer has entries associated with it
        if not Controller.fetched_reqs:
            for widget in self.vert_frame.interior.winfo_children():
                widget.destroy()
            self.LE = ttk.Label(self.vert_frame.interior, text = \
                    'No requests associated with this number.')
            self.LE.grid(column = 0, row = 0)
        else:
            #if valid, load request table
            self.search_emp()
    
    #first checks for stell requests
    def start_stell_stuff(self):
        Controller.get_stell(self)
        #checking if the anyone has the user as stellvertreter
        if not Controller.stell_reqs:
            for widget in self.vert_frame2.interior.winfo_children():
                widget.destroy()
            self.LE = ttk.Label(self.vert_frame2.interior, text = \
                    'You are not listed as Stellvertreter.')
            self.LE.grid(column = 0, row = 0)
        else:
            #if requests exist, loads table
            self.stell_stuff()
    
    #builds current request table
    def search_emp(self):        
        #lists necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.vert_frame.interior.winfo_children():
            widget.destroy()

        # ---- column headers
        column_headers = {'borderwidth' : 1, 'relief' : 'flat'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)

        self.start_label = ttk.Label(self.vert_frame.interior, text = 'Startdatum', **column_headers)
        self.start_label.config(font = column_font)
        self.start_label.grid(column = 0, row = 0)

        self.end_label = ttk.Label(self.vert_frame.interior, text = 'Endedatum', **column_headers)
        self.end_label.config(font = column_font)
        self.end_label.grid(column = 1, row = 0)

        self.stell_label = ttk.Label(self.vert_frame.interior, text = 'Stellvertreter', **column_headers)
        self.stell_label.config(font = column_font)
        self.stell_label.grid(column = 2, row = 0)

        self.grund_label = ttk.Label(self.vert_frame.interior, text = 'Grund', **column_headers)
        self.grund_label.config(font = column_font)
        self.grund_label.grid(column = 3, row = 0)

        self.status_label = ttk.Label(self.vert_frame.interior, text = 'Status', **column_headers)
        self.status_label.config(font = column_font)
        self.status_label.grid(column = 4, row = 0)
        # ---- column headers
       
        #lists needed for iteration and indexing
        entry_list = []
        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        button_list = []

        #iterate through rows of fetched requests
        for i in range(0, len(Controller.fetched_reqs), 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            
            #picks one row of the fetched reqs
            entry_list.append(Controller.fetched_reqs[i])
            
            # ---- build widgets
            #must use tk.Entry instead of ttk because background and foreground
            # colors are not changable with ttk
            antrags_list.append(tk.StringVar())

            start_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'groove'))

            end_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'groove'))
            
            stell_list.append(tk.Entry(self.vert_frame.interior, width = 20, relief = 'groove'))

            grund_list.append(tk.Entry(self.vert_frame.interior, width = 15, relief = 'groove'))

            status_list.append(tk.Label(self.vert_frame.interior, width = 15))
            # ---- build widgets
            
            # ---- insert info into each widget by index
            antrags_list[i] = str(entry_list[i][0])

            start_list[i].insert(0, str(entry_list[i][1]))
            start_list[i].grid(row = i + 1, column = 0, **pad_options)

            end_list[i].insert(0, str(entry_list[i][2]))
            end_list[i].grid(row = i +1, column = 1, **pad_options)

            if entry_list[i][11]:
                Controller.get_stellvertreter_name(self, entry_list[i][11])
                stell_list[i].insert(0, Controller.stell_info_formatted[0])
            stell_list[i].config(foreground = 'black')
            #color widget based on its contents
            if int(entry_list[i][7]) == 0:
                stell_list[i].config(background = '#d4ef64')
            elif int(entry_list[i][7]) == 1:
                stell_list[i].config(background = '#64ef7f')
            elif int(entry_list[i][7]) == 2:
                stell_list[i].config(background = '#ef7f64')
            stell_list[i].grid(row = i + 1, column = 2, **pad_options)

            grund_list[i].insert(0, str(entry_list[i][4]))
            grund_list[i].grid(row = i + 1, column = 3, **pad_options)

            status_list[i].config(text =  f'{entry_list[i][5]}')
            #color widget based on its contents
            if str(entry_list[i][5]) == 'bestätigt':
                status_list[i].config(background = '#64ef7f', foreground = 'black')
            elif str(entry_list[i][5]) == 'geplant':
                status_list[i].config(background = '#d4ef64', foreground = 'black')
            elif str(entry_list[i][5]) == 'denied':
                status_list[i].config(background = '#ef7f64', foreground = 'white')
            status_list[i].grid(row = i + 1, column = 4, **pad_options)
            # ---- insert into into each widget by index
            
            # ---- table button widgets
            def update_button(self, i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                if start_date != str(entry_list[i][1]) or end_date != str(entry_list[i][2]):
                    nStellStatus = 0
                else:
                    nStellStatus = entry_list[i][7]
                
                new_reason = grund_list[i].get().strip()
                xnRequest = antrags_list[i]

                #checking for an unfilled start date
                if start_date == '' or start_date == 'YYYY-MM-DD':
                    Controller.error_window(self, 'Please enter a start date.', 'info', 2500)
                    return

                #checking for an unfilled end date
                if end_date == '':
                    end_date = start_date
                    
                #setting string dates to datetime
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError as error:
                    Controller.error_window(self, f'Please enter a valid date format.\n{error}', 'error')
                    return

                #followed by checking that the start date comes before end date
                if start_date > end_date:
                    Controller.error_window(self, 'Please enter an end date that is later than the start date.', 'info', 3000)
                    return
                
                updated = (start_date, end_date, new_reason, nStellStatus, xnRequest, int(login_info))
                Controller.update(self, updated)

                loginbox.update_days_entry(self)

                loginbox.search_by_employee(self)

            button_list.append(ttk.Button(self.vert_frame.interior, text = 'Update', width = 15, \
                command = lambda i=i : update_button(self, i)))
            button_list[i].grid(row = i + 1, column = 5, **pad_options)
            # ---- table button widgets
            
    #builds pending stell request table
    def stell_stuff(self):
        #lists necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.vert_frame2.interior.winfo_children():
            widget.destroy()

        # ---- column headers
        column_headers = {'borderwidth' : 1, 'relief' : 'flat'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)

        self.start_label = ttk.Label(self.vert_frame2.interior, text = 'Startdatum', **column_headers)
        self.start_label.config(font = column_font)
        self.start_label.grid(column = 0, row = 0)

        self.end_label = ttk.Label(self.vert_frame2.interior, text = 'Endedatum', **column_headers)
        self.end_label.config(font = column_font)
        self.end_label.grid(column = 1, row = 0)

        self.anstrell_label = ttk.Label(self.vert_frame2.interior, text = 'Antragssteller', **column_headers)
        self.anstrell_label.config(font = column_font)
        self.anstrell_label.grid(column = 2, row = 0)

        self.grund_label = ttk.Label(self.vert_frame2.interior, text = 'Grund', **column_headers)
        self.grund_label.config(font = column_font)
        self.grund_label.grid(column = 3, row = 0)

        self.status_label = ttk.Label(self.vert_frame2.interior, text = 'Status', **column_headers)
        self.status_label.config(font = column_font)
        self.status_label.grid(column = 4, row = 0)
        # ---- column headers
        
        #lists needed for iterating and indexing
        antrags_list = []
        start_list = []
        end_list = []
        antragssteller_list = []
        grund_list = []
        status_list = []
        yesbutton_list = []
        nobutton_list = []

        #iterate through rows of fetched requests
        for i in range(0, len(Controller.stell_reqs), 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            
            #picks one row of the fetched reqs
            self.entry = Controller.stell_reqs[i]
            
            # ---- build widgets
            #must use tk.Entry instead of ttk because background and foreground
            # colors are not changable with ttk
            antrags_list.append(tk.StringVar())

            start_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            end_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))
            
            antragssteller_list.append(tk.Entry(self.vert_frame2.interior, width = 20, relief = 'ridge'))

            grund_list.append(tk.Entry(self.vert_frame2.interior, width = 15, relief = 'ridge'))

            status_list.append(tk.Label(self.vert_frame2.interior, width = 15))

            antrags_list[i] = str(self.entry[0])
            # ---- build widgets
            
            # ---- insert info into each widget by index
            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 0, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 1, **pad_options)

            antragssteller_info = f'{self.entry[3]} {self.entry[10]}, {self.entry[9]}'
            antragssteller_list[i].insert(0, antragssteller_info)
            antragssteller_list[i].grid(row = i + 1, column = 2, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 3, **pad_options)

            status_list[i].config(text =  f'{self.entry[5]}')
            #color widget based on its contents
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#64ef7f', foreground = 'black')
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = '#d4ef64', foreground = 'black')
            elif str(self.entry[5]) == 'denied':
                status_list[i].config(background = '#ef7f64', foreground = 'white')
            status_list[i].grid(row = i + 1, column = 4, **pad_options)

            # ---- table button widgets
            def stell_status_button(i, sStellStatus):
                xnRequest = antrags_list[i]
                Controller.update_stell(self, sStellStatus, xnRequest)
                self.start_stell_stuff()

            yesbutton_list.append(ttk.Button(self.vert_frame2.interior, text = 'Confirm', width = 15, \
                command = lambda i=i : stell_status_button(i, 1)))
            yesbutton_list[i].grid(row = i + 1, column = 5, **pad_options)

            nobutton_list.append(ttk.Button(self.vert_frame2.interior, text = 'Deny', width = 15, \
                command = lambda i=i : stell_status_button(i, 2)))
            nobutton_list[i].grid(row = i + 1, column = 6, **pad_options)
            # ---- table button widgets
            
class request_window(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        #create the main frame
        self.Main = ttk.Frame(self)

        frame_options = {'relief' : 'groove', 'borderwidth' : 2, 'padding' : 5}

        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 16, weight = "bold", underline = 1)

        #title
        self.title_label= ttk.Label(self.Main, text = 'Urlaubsantrag', font = header_font)
        self.title_label.grid(column = 0, row = 0, padx = 5, pady = 5)

        # ---- logo
        # Create an object of tkinter ImageTk
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB_negativ.png'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.Main, image = self.new_img)
        #self.label.grid(column = 1, row = 0, padx = 5, pady = 5)
        # ---- logo
        
        # ----- section 1
        # pack options for section 1
        s1options = {'padx' : 5, 'pady' : 5}

        self.section1 = ttk.Frame(self.Main, **frame_options)

        self.dDateStart_label = ttk.Label(self.section1, text = "Urlaub am/vom")
        self.dDateStart_label.pack(side = 'left', **s1options)

        self.dDateStart = ttk.Entry(self.section1, foreground = 'grey')
        self.dDateStart.insert(0, 'YYYY-MM-DD')
        self.dDateStart.bind('<Return>', self.submit)
        self.dDateStart.pack(side = 'left', **s1options)

        self.dDateEnd_label = ttk.Label(self.section1, text = "bis einschl.")
        self.dDateEnd_label.pack(side = 'left', **s1options)

        self.dDateEnd = ttk.Entry(self.section1, foreground = 'grey')
        self.dDateEnd.insert(0, 'YYYY-MM-DD')
        self.dDateEnd.bind('<Return>', self.submit)
        self.dDateEnd.pack(side = 'left', **s1options)
         
        self.section1.grid(columnspan = 2, column = 0, row = 1, padx = 5, pady = 5, sticky = 'ns')
        # ----- section 1

        # ----- section 2
        # pack options for section 2
        s2options = {'padx' : 5, 'pady' : 5}

        self.section2 = ttk.Frame(self.Main, **frame_options)

        self.stell_label = ttk.Label(self.section2, text = "Stellvertreter")
        self.stell_label.grid(column = 0, row = 0, **s2options)
       
        self.stell_entry = ttk.Entry(self.section2)
        self.stell_entry.bind('<Return>', self.submit)
        self.stell_entry.grid(column = 0, row = 1, **s2options)

        self.Rvar1 = IntVar()
        self.Rvar1.set(1) #default value of self.Rvar1
        self.R1 = ttk.Radiobutton(self.section2, text = "Erholungsurlaub", variable = self.Rvar1, value = 1)
        self.R2 = ttk.Radiobutton(self.section2, text = "Sonderurlaub:", variable = self.Rvar1, value = 2)
        self.R1.grid(column = 1, row = 0, **s2options)
        self.R2.grid(column = 2, row = 0, **s2options)

        self.grund_label = ttk.Label(self.section2, text = "")
        self.grund_label.grid(column = 1, row = 1, **s2options)

        self.grund_entry = ttk.Entry(self.section2, width = 20)
        self.grund_entry.bind('<Return>', self.submit)
        self.grund_entry.grid(column = 2, row = 1, **s2options)

        self.section2.grid(columnspan = 2, column = 0, row = 2, padx = 5, pady = 5, sticky = 'ns')
        # ----- section 2

        #frame for the bottom buttons
        self.bottom = ttk.Frame(self.Main)
        
        # ---- buttons
        self.submit_button = ttk.Button(self.bottom, text = "Submit", \
            command = lambda : [request_window.submit(self), \
                Controller.update_resturlaub(self, login_info)])
        self.submit_button.pack(padx = 5, pady = 5, side = 'right')
        
        self.return_button = ttk.Button(self.bottom, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.return_button.pack(padx = 5, pady = 5, side = 'left')
        # ---- buttons
        
        self.bottom.grid(columnspan = 2, column = 0, row = 5, sticky = 'ns')
 
        self.Main.pack(fill = 'y')
        
        #------ Section for Stellvertreters with the same last name
        self.same_last_name = ttk.Frame(self.Main, **frame_options)
        
        self.stell_label = ttk.Label(self.same_last_name, text = "There are two employees with this last name. Which would you like to choose as your Stellvertreter?")
        self.stell_label.grid(column = 0, row = 0, **s2options)
        
        self.stellvertreter_selection = tk.StringVar()
        self.stellvertreter_combo = ttk.Combobox(self.same_last_name, \
            state = "readonly", textvariable = self.stellvertreter_selection)
        
        self.stellvertreter_combo.bind('<<ComboboxSelected>>', self.stell_combo_handler)
        self.stellvertreter_combo.grid(column = 0, row = 1)
        #------ Section for Stellvertreters with the same last name
    
    #on submit button press
    def submit(self):
        self.same_last_name.grid_remove()
        Controller.stellvertreter_values.clear()
        Controller.stellvertreter_info.clear()
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        
        #checking for an unfilled start date
        if start_date == '' or start_date == 'YYYY-MM-DD':
            Controller.error_window(self, 'Please enter a start date.', 'info', 2500)
            return

        #checking for an unfilled end date
        if end_date == '' or end_date == 'YYYY-MM-DD':
            end_date = start_date
            
        #setting string dates to datetime
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as error:
            Controller.error_window(self, f'Please enter a valid date format.\n\n{error}', 'error')
            return

        #checking that the start date is before or equal to end date
        if start_date > end_date:
            Controller.error_window(self, 'Please enter an end date that is later than the start date.', 'info', 3000)
            return

        #set radiobutton responses
        erholungsurlaub = 'Erholungsurlaub'
        sonderurlaub = self.grund_entry.get()

        #check radiobutton vals
        gründe = self.Rvar1.get()
        if gründe == 1:
            output = erholungsurlaub
        elif gründe == 2:
            output = sonderurlaub
        if output == '':
            Controller.error_window(self, 'Please enter a short Sonderurlaub description.', 'info')
            return
        elif gründe == 0:
            Controller.error_window(self, 'Please select vacation type.', 'info')
            return
        else:
            self.data = [start_date, end_date, int(login_info), output, "geplant", '', None]
            #check for stellvertreter entry
            if self.stell_entry.get() != '':
                Controller.get_stellvertreter_number(self, self.stell_entry.get())
                if len(Controller.stellvertreter_values) != 0:
                    self.stellvertreter_combo['values'] = Controller.stellvertreter_values
                    self.same_last_name.grid(column = 0, row = 4)
                elif len(Controller.stellvertreter_info) == 0:
                    ...
                else:
                    #add stellvertreter info to data
                    self.data[5] = Controller.stellvertreter_info[0][2]
                    self.data[6] = Controller.stellvertreter_info[0][0]
                    Controller.sub_new_info(self, self.data)    
            else:
                Controller.sub_new_info(self, self.data)

    #if there are multiple employees with the name entered for stellvertreter,
    #handles combobox for employee to choose which one they meant
    def stell_combo_handler(self, event = None):
        stell_index = self.stellvertreter_combo.current()
        self.data[5] = Controller.stellvertreter_info[stell_index][2]
        self.data[6] = Controller.stellvertreter_info[stell_index][0]
        Controller.sub_new_info(self, self.data)
        
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
        #self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB_negativ.png'
        #self.img = Image.open(self.path)
        #self.img.thumbnail((200,200))
        #self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        #self.label = ttk.Label(self.Headerframe, image = self.new_img)
        #self.label.grid(rowspan = 2, column = 7, row = 0, \
        #    padx = 10, pady = 20, sticky = 'e')

        # ---- control widgets
        self.title_label = ttk.Label(self.Headerframe, text = "Manager Request Search")
        self.title_label.configure(font = header_font)
        self.title_label.grid( columnspan = 2, column = 0, row = 0, padx = 10, pady = 20)

        self.search_label = ttk.Label(self.Headerframe, text = 'Search by:')
        self.search_label.grid(column = 0, row = 1)

        self.search_params = tk.StringVar()
        self.search_by = ttk.Combobox(self.Headerframe, textvariable = self.search_params)
        self.search_by['values'] = ('All', 'New', 'Status: bestätigt', 'Status: geplant', \
            'Status: denied')
        self.search_by.bind('<Return>', self.combo_handler)
        self.search_by.grid(column = 1, row = 1)
        # ---- control widgets
        
        # ---- buttons
        self.search_button = ttk.Button(self.Headerframe, text = "Search", \
            command = lambda : [manager_view.combo_handler(self), self.F1.canvas.yview_moveto(0)])
        self.search_button.grid(column = 2, row = 1)
        
        self.view_schedule_button = ttk.Button(self.Headerframe, text = "View Schedule", \
            command = lambda : manager_view.open_schedule(self))
        self.view_schedule_button.grid(column = 3, row = 1, padx = 10, pady = 10)
        
        self.return_button = ttk.Button(self.Headerframe, text = 'Return', \
            command = lambda : controller.show_frame(loginbox))
        self.return_button.grid(column = 4, row = 1, padx = 10, pady = 10)
        # ---- buttons
        
        #table frame
        self.F1 = VerticalScrolledFrame(self)
        self.F1.pack(fill = 'both', expand = True)

    #handle combobox options
    def combo_handler(self, event = None):
        combo_val = self.search_by.get()
        if combo_val == 'All':
            Controller.search_all(self)
            self.build_table()
        elif combo_val == 'New':
            Controller.get_unseen(self)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No new requests.', 'info')
            else:
                self.unseen_view()
        elif combo_val == 'Status: bestätigt':
            Controller.get_green(self)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No approved requests.', 'info')
            else:
                self.build_table()
        elif combo_val == 'Status: geplant':
            Controller.get_yellow(self)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No pending requests.', 'info')
            else:
                self.build_table()
        elif combo_val == 'Status: denied':
            Controller.get_red(self)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No denied requests.', 'info')
            else:
                self.build_table()
        elif combo_val.isdigit() == True:
            Controller.search_emp(self, combo_val)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No requests associated with this number.', 'info')
            else:
                self.build_table()
        else:
            Controller.get_by_name(self, combo_val)
            if not Controller.fetched_reqs:
                for widget in self.F1.interior.winfo_children():
                    widget.destroy()
                Controller.error_window(self, 'No requests associated with this name.', 'info')
            else:
                self.build_table()

    #generic table used for all combobox options other than New
    def build_table(self):
        #list necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        # ---- column headers
        column_headers = {'borderwidth' : 1, 'relief' : 'flat'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)
        
        self.start_label = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.start_label.config(font = column_font)
        self.start_label.grid(column = 0, row = 0)

        self.end_label = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.end_label.config(font = column_font)
        self.end_label.grid(column = 1, row = 0)

        self.stell_label = ttk.Label(self.F1.interior, text = 'Stellvertreter', **column_headers)
        self.stell_label.config(font = column_font)
        self.stell_label.grid(column = 2, row = 0)

        self.grund_label = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.grund_label.config(font = column_font)
        self.grund_label.grid(column = 3, row = 0)

        self.pnummer_label = ttk.Label(self.F1.interior, text = 'Employee', **column_headers)
        self.pnummer_label.config(font = column_font)
        self.pnummer_label.grid(column = 4, row = 0)

        self.status_label = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.status_label.config(font = column_font)
        self.status_label.grid(column = 5, row = 0)
        # ---- column headers
        
        #lists needed for iteration and indexing
        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        status_val_list = []
        emp_list = []
        button_list = []
        delete_button_list = []

        #iterate through rows of fetched requests
        for i in range(0, len(Controller.fetched_reqs), 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            
            #take data from one row of fetched reqs
            self.entry = Controller.fetched_reqs[i]

            # ---- build widgets
            #must use tkEntry instead of ttk because background and foreground 
            # colors are not changable with ttk
            antrags_list.append(tk.StringVar())

            start_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))

            end_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))
            
            stell_list.append(tk.Entry(self.F1.interior, width = 20, relief = 'groove'))

            grund_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))

            emp_list.append(tk.Entry(self.F1.interior, width = 20, relief = 'groove'))
            # ---- build widgets
            
            # ---- insert info into each widget by index
            antrags_list[i] = str(self.entry[0])

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 0, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 1, **pad_options)

            if self.entry[11]:
                Controller.get_stellvertreter_name(self, self.entry[11])
                stell_list[i].insert(0, Controller.stell_info_formatted[0])
            stell_list[i].config(foreground = 'black')
            #color widget based on its contents
            if int(self.entry[7]) == 0:
                stell_list[i].config(background = '#d4ef64')
            elif int(self.entry[7]) == 1:
                stell_list[i].config(background = '#64ef7f')
            elif int(self.entry[7]) == 2:
                stell_list[i].config(background = '#ef7f64')
            stell_list[i].grid(row = i + 1, column = 2, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 3, **pad_options)

            emp_list[i].insert(0, f'{str(self.entry[3])} {str(self.entry[10])}, {str(self.entry[9])}')
            emp_list[i].grid(row = i + 1, column = 4)
            # ---- insert info into each widget by index
            
            # ---- table button widgets
            #used for changing the approval status button
            def cycle_status_val(i):
                if status_val_list[i] == 2:
                    status_list[i].config(background = '#d4ef64', foreground = 'black', \
                        text = 'geplant')
                    status_val_list[i] = 1
                elif status_val_list[i] == 1:
                    status_list[i].config(background = '#ef7f64', foreground = 'white', \
                        text = 'denied')
                    status_val_list[i] = 0
                elif status_val_list[i] == 0:
                    status_list[i].config(background = '#64ef7f', foreground = 'black', \
                        text = 'bestätigt')
                    status_val_list[i] = 2

            status_list.append(tk.Button(self.F1.interior, width = 10, \
                command = lambda i=i :cycle_status_val(i)))
            status_val_list.append(int)
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#64ef7f', foreground = 'black', \
                    text = 'bestätigt')
                status_val_list[i] = 2
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = '#d4ef64', foreground = 'black', \
                    text = 'geplant')
                status_val_list[i] = 1
            elif str(self.entry [5]) =='denied':
                status_list[i].config(background = '#ef7f64', foreground = 'white', \
                    text = 'denied')
                status_val_list[i] = 0
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            def update_button(self, i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                new_reason = grund_list[i].get().strip()

                #getting status value from buttons
                if status_val_list[i] == 2:
                    sStatus = 'bestätigt'
                elif status_val_list[i] == 1:
                    sStatus = 'geplant'
                elif status_val_list[i] == 0:
                    sStatus = 'denied'

                sStellvertreter = stell_list[i].get().strip()
                xnRequest = antrags_list[i]

                #checking for an unfilled start date
                if start_date == '' or start_date == 'YYYY-MM-DD':
                    Controller.error_window(self, 'Please enter a start date.', 'info', 2500)
                    return

                #checking for an unfilled end date
                if end_date == '' or end_date == 'YYYY-MM-DD':
                    end_date = start_date

                #setting string dates to datetime
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError as error:
                    Controller.error_window(self, f'Please enter a valid date format.\n\n{error}', 'error')
                    return

                if start_date > end_date:
                    Controller.error_window(self, 'Please enter an end date that is later than the start date.', 'info', 3000)
                    return

                updated = (start_date, end_date, new_reason, sStatus, sStellvertreter, login_info, xnRequest)
                Controller.man_update(self, updated)

                manager_view.combo_handler(self)

            button_list.append(ttk.Button(self.F1.interior, text = 'Update', width = 10, \
                command = lambda i=i : update_button(self, i)))
            button_list[i].grid(row = i + 1, column = 6, **pad_options)

            def delete_button(self, i):
                Controller.delete(self, antrags_list[i])
                manager_view.combo_handler(self)
            
            delete_button_list.append(ttk.Button(self.F1.interior, text = 'Delete', \
                width = 10, command = lambda i=i : delete_button(self, i)))
            delete_button_list[i].grid(row = i + 1, column = 7, **pad_options)
            # ---- table button widgets
            
    #opens the full schedule view
    def open_schedule(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qdarktheme.load_stylesheet())
        Form = QtWidgets.QWidget()
        schedule = Ui_Form()
        Controller.login_empnum.clear()
        Controller.login_empnum.append(int(login_info))
        schedule.setupUi(Form, empnum = Controller.login_empnum[0])
        Form.show()
        app.exec_()
    
    #table for the New option
    def unseen_view(self):
        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        #list necessary for entries
        self.entries = []

        # ---- column headers
        column_headers = {'borderwidth' : 1, 'relief' : 'flat'}
        column_font = tkinter.font.Font(family = "Helvetica", size = 11)
        
        self.start_label = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.start_label.config(font = column_font)
        self.start_label.grid(column = 0, row = 0)

        self.end_label = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.end_label.config(font = column_font)
        self.end_label.grid(column = 1, row = 0)

        self.stell_label = ttk.Label(self.F1.interior, text = 'Stellvertreter', **column_headers)
        self.stell_label.config(font = column_font)
        self.stell_label.grid(column = 2, row = 0)

        self.grund_label = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.grund_label.config(font = column_font)
        self.grund_label.grid(column = 3, row = 0)

        self.status_label = ttk.Label(self.F1.interior, text = 'Employee', **column_headers)
        self.status_label.config(font = column_font)
        self.status_label.grid(column = 4, row = 0)

        self.pnummer_label = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.pnummer_label.config(font = column_font)
        self.pnummer_label.grid(column = 5, row = 0)
        # ---- column headers
        
        #lists needed for iteration and indexing
        antrags_list = []
        start_list = []
        end_list = []
        stell_list = []
        grund_list = []
        status_list = []
        status_val_list = []
        emp_list = []
        button_list = []
        mark_seen_button_list = []

        #iterate through rows of fetched requests
        for i in range(0, len(Controller.fetched_reqs), 1):
            pad_options = {'padx' : 5, 'pady' : 5}
            
            #pick one row of fetched requests
            self.entry = Controller.fetched_reqs[i]

            # ---- build widgets
            #must use tk.Entry instead of ttk because background and foreground
            # colors are not changable with ttk
            antrags_list.append(tk.StringVar())

            start_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))

            end_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))
            
            stell_list.append(tk.Entry(self.F1.interior, width = 20, relief = 'groove'))

            grund_list.append(tk.Entry(self.F1.interior, width = 15, relief = 'groove'))

            emp_list.append(tk.Entry(self.F1.interior, width = 20, relief = 'groove'))
            # ---- build widgets
            
            # ---- insert info into each widget by index
            antrags_list[i] = str(self.entry[0])

            start_list[i].insert(0, str(self.entry[1]))
            start_list[i].grid(row = i + 1, column = 0, **pad_options)

            end_list[i].insert(0, str(self.entry[2]))
            end_list[i].grid(row = i +1, column = 1, **pad_options)

            if self.entry[11]:
                Controller.get_stellvertreter_name(self, self.entry[11])
                stell_list[i].insert(0, Controller.stell_info_formatted[0])
            stell_list[i].config(foreground = 'black')
            #color widget based on its contents
            if int(self.entry[7]) == 0:
                stell_list[i].config(background = '#d4ef64')
            elif int(self.entry[7]) == 1:
                stell_list[i].config(background = '#64ef7f')
            elif int(self.entry[7]) == 2:
                stell_list[i].config(background = '#ef7f64')
            stell_list[i].grid(row = i + 1, column = 2, **pad_options)

            grund_list[i].insert(0, str(self.entry[4]))
            grund_list[i].grid(row = i + 1, column = 3, **pad_options)

            emp_list[i].insert(0, f'{str(self.entry[3])} {str(self.entry[10])}, {str(self.entry[9])}')
            emp_list[i].grid(row = i + 1, column = 4)

            # ---- table button widgets
            #used for changing the approval status button
            def cycle_status_val(i):
                if status_val_list[i] == 2:
                    status_list[i].config(background = '#d4ef64', foreground = 'black', \
                        text = 'geplant')
                    status_val_list[i] = 1
                elif status_val_list[i] == 1:
                    status_list[i].config(background = '#ef7f64', foreground = 'white', \
                        text = 'denied')
                    status_val_list[i] = 0
                elif status_val_list[i] == 0:
                    status_list[i].config(background = '#64ef7f', foreground = 'black', \
                        text = 'bestätigt')
                    status_val_list[i] = 2

            status_list.append(tk.Button(self.F1.interior, width = 10, \
                command = lambda i=i :cycle_status_val(i)))
            status_val_list.append(int)
            if str(self.entry[5]) == 'bestätigt':
                status_list[i].config(background = '#64ef7f', foreground = 'black', \
                    text = 'bestätigt')
                status_val_list[i] = 2
            elif str(self.entry[5]) == 'geplant':
                status_list[i].config(background = '#d4ef64', foreground = 'black', \
                    text = 'geplant')
                status_val_list[i] = 1
            elif str(self.entry [5]) =='denied':
                status_list[i].config(background = '#ef7f64', foreground = 'white', \
                    text = 'denied')
                status_val_list[i] = 0
            status_list[i].grid(row = i + 1, column = 5, **pad_options)

            def update_button(self, i):
                start_date = start_list[i].get().strip()
                end_date = end_list[i].get().strip()
                new_reason = grund_list[i].get().strip()

                if status_val_list[i] == 2:
                    sStatus = 'bestätigt'
                elif status_val_list[i] == 1:
                    sStatus = 'geplant'
                elif status_val_list[i] == 0:
                    sStatus = 'denied'

                sStellvertreter = stell_list[i].get().strip()
                xnRequest = antrags_list[i]

                #checking for an unfilled start date
                if start_date == '' or start_date == 'YYYY-MM-DD':
                    Controller.error_window(self, 'Please enter a start date.', 'info', 2500)
                    return

                #checking for an unfilled end date
                if end_date == '' or end_date == 'YYYY-MM-DD':
                    end_date = start_date

                #setting string dates to datetime
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError as error:
                    Controller.error_window(self, f'Please enter a valid date format.\n\n{error}', 'error')
                    return

                if start_date > end_date:
                    Controller.error_window(self, 'Please enter an end date that is later than the start date.', 'info', 3000)
                    return

                updated = (start_date, end_date, new_reason, sStatus, sStellvertreter, login_info, xnRequest)
                Controller.man_update(self, updated)
                manager_view.combo_handler(self)

            button_list.append(ttk.Button(self.F1.interior, text = 'Update', width = 10, \
                command = lambda i=i : update_button(self, i)))
            button_list[i].grid(row = i + 1, column = 6, **pad_options)

            def mark_seen_button(self, i):
                Controller.set_seen(self, int(antrags_list[i]))
                manager_view.combo_handler(self)
            
            mark_seen_button_list.append(ttk.Button(self.F1.interior, text = 'Mark as Seen', \
                width = 15, command = lambda i=i : mark_seen_button(self, i)))
            mark_seen_button_list[i].grid(row = i + 1, column = 7, **pad_options)
            # ---- table buton widgets

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        #start processes to build schedule
        Controller.create_table(self)

    def data(self, index, role):
        #index gives location in the table for which info is currently being requested. .row() and .column()
        #role describes what kind of info the method should return on thi call. QtDisplayRole expects a str.
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value
        if role == Qt.BackgroundRole:
            value = self._data[index.row()][index.column()]
            if value == '   ':
                return QtGui.QColor('#757575')
            if value == '--------------':
                return QtGui.QColor('dark gray')
            if value == 'Feiertag':
                return QtGui.QColor('#55d3dd')
            if value == 'geplant':
                return QtGui.QColor('#dda355')
            if value == 'bestätigt':
                return QtGui.QColor('#5dbb4e')
            if ',' in value and '*' not in value:
                return QtGui.QColor('#ef7f64')
            if '*' in value:
                return QtGui.QColor('#8d55dd')
            else:
                return value

    #needed for dimensions of table
    def rowCount(self, index = None):
        return len(Controller.rows)

    #needed for dimensions of table
    def columnCount(self, index = None):
        return len(Controller.headers)

    #needed for column headers
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return Controller.headers[section]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return Controller.rows[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

class Ui_Form(object):
    #directly pulled from the QT Designer file
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
            Controller.get_group_from_empnum(self, empnum)
        if empnum in Controller.manager_empnums:
            Controller.selected_group.append(7)

        #builds table widget
        self.tableWidget = QtWidgets.QTableView(self.layoutWidget) 
        self.tableWidget.setObjectName("tableWidget")

        #puts the TableModel class into table widget and fills it with data
        data = Controller.data_values
        self.model = TableModel(data) 
        self.verticalLayout.addWidget(self.tableWidget) 
        self.verticalLayout_2.addLayout(self.verticalLayout) 
        self.tableWidget.setModel(self.model)
        for i in range(TableModel.columnCount(TableModel)):
            self.tableWidget.setColumnWidth(i, 100)
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'hello', QtCore.Qt.DisplayRole)


        self.retranslateUi(Form, empnum)
        QtCore.QMetaObject.connectSlotsByName(Form)

    #more QTDesigner code
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
        self.comboBox.setItemText(7, _translate("Form", "Alle Grupppen"))
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

        #disables produktionsgruppe combobox if user is not a manater
        if empnum not in Controller.manager_empnums:
            self.comboBox.setEnabled(False)
        if empnum in Controller.manager_empnums:
            ...

    def change_group(self):
        group_selection = int(self.comboBox.currentIndex())
        data = Controller.data_values
        Controller.selected_group.clear()
        Controller.list_of_emp_info.clear()
        Controller.rows.clear()
        Controller.selected_group.append(group_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model)

    def change_month(self):
        month_selection = int(self.comboBox_2.currentIndex()) + 1
        data = Controller.data_values
        Controller.selected_month.clear()
        Controller.selected_month.append(month_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model)

    def change_year(self):
        year_selection = int(self.comboBox_3.currentText())
        data = Controller.data_values
        Controller.selected_year.clear()
        Controller.selected_year.append(year_selection)
        self.model = TableModel(data)
        self.tableWidget.setModel(self.model)

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
