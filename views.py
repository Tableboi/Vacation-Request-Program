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
from controller import Controller

class loginbox(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        pad_options = {'padx' : 5, 'pady' : 5}

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self, image = self.new_img)
        self.label.pack(side = 'top', pady = 20)

        #setting the font types
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 14, weight = "bold", underline = 1)
        
        subheader_font = tkinter.font.Font(\
            family = "Helvertica", size = 12, weight = "normal", underline = 0)

        self.F1 = ttk.Frame(self, relief = 'groove', \
            borderwidth = 2, padding = 5)
        self.F1.pack(pady = 20)

        self.label = ttk.Label(self.F1, text = "Einloggen")
        self.label.grid(column = 1, row = 0, **pad_options)
        self.label.configure(font = header_font)
        
        self.L1 = ttk.Label(self.F1, text = "Personal Nummer:")
        self.L1.grid(column = 0, row = 1, sticky = "E", **pad_options)

        logininfo = tk.StringVar()
        self.E1 = ttk.Entry(self.F1, textvariable = logininfo)
        self.E1.focus()
        self.E1.grid(column = 1, row = 1, sticky = "W", **pad_options)

        self.B1 = ttk.Button(self.F1, text = "Submit", \
            command = lambda : loginbox.submit(self))
        self.B1.grid(column = 2, row = 1, sticky = "", **pad_options)

        self.F2 = ttk.Frame(self, relief = 'groove', \
            borderwidth = 2, padding = 5)

        #self.label = ttk.Label(self.F2, text = "Options")
        #self.label.grid(columnspan = 3, column = 0, row = 0)

        self.L1 = ttk.Label(self.F2, text = "View Request")
        self.L1.configure(font = subheader_font)
        self.L1.grid(column = 0, row = 1, **pad_options)

        self.B1 = ttk.Button(self.F2, text = "Go", \
                command = lambda : controller.show_frame(employee_req_view), \
                    state = 'disabled')
        self.B1.grid(column = 0, row = 2, **pad_options)

        self.L2 = ttk.Label(self.F2, text = "New Request")
        self.L2.configure(font = subheader_font)
        self.L2.grid(column = 1, row = 1, **pad_options)

        self.B2 = ttk.Button(self.F2, text = "Go", \
                command = lambda : controller.show_frame(request_window), state = 'disabled')
        self.B2.grid(column = 1, row = 2, **pad_options)

        self.L3 = ttk.Label(self.F2, text = "Manager View")
        self.L3.configure(font = subheader_font)
        self.L3.grid(column = 2, row = 1, **pad_options)
            
        self.B3 = ttk.Button(self.F2, text = "Go", \
                command = lambda : controller.show_frame(manager_view), \
                    state = 'disabled')
        self.B3.grid(column = 2, row = 2, **pad_options)

    def submit(self):
        #reveal buttons
        self.F2.pack(pady = 10)

        #reset button states
        self.B1.configure(state = 'disable')
        self.B2.configure(state = 'disable')
        self.B3.configure(state = 'disable')

        #need a global variable here so other classes can easily access it
        global login_info
        login_info = self.E1.get()
        try:
            Controller.login(int(login_info))
            #this is the employee number validator, to check if
            # the user is a manager
            if int(login_info) == 905:
                loginbox.enable_allbuttons(self)
            else:
                loginbox.enable_empbuttons(self)
        except TypeError:
            messagebox.showerror('Error', 'Invalid Personalnummer')
    
    def enable_empbuttons(self):
        self.B1.configure(state = 'enable')
        self.B2.configure(state = 'enable')
    
    def enable_allbuttons(self):
        self.B1.configure(state = 'enable')
        self.B2.configure(state = 'enable')
        self.B3.configure(state = 'enable')
            
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
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Main, image = self.new_img)
        self.label.grid(column = 1, row = 0, padx = 5, pady = 5)

        # ----- Section 1
        # pack options for section 1
        s1options = {'padx' : 5, 'pady' : 5}

        self.section1 = ttk.Frame(self.Main, **frame_options)
 
        self.L1 = ttk.Label(self.section1, text = "Name:")
        self.L1.grid(column = 0, row = 0, **s1options)
 
        self.E1 = ttk.Entry(self.section1)
        self.E1.grid(column = 1, row = 0, **s1options)
 
        self.L2 = ttk.Label(self.section1, text = "Vorname:")
        self.L2.grid(column = 2, row = 0, **s1options)
 
        self.E2 = ttk.Entry(self.section1)
        self.E2.grid(column = 3, row = 0, **s1options)

        self.L3 = ttk.Label(self.section1, text = "Abteilung:")
        self.L3.grid(column = 4, row = 0, **s1options)

        self.E3 = ttk.Entry(self.section1)
        self.E3.grid(column = 5, row = 0, **s1options)
        
         
        self.section1.grid(columnspan = 2, column = 0, row = 1, padx = 5, pady = 5, sticky = 'ns')
 
        # ----- Section 1
 

        # ----- Section 2
        # pack options for section 2
        s2options = {'padx' : 5, 'pady' : 5}

        self.section2 = ttk.Frame(self.Main, **frame_options)
        
        self.L4 = ttk.Label(self.section2, text = "Personal-Nr:")
        self.L4.grid(column = 0, row = 0, **s2options)
        
        ## ---- nEmployee
       
        self.nEmployee = ttk.Entry(self.section2)
        self.nEmployee.grid(column = 1, row = 0, **s2options)
        
        ## ---- nEmployee

        self.L5 = ttk.Label(self.section2, text = "Stellvertreter:")
        self.L5.grid(column = 2, row = 0, **s2options)
 
        self.E5 = ttk.Entry(self.section2)
        self.E5.grid(column = 3, row = 0, **s2options)
 
        self.L6 = ttk.Label(self.section2, text = "Resturlaub:")
        self.L6.grid(column = 4, row = 0, **s2options)
 
        self.E6 = ttk.Entry(self.section2)
        self.E6.grid(column = 5, row = 0, **s2options)
        ## ---- nEmployee

        self.section2.grid(columnspan = 2, column = 0, row = 2, padx = 5, pady = 5, sticky = 'ns')
 
        # ----- Section 2


        # ----- Section 3
        # pack options for section 3
        s3options = {'padx' : 5, 'pady' : 5}

        self.section3 = ttk.Frame(self.Main, **frame_options)
    
        self.L7 = ttk.Label(self.section3, text = "Urlaub am/vom")
        self.L7.grid(column = 0, row = 0, **s3options)

        ## ---- dDateStart

        self.dDateStart = ttk.Entry(self.section3)
        self.dDateStart.grid(column = 1, row = 0, **s3options)

        ## ---- dDateStart

        self.L8 = ttk.Label(self.section3, text = "bis einschl.")
        self.L8.grid(column = 2, row = 0, **s3options)
        
        ## ---- dDateEnd
        
        self.dDateEnd = ttk.Entry(self.section3)
        self.dDateEnd.grid(column = 3, row = 0, **s3options)
               
    
        ## ---- dDateEnd
        
        self.L9 = ttk.Label(self.section3, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L9.grid(column = 4, row = 0, **s3options)
 
        self.E9 = ttk.Entry(self.section3, width = 6)
        self.E9.grid(column = 5, row = 0, **s3options)
         
        self.section3.grid(columnspan = 2, column = 0, row = 3, padx = 5, pady = 5, sticky = 'ns')
       
        # ----- Section 3
    
       
        # ------ Section 4
        # pad options for section 4
        s4options = {'padx' : 5, 'pady' : 5}

        self.section4 = ttk.Frame(self.Main)
        
        ## ---- Section 4 sub-frame 1

        self.section4_1 = ttk.Frame(self.section4, **frame_options)        
 
        self.L10 = ttk.Label(self.section4_1, text = "Urlaubsgrund:")
        self.L10.pack(padx = 5, pady = 5)

        self.T1 = tk.Text(self.section4_1, height = 2, width = 20)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = 'x')

        self.section4_1.grid(column = 0, row = 0, **s4options)
 
        ## ---- Section 4 sub-frame 1
 
 
        ## ---- Section 4 sub-frame 2
         
        self.section4_2 = ttk.Frame(self.section4, **frame_options)        
 
        self.L12 = ttk.Label(self.section4_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
              
        self.Rvar2 = tk.IntVar()

        self.R3 = ttk.Radiobutton(self.section4_2, text = "Ja", variable = self.Rvar2, value = 3)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = ttk.Radiobutton(self.section4_2, text = "Nein", variable = self.Rvar2, value = 4)
        self.R4.pack(padx = 5, pady = 5)
      
        self.section4_2.grid(column = 1, row = 0, **s4options)
         
        ## ---- Section 4 sub-frame 2

        ## ---- Section 4 sub-frame 3

        self.section4_3 = ttk.Frame(self.section4, **frame_options)

        self.L13 = ttk.Label(self.section4_3, text = "Deine Urlaubtage:")
        self.L13.pack(padx = 5, pady = 5)

        self.E10_var = tk.IntVar()
        self.E10 = ttk.Entry(self.section4_3, textvariable = self.E10_var)
        self.E10.pack(padx = 5, pady = 5)

        self.section4_3.grid(column = 2, row = 0, **s4options)

        self.section4.grid(columnspan = 2, column = 0 , row = 4, padx = 5, pady = 5, sticky = 'ns')
        
        ## ---- Section 4 sub-frame 3

        ## ----- Section 4

        self.bottom = ttk.Frame(self.Main)
        
        self.B1 = ttk.Button(self.bottom, text = "Submit", \
            command = lambda : request_window.submit(self))
        self.B1.pack(padx = 5, pady = 5, side = 'right')
        
        self.B2 = ttk.Button(self.bottom, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.B2.pack(padx = 5, pady = 5, side = 'left')

        self.bottom.grid(columnspan = 2, column = 0, row = 6, sticky = 'ns')
 
        self.Main.pack(fill = 'y')

    def update_vacation_days(self):
        Controller.get_days_left(login_info)
        self.E10.insert(0, str(Controller.days_left))

    def submit(self):
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            data = (start_date, end_date, self.nEmployee.get(), self.T1.get("1.0", "end"), "geplant", self.E5.get())
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
        self.Headerframe.columnconfigure(4, weight = 2)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Headerframe, image = self.new_img)
        self.label.grid(rowspan = 2, column = 5, row = 0, \
            padx = 10, pady = 20, sticky = 'e')

        self.label = ttk.Label(self.Headerframe, text = "Manager Request Search")
        self.label.configure(font = header_font)
        self.label.grid( columnspan = 2, column = 0, row = 0, padx = 10, pady = 20)

        self.E1_var = tk.StringVar()
        self.E1 = ttk.Entry(self.Headerframe, textvariable = self.E1_var)
        self.E1.focus()
        self.E1.grid(column = 1, row = 1)

        self.L0 = ttk.Label(self.Headerframe, text = 'Personalnummer:')
        self.L0.grid(column = 0, row = 1)

        self.B1 = ttk.Button(self.Headerframe, text = "Search", \
            command = lambda : manager_view.search_by_employee(self))
        self.B1.grid(column = 2, row = 1)

        self.Bhf2 = ttk.Button(self.Headerframe, text = "Load All", \
            command = lambda : manager_view.all_view(self))
        self.Bhf2.grid(column = 3, row = 1)
        
        self.Bhf3 = ttk.Button(self.Headerframe, text = "View Schedule", \
            command = lambda : manager_view.open_schedule(self))
        self.Bhf3.grid(column = 4, row = 1, padx = 10, pady = 10)

        #command frame for the buttons on the bottom
        self.F2 = ttk.Frame(self)
        self.F2.pack(side = 'bottom', fill = 'x')
        self.F2.configure(relief = 'groove', \
            borderwidth = 2, padding = 5)

        self.cf_label = ttk.Label(self.F2, text = 'Update Requests:')
        self.cf_label.configure(font = header_font)
        self.cf_label.grid(columnspan = 1, column = 0, row = 0)
        
        self.cf_search_label = ttk.Label(self.F2, text = 'Antragsnummer:')
        self.cf_search_label.grid(column = 1, row = 1)

        self.cf_search_val = tk.StringVar()
        self.cf_search = ttk.Entry(self.F2, textvariable = self.cf_search_val)
        self.cf_search.grid(column = 2, row = 1)

        self.cf_search_button = ttk.Button(self.F2, text = 'Search', \
            command = lambda : manager_view.search(self))
        self.cf_search_button.grid(column = 3, row = 1)

        self.cf_options = {'padx' : 5, 'pady' : 5}

        self.cf_Eframe = ttk.Frame(self.F2)
        self.cf_Eframe.grid(columnspan = 5, column = 0, row = 2)

        self.cf_E1_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E1 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E1_val, \
            width = 15, state = 'disabled')
        self.cf_E1.grid(column = 0, row = 0, **self.cf_options)

        self.cf_E2_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E2 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E2_val, \
            width = 15, state = 'disabled')
        self.cf_E2.grid(column = 1, row = 0, **self.cf_options)

        self.cf_E3_val = tk.StringVar(value = 'personalnummer')
        self.cf_E3 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E3_val, \
            width = 15, state = 'disabled')
        self.cf_E3.grid(column = 2, row = 0, **self.cf_options)

        self.cf_E4_val = tk.StringVar(value = 'grund')
        self.cf_E4 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E4_val, \
            width = 15, state = 'disabled')
        self.cf_E4.grid(column = 3, row = 0, **self.cf_options)

        self.cf_E5_val = tk.StringVar(value = 'status')
        self.cf_E5 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E5_val, \
            width = 15, state = 'disabled')
        self.cf_E5.grid(column = 4, row = 0, **self.cf_options)

        self.cf_E6_val = tk.StringVar(value = 'stellvertreter')
        self.cf_E6 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E6_val, \
            width = 15, state = 'disabled')
        self.cf_E6.grid(column = 5, row = 0, **self.cf_options)

        self.B2 = ttk.Button(self.F2, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.B2.grid(column = 1, row = 3)

        self.B3 = ttk.Button(self.F2, text = "Update", \
            command = lambda : manager_view.update(self))
        self.B3.grid(column = 3, row = 3)

        self.B4 = ttk.Button(self.F2, text = "Delete Request", \
            command = lambda : manager_view.delete(self))
        self.B4.grid(column = 2, row = 3)

        #entry box master frame
        self.F1 = VerticalScrolledFrame(self)
        self.F1.pack(fill = 'x')

    def open_schedule(self):
        schedule = Schedule()

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

        for i in range(0, row_len, 1):
            for ii in range(0, 7, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior, width = 15))
                self.entries[-1].insert(0, [data])
                self.entries[-1].configure(state = 'disabled')
                self.entries[-1].grid(row = i + 1 , column = ii, padx = 5, pady = 5)

    def search_by_employee(self):
        Controller.search_emp(int(self.E1.get()))

        #validating if the input personalnummer has entries associated with it
        if not Controller.fetched_reqs:
            for widget in self.F1.interior.winfo_children():
                widget.destroy()
            messagebox.showerror('Error', 'No requests associated with this numnber.')
        else:
            manager_view.specific_view(self)

    def specific_view(self):
        row_len = len(Controller.fetched_reqs)
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


        for i in range(0, row_len, 1):
            for ii in range(0, 6, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior, width = 15))
                self.entries[-1].insert(0, [data])
                self.entries[-1].configure(state = 'disabled')
                self.entries[-1].grid(row = i + 1 , column = ii, padx = 5, pady = 5)

    def search(self):
        Controller.search(int(self.cf_search.get()))
        try:
            
            self.cf_E1.config(state = 'endabled')
            self.cf_E1.delete(0, 'end')
            self.cf_E1.insert(0, [str(Controller.req_data[0])])

            self.cf_E2.config(state = 'enabled')
            self.cf_E2.delete(0, 'end')
            self.cf_E2.insert(0, [str(Controller.req_data[1])])

            self.cf_E3.config(state = 'enabled')
            self.cf_E3.delete(0, 'end')
            self.cf_E3.insert(0, [str(Controller.req_data[2])])
            self.cf_E3.config(state = 'disabled')
            
            self.cf_E4.config(state = 'enabled')
            self.cf_E4.delete(0, 'end')
            self.cf_E4.insert(0, [str(Controller.req_data[3]).strip()])

            self.cf_E5.config(state = 'enabled')
            self.cf_E5.delete(0, 'end')
            self.cf_E5.insert(0, [str(Controller.req_data[4])])

            self.cf_E6.config(state = 'enabled')
            self.cf_E6.delete(0, 'end')
            self.cf_E6.insert(0, [str(Controller.req_data[5])])

        except TypeError:
            messagebox.showerror('Error', 'Invalid Antragsnummer')

    def update(self):
        start_date = self.cf_E1.get().strip()
        end_date = self.cf_E2.get().strip()
        new_reason = self.cf_E4.get().strip()
        sStatus = self.cf_E5.get().strip()
        xnRequest = self.cf_search.get().strip()
        sStellvertreter = self.cf_E6.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, sStatus, sStellvertreter, xnRequest)
        Controller.man_update(updated)
    
    def delete(self):
        xnRequest = self.cf_search.get().strip()
        Controller.delete(xnRequest)
        self.cf_E1.delete(0, 'end')
        self.cf_E2.delete(0, 'end')

        self.cf_E3.config(state = 'enabled')
        self.cf_E3.delete(0, 'end')
        self.cf_E3.config(state = 'disabled')

        self.cf_E4.delete(0, 'end')
        self.cf_E5.delete(0, 'end')
        self.cf_E6.delete(0, 'end')

class employee_req_view(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        #setting some fonts for headers
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 16, weight = "bold", underline = 1)

        #top frame for header widgets
        self.Headerframe = ttk.Frame(self)
        self.Headerframe.pack(side = 'top', fill = 'x')
        self.Headerframe.configure(relief = 'groove', \
            borderwidth = 2)
        self.Headerframe.columnconfigure(2, weight = 4)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Headerframe, image = self.new_img)
        self.label.grid(column = 2, row = 0, padx = 10, pady = 20, sticky = 'e')

        self.label = ttk.Label(self.Headerframe, text = "Your Requests:")
        self.label.configure(font = header_font)
        self.label.grid(column = 0, row = 0, padx = 10, pady = 20)

        self.B1 = ttk.Button(self.Headerframe, text = "Load", \
            command = lambda : employee_req_view.search_by_employee(self))
        self.B1.grid(column = 1, row = 0, padx = 5, pady = 5)

        #command frame for the buttons on the bottom
        self.F2 = ttk.Frame(self)
        self.F2.pack(side = 'bottom', fill = 'x')
        self.F2.configure(relief = 'groove', \
            borderwidth = 2, padding = 5)

        self.cf_label = ttk.Label(self.F2, text = 'Update Request:')
        self.cf_label.configure(font = header_font)
        self.cf_label.grid(columnspan = 1, column = 0, row = 0)
        
        self.cf_search_label = ttk.Label(self.F2, text = 'Antragsnummer:')
        self.cf_search_label.grid(column = 1, row = 1)

        self.cf_search_val = tk.StringVar()
        self.cf_search = ttk.Entry(self.F2, textvariable = self.cf_search_val)
        self.cf_search.focus()
        self.cf_search.grid(column = 2, row = 1)

        self.cf_search_button = ttk.Button(self.F2, text = 'Search', \
            command = lambda : employee_req_view.search(self))
        self.cf_search_button.grid(column = 3, row = 1)

        self.cf_options = {'padx' : 5, 'pady' : 5}

        self.cf_Eframe = ttk.Frame(self.F2)
        self.cf_Eframe.grid(columnspan = 5, column = 0, row = 2)

        self.cf_E1_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E1 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E1_val, width = 15)
        self.cf_E1.config(foreground = 'grey')
        self.cf_E1.grid(column = 0, row = 0, **self.cf_options)

        self.cf_E2_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E2 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E2_val, width = 15)
        self.cf_E2.config(foreground = 'grey')
        self.cf_E2.grid(column = 1, row = 0, **self.cf_options)

        self.cf_E3_val = tk.StringVar(value = 'personalnummer')
        self.cf_E3 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E3_val, width = 15)
        self.cf_E3.config(foreground = 'grey')
        self.cf_E3.grid(column = 2, row = 0, **self.cf_options)

        self.cf_E4_val = tk.StringVar(value = 'grund')
        self.cf_E4 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E4_val, width = 15)
        self.cf_E4.config(foreground = 'grey')
        self.cf_E4.grid(column = 3, row = 0, **self.cf_options)

        self.cf_E5_val = tk.StringVar(value = 'status')
        self.cf_E5 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E5_val, width = 15)
        self.cf_E5.config(foreground = 'grey')
        self.cf_E5.grid(column = 4, row = 0, **self.cf_options)

        self.cf_E6_val = tk.StringVar(value = 'stellvertreter')
        self.cf_E6 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E6_val, width = 15)
        self.cf_E6.config(foreground = 'grey')
        self.cf_E6.grid(column = 5, row = 0, **self.cf_options)

        self.B2 = ttk.Button(self.F2, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.B2.grid(column = 1, row = 3)

        self.B3 = ttk.Button(self.F2, text = "Update", \
            command = lambda : employee_req_view.update(self))
        self.B3.grid(column = 3, row = 3)

        #entry box master frame
        self.F1 = VerticalScrolledFrame(self)
        self.F1.pack(fill = 'x')            

    def search_by_employee(self):
        Controller.search_emp(login_info)

        #validating if the input personalnummer has entries associated with it
        if not Controller.fetched_reqs:
            for widget in self.F1.interior.winfo_children():
                widget.destroy()
            messagebox.showerror('Error', 'No requests associated with this numnber.')
        else:
            employee_req_view.search_emp(self)

    def search_emp(self):        
        #lists necessary for entries
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
        
        #Controller.search_emp(int(login_info))
        row_len = len(Controller.fetched_reqs)

        for i in range(0, row_len, 1):
            for ii in range(0, 6, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior, width = 15))
                self.entries[-1].insert(0, [data])
                self.entries[-1].configure(state = 'disabled')
                self.entries[-1].grid(row = i + 1 , column = ii, padx = 5, pady = 5)

    def search(self):
        #try except is necessary here instead of controller because the error
        # arises as a result of this method, not because of the model used
        try:
            Controller.search(int(self.cf_search.get()))

            self.cf_E1.delete(0, 'end')
            self.cf_E1.config(foreground = 'black')
            self.cf_E1.insert(0, [str(Controller.req_data[0])])

            self.cf_E2.delete(0, 'end')
            self.cf_E2.config(foreground = 'black')
            self.cf_E2.insert(0, [str(Controller.req_data[1])])

            self.cf_E3.config(state = 'enabled')
            self.cf_E3.delete(0, 'end')
            self.cf_E3.config(foreground = 'black')
            self.cf_E3.insert(0, [str(Controller.req_data[2])])
            self.cf_E3.config(state = 'disabled')
            
            self.cf_E4.delete(0, 'end')
            self.cf_E4.config(foreground = 'black')
            self.cf_E4.insert(0, [str(Controller.req_data[3]).strip()])

            self.cf_E5.config(state = 'enabled')
            self.cf_E5.delete(0, 'end')
            self.cf_E5.config(foreground = 'black')
            self.cf_E5.insert(0, [str(Controller.req_data[4])])
            self.cf_E5.config(state = 'disabled')

            self.cf_E6.delete(0, 'end')
            self.cf_E6.config(foreground = 'black')
            self.cf_E6.insert(0, [str(Controller.req_data[5])])

        except TypeError:
            messagebox.showerror('Error', 'Invalid Antragsnummer')

    def update(self):
        start_date = self.cf_E1.get().strip()
        end_date = self.cf_E2.get().strip()
        new_reason = self.cf_E4.get().strip()
        xnRequest = self.cf_search.get().strip()
        sStellvertreter = self.cf_E6.get().strip()

        if int(login_info) != Controller.req_data[2]:
            messagebox.showerror('Error', 'Cannot edit requests associated with a different personalnummer.')
        elif start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, sStellvertreter, xnRequest, int(login_info))
            Controller.update(updated)

class Schedule(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Schedule')

        self.geometry('800x900')

        self.Main = ttk.Frame(self)
        self.Main.pack(fill = 'both')

        #things to be initialized
        Controller.get_holidays()
        Controller.get_emp_list()
        Controller.get_no_group_list()
        Controller.get_requests()

        #widgets
        self.treeFrame = ttk.Frame(self.Main, height = 690, width = 800)
        self.treeFrame.pack(side = 'bottom', expand = False)
        
        self.optionsFrame = ttk.Frame(self.Main, height = 140, width = 800)
        self.optionsFrame.pack(side = 'top', expand = False)
        
        global PGvariable
        PGvariable = tk.StringVar()
        PGvariable.set(Controller.ProduktionsGruppe[0])
        self.ProduktionsGruppeOptionMenu = ttk.OptionMenu(self.optionsFrame, PGvariable, 
                    'Gruppe auswählen', *Controller.ProduktionsGruppe.values(), command = Schedule.select_PG)
        self.ProduktionsGruppeOptionMenu.pack(pady = 10)
        
        global Monthvariable
        Monthvariable = tk.StringVar()
        Monthvariable.set(Controller.months[0])
        self.MonthOptionMenu = ttk.OptionMenu(self.optionsFrame, Monthvariable, 
                    'Monat auswählen', *Controller.months.values(), command = Schedule.select_month)
        self.MonthOptionMenu.pack(pady = 10)
        
        global Yearvariable
        Yearvariable = tk.StringVar()
        Yearvariable.set(Controller.years[0])
        self.YearOptionMenu = ttk.OptionMenu(self.optionsFrame, Yearvariable,
                    'Jahr auswählen', *Controller.years.values(), command = Schedule.select_year)
        self.YearOptionMenu.pack(pady = 10)

        global tree
        tree = ttk.Treeview(self.treeFrame, show = 'headings', height = 32)

        #create scrollbar
        hbar = ttk.Scrollbar(self.treeFrame, orient = 'horizontal', command = tree.xview)
        tree.configure(xscrollcommand = hbar.set)
        hbar.pack(side = 'bottom', fill = 'x')

        self.select_PG()

    def _on_mousewheel(self, event):
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def create_tree(self, columnlist):
        tree.column('#0', anchor = 'center', stretch = 0, width = 100)
        tree.heading('Date', text = 'Date')
        for i, val in enumerate(columnlist):
                tree.column(str(i), anchor = 'center', stretch = 0, width = 100)
                tree.heading(columnlist[i], text = columnlist[i])

        tree.pack(fill = 'both')    
        
        Schedule.select_year(self)
    
    def select_PG(self):
        #delete existing tree
        for i in tree.get_children():
            tree.delete(i)
        
        #get production group selection
        PGselection = PGvariable.get()
        if PGselection != 'Gruppe auswählen':
            global PGselectionint
            PGselectionint = [k for k, v in Controller.ProduktionsGruppe.items() if v == PGselection][0]
        else:
            #for numlist in Controller.list_of_number_lists:
            #    if empnum in numlist:
            #        PGselectionint = Controller.list_of_number_lists.index(numlist)
            #    else:
            #        pass
            PGselectionint = 0
        PGvariable.set(Controller.ProduktionsGruppe[PGselectionint])
        
        #create tree with list of selected group's names as columns
        treeview_columns = Controller.list_of_number_lists[PGselectionint]
        tree['columns'] = treeview_columns
        Schedule.create_tree(self, treeview_columns)
    
    def select_year(self):
        Yearselection = Yearvariable.get()
        if Yearselection != 'Jahr auswählen':
            Yearselectionint = int(Yearselection)
        else:
            Yearselectionint = Controller.current_year
        global year_shown
        year_shown = Yearselectionint
        Schedule.select_month(self)
    
    def select_month(self):
        #clear existing tree
        tree.delete(*tree.get_children())
        
        #get month selection
        Monthselection = Monthvariable.get()
        if Monthselection != 'Monat auswählen':
            Monthselectionint = [k for k, v in Controller.months.items() if v == Monthselection][0] + 1
        else:
            Monthselectionint = Controller.current_month
        
        global month_shown
        month_shown = Monthselectionint    
        Monthvariable.set(Controller.months[Monthselectionint-1])
        
        #populate tree
        for c in range (0, 31):
            datebeingused = datetime.datetime(year_shown, month_shown, 1) + timedelta(days = c)
            datevalue = datebeingused.strftime('%d' + ' %b' + ' %y' + ' %a')
            
            if c <= Controller.number_of_days[Monthselectionint - 1]-1:
                weekend = set([5, 6])
                numberofcolumns = len(Controller.list_of_number_lists[PGselectionint])
                
                if datebeingused.weekday() in weekend:    
                    treevalueslist = [datevalue]
                    for i in range (0, numberofcolumns):
                        treevalueslist.append('Weekend')
                    treevalues = tuple(treevalueslist)
                    tree.insert('', index = c, iid = c + 1, text = '', values = treevalues, tags = ('weekend',))
                    tree.tag_configure('weekend', background = 'light gray')
                    
                elif datebeingused.strftime('%Y.' + '%m.' + '%d') in Controller.list_of_holiday_dates:
                    treevalueslist = [datevalue]
                    for i in range (0, numberofcolumns):
                        treevalueslist.append('Holiday')
                    treevalues = tuple(treevalueslist)
                    tree.insert('', index = c, iid = c + 1, text = '', values = treevalues, tags = ('holiday',))
                    tree.tag_configure('holiday', background = 'light gray')
                else:
                    treevalueslist = [datevalue]
                    for i in range (0, numberofcolumns):
                        treevalueslist.append('--')
                    treevalues = tuple(treevalueslist)
                    tree.insert('', index = c, iid = c + 1, text = '', values = treevalues)
            else:
                pass
        
        Schedule.change_value(self)
    
    def change_value(self):
        #get request value
        for key, value in Controller.request_dictionary.items():
            req_list = value
            name_entered = req_list[0]
            date_entered = req_list[1]
            status = req_list[2]

            #check if requests are in the selected production group
            for item in Controller.list_of_number_lists:
                if name_entered in Controller.list_of_number_lists[PGselectionint]:
                    name_index = Controller.list_of_number_lists[PGselectionint].index(name_entered)
                else:
                    name_index = None
            
            #isolate day, month, year values
            day_entered = (date_entered[8:10:1]).lstrip('0')
            month_entered = (date_entered[5:7:1]).lstrip('0')
            year_entered = date_entered[0:4:1]

            #check if date is on the weekend
            weekend = set([5, 6])
            if datetime.datetime(int(year_entered), int(month_entered), int(day_entered)).weekday() in weekend:
                pass
            elif datetime.datetime(int(year_entered), int(month_entered), int(day_entered)).strftime('%Y.' \
                + '%m.' + '%d') in Controller.list_of_holiday_dates:
                pass
            else:
                #check if date is in shown month
                if int(month_entered) == month_shown:
                    if int(year_entered) == year_shown:
                        #select day
                        tree.selection_set(day_entered)
                        for item in tree.selection():
                            item_values = tree.item(item, "values")
                        
                        #update value and delete old value
                        temp = list(item_values)
                        if name_index is not None:
                            if status == 'bestätigt':
                                temp[name_index] = 'VACATION'
                            if status == 'geplant':
                                temp[name_index] = 'Requested'
                            temp_tuple = tuple(temp)
                            tree.delete(tree.selection()[0])
                            tree.insert(parent = '', index = int(day_entered) - 1, iid = int(day_entered), text = '', values = temp_tuple)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

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