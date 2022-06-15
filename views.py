#The View represents the GUI, which interact with the end
#user. It represents the model's data to the user.
import tkinter as tk
from tkinter import ttk
import tkinter.font
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk

from controller import Controller

class loginbox(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        pad_options = {'padx' : 5, 'pady' : 5}

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self, image = self.new_img)
        self.label.pack(side = 'top', **pad_options)

        #setting the font types
        header_font = tkinter.font.Font(\
            family = "Helvertica", size = 14, weight = "bold", underline = 1)
        
        subheader_font = tkinter.font.Font(\
            family = "Helvertica", size = 12, weight = "normal", underline = 0)

        self.F1 = ttk.Frame(self, relief = 'groove')
        self.F1.pack()

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

        self.F2 = ttk.Frame(self, relief = 'groove')
        #self.F2.pack()

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
                command = lambda : controller.show_frame(request_window), \
                    state = 'disabled')
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
        self.F2.pack()

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

        tk.Frame.__init__(self, parent)
        
        self.Main = ttk.Frame(self)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Main, image = self.new_img)
        self.label.grid(column = 0, row = 0, padx = 5, pady = 5)

        # ----- Section 1
        # pack options for section 1
        s1options = {'padx' : 5, 'pady' : 5}

        self.section1 = ttk.Frame(self.Main, relief = 'groove')
 
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
        
         
        self.section1.grid(column = 0, row = 1, padx = 5, pady = 5)
 
        # ----- Section 1
 

        # ----- Section 2
        # pack options for section 2
        s2options = {'padx' : 5, 'pady' : 5}

        self.section2 = ttk.Frame(self.Main, relief = 'groove')
        
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

        self.section2.grid(column = 0, row = 2, padx = 5, pady = 5)
 
        # ----- Section 2


        # ----- Section 3
        # pack options for section 3
        s3options = {'padx' : 5, 'pady' : 5}

        self.section3 = ttk.Frame(self.Main, relief = 'groove')
    
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
         
        self.section3.grid(column = 0, row = 3, padx = 5, pady = 5)
       
        # ----- Section 3
    
       
        # ------ Section 4

        self.section4 = ttk.Frame(self.Main)
        
        ## ---- Section 4 sub-frame 1

        self.section4_1 = ttk.Frame(self.section4, relief = 'groove')        
 
        self.L10 = ttk.Label(self.section4_1, text = "Urlaubsgrund:")
        self.L10.pack(padx = 5, pady = 5)

        self.T1 = tk.Text(self.section4_1, height = 2, width = 20)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = 'x')

        self.section4_1.pack(padx = 50, pady = 5, side = 'left')
 
        ## ---- Section 4 sub-frame 1
 
 
        ## ---- Section 4 sub-frame 2
         
        self.section4_2 = ttk.Frame(self.section4, relief = 'groove')        
 
        self.L12 = ttk.Label(self.section4_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
              
        self.Rvar2 = tk.IntVar()

        self.R3 = ttk.Radiobutton(self.section4_2, text = "Ja", variable = self.Rvar2, value = 3)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = ttk.Radiobutton(self.section4_2, text = "Nein", variable = self.Rvar2, value = 4)
        self.R4.pack(padx = 5, pady = 5)
      
        self.section4_2.pack(padx = 50, pady = 5, side = 'right')
         
        ## ---- Section 4 sub-frame 2
         
        self.section4.grid(column = 0 , row = 4, padx = 5, pady = 5)
        
        # ----- Section 4

        self.bottom = ttk.Frame(self.Main)
        
        self.B1 = ttk.Button(self.bottom, text = "Submit", \
            command = lambda : request_window.submit(self))
        self.B1.pack(padx = 5, pady = 5, side = 'right')
        
        self.B2 = ttk.Button(self.bottom, text = "Return", \
            command = lambda : controller.show_frame(loginbox))
        self.B2.pack(padx = 5, pady = 5, side = 'left')

        self.bottom.grid(column = 0, row = 6)
 
        self.Main.pack(expand = True, fill = 'both')

    def submit(self):
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            data = (start_date, end_date, self.nEmployee.get(), self.T1.get("1.0", "end"), "geplant")
        Controller.sub_new_info(data)

class manager_view(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #setting the font for headers
        header_font = tkinter.font.Font(\
            family = "Helvertica", size = 16, weight = "bold", underline = 1)
        
        #top frame for header widgets
        self.Headerframe = ttk.Frame(self)
        self.Headerframe.pack(side = 'top', fill = 'x')
        self.Headerframe.configure(relief = 'groove', \
            borderwidth = 2, padding = 5)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Headerframe, image = self.new_img)
        self.label.grid(rowspan = 2, columnspan = 2, column = 4, row = 0, \
            padx = 5, pady = 5)

        self.label = ttk.Label(self.Headerframe, text = "Manager Request Search")
        self.label.configure(font = header_font)
        self.label.grid( columnspan = 2, column = 0, row = 0)

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
        self.cf_E1 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E1_val)
        self.cf_E1.config(foreground = 'grey')
        self.cf_E1.grid(column = 0, row = 0, **self.cf_options)

        self.cf_E2_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E2 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E2_val)
        self.cf_E2.config(foreground = 'grey')
        self.cf_E2.grid(column = 1, row = 0, **self.cf_options)

        self.cf_E3_val = tk.StringVar(value = 'personalnummer')
        self.cf_E3 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E3_val)
        self.cf_E3.config(foreground = 'grey')
        self.cf_E3.grid(column = 2, row = 0, **self.cf_options)

        self.cf_E4_val = tk.StringVar(value = 'grund')
        self.cf_E4 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E4_val)
        self.cf_E4.config(foreground = 'grey')
        self.cf_E4.grid(column = 3, row = 0, **self.cf_options)

        self.cf_E5_val = tk.StringVar(value = 'status')
        self.cf_E5 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E5_val)
        self.cf_E5.config(foreground = 'grey')
        self.cf_E5.grid(column = 4, row = 0, **self.cf_options)

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

    def all_view(self):
        Controller.search_all()
        row_len = len(Controller.fetched_reqs)
        #list necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        column_headers = {'borderwidth' : 2, 'relief' : 'solid', 'background' : 'grey', 'foreground' : 'white'}

        self.Nu = ttk.Label(self.F1.interior, text = 'Antragsnummer', **column_headers)
        self.Nu.grid(column = 0, row = 0)
        
        self.L1 = ttk.Label(self.F1.interior, text = 'Startdatum', **column_headers)
        self.L1.grid(column = 1, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Endedatum', **column_headers)
        self.L2.grid(column = 2, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Personalnummer', **column_headers)
        self.L3.grid(column = 3, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Grund', **column_headers)
        self.L4.grid(column = 4, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Status', **column_headers)
        self.L5.grid(column = 5, row = 0)

        for i in range(0, row_len, 1):
            for ii in range(0, 6, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior))
                self.entries[-1].insert(0, [data])
                self.entries[-1].configure(state = 'disabled')
                self.entries[-1].grid(row = i + 1 , column = ii, padx = 5, pady = 5)

    def search_by_employee(self):
        Controller.search_emp(int(self.E1.get()))

        #validating if the input personalnummer has entries associated with it
        if not Controller.fetched_reqs:
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

        self.L1 = ttk.Label(self.F1.interior, text = 'Startdatum', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L1.grid(column = 0, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Endedatum', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L2.grid(column = 1, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Antragsnummer', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L3.grid(column = 2, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Grund', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L4.grid(column = 3, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Status', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L5.grid(column = 4, row = 0)


        for i in range(0, row_len, 1):
            for ii in range(0, 5, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior))
                self.entries[-1].insert(0, [data])
                self.entries[-1].configure(state = 'disabled')
                self.entries[-1].grid(row = i + 1 , column = ii, padx = 5, pady = 5)

    def search(self):
        Controller.search(int(self.cf_search.get()))
        try:
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

            self.cf_E5.delete(0, 'end')
            self.cf_E5.config(foreground = 'black')
            self.cf_E5.insert(0, [str(Controller.req_data[4])])

        except TypeError:
            messagebox.showerror('Error', 'Invalid Antragsnummer')

    def update(self):
        start_date = self.cf_E1.get().strip()
        end_date = self.cf_E2.get().strip()
        new_reason = self.cf_E4.get().strip()
        sStatus = self.cf_E5.get().strip()
        xnRequest = self.cf_search.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, sStatus, xnRequest)
        Controller.man_update(updated)
    
    def delete(self):
        xnRequest = self.cf_search.get().strip()
        Controller.delete(xnRequest)
        self.cf_E1.delete(0, 'end')
        self.cf_E2.delete(0, 'end')
        self.cf_E3.delete(0, 'end')
        self.cf_E4.delete(0, 'end')
        self.cf_E5.delete(0, 'end')

class employee_req_view(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #setting some fonts for headers
        header_font = tkinter.font.Font(\
            family = "Helvetica", size = 16, weight = "bold", underline = 1)

        #top frame for header widgets
        self.Headerframe = ttk.Frame(self)
        self.Headerframe.pack(side = 'top', fill = 'x')
        self.Headerframe.configure(relief = 'groove', \
            borderwidth = 2)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.Headerframe, image = self.new_img)
        self.label.grid(column = 2, row = 0, padx = 5, pady = 5)

        self.label = ttk.Label(self.Headerframe, text = "Your Requests:")
        self.label.configure(font = header_font)
        self.label.grid(column = 0, row = 0)

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
        self.cf_E1 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E1_val)
        self.cf_E1.config(foreground = 'grey')
        self.cf_E1.grid(column = 0, row = 0, **self.cf_options)

        self.cf_E2_val = tk.StringVar(value = 'yyyy-mm-dd')
        self.cf_E2 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E2_val)
        self.cf_E2.config(foreground = 'grey')
        self.cf_E2.grid(column = 1, row = 0, **self.cf_options)

        self.cf_E3_val = tk.StringVar(value = 'personalnummer')
        self.cf_E3 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E3_val)
        self.cf_E3.config(foreground = 'grey')
        self.cf_E3.grid(column = 2, row = 0, **self.cf_options)

        self.cf_E4_val = tk.StringVar(value = 'grund')
        self.cf_E4 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E4_val)
        self.cf_E4.config(foreground = 'grey')
        self.cf_E4.grid(column = 3, row = 0, **self.cf_options)

        self.cf_E5_val = tk.StringVar(value = 'status')
        self.cf_E5 = ttk.Entry(self.cf_Eframe, textvariable = self.cf_E5_val)
        self.cf_E5.config(foreground = 'grey')
        self.cf_E5.grid(column = 4, row = 0, **self.cf_options)

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
        #lists necessary for entries
        self.entries = []

        #first clear the frame that the entry widgets will fill
        for widget in self.F1.interior.winfo_children():
            widget.destroy()

        self.L1 = ttk.Label(self.F1.interior, text = 'Startdatum', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L1.grid(column = 0, row = 0)

        self.L2 = ttk.Label(self.F1.interior, text = 'Endedatum', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L2.grid(column = 1, row = 0)

        self.L3 = ttk.Label(self.F1.interior, text = 'Antragsnummer', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L3.grid(column = 2, row = 0)

        self.L4 = ttk.Label(self.F1.interior, text = 'Grund', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L4.grid(column = 3, row = 0)

        self.L5 = ttk.Label(self.F1.interior, text = 'Status', \
            borderwidth = 2, relief = 'solid', background = 'grey', \
            foreground = 'white')
        self.L5.grid(column = 4, row = 0)
        
        Controller.search_emp(int(login_info))
        row_len = len(Controller.fetched_reqs)

        for i in range(0, row_len, 1):
            for ii in range(0, 5, 1):
                entry = Controller.fetched_reqs[i]
                data = str(entry[ii])
                self.entries.append(ttk.Entry(self.F1.interior))
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
        except TypeError:
            messagebox.showerror('Error', 'Invalid Antragsnummer')

    def update(self):
        start_date = self.cf_E1.get().strip()
        end_date = self.cf_E2.get().strip()
        new_reason = self.cf_E4.get().strip()
        xnRequest = self.cf_search.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, xnRequest, int(login_info))
        if int(login_info) != Controller.req_data[2]:
            messagebox.showerror('Error', 'Cannot edit requests associated with a different personalnummer.')
        else:
            Controller.update(updated)
    
    def delete(self):
        xnRequest = self.cf_search.get().strip()
        Controller.delete(xnRequest)
        self.cf_E1.delete(0, 'end')
        self.cf_E2.delete(0, 'end')
        self.cf_E3.delete(0, 'end')
        self.cf_E4.delete(0, 'end')
        self.cf_E5.delete(0, 'end')

#The below frame is needed for the manager_view and employee_req_view
# scrollbar frames
class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side = 'left', fill = 'both', expand = True)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)