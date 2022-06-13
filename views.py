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

        self.label = ttk.Label(self, text = "Core Solution Einloggen")
        self.label.grid(column = 1, row = 0)
        
        self.L1 = ttk.Label(self, text = "Personal Nummer:")
        self.L1.grid(column = 0, row = 1, sticky = "E")

        logininfo = int()
        self.E1 = ttk.Entry(self, textvariable = logininfo)
        self.E1.focus()
        self.E1.grid(column = 1, row = 1, sticky = "W")

        self.B1 = ttk.Button(self, text = "Submit", \
            command = lambda : [controller.show_frame(emp_choose), \
                loginbox.submit(self)])
        self.B1.grid(column = 2, row = 1, sticky = "")

    def submit(self):
        #need a global variable here so other classes can easily access it
        global logininfo
        logininfo = self.E1.get()
        Controller.login(logininfo)

class emp_choose(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text = "Options")
        self.label.grid(columnspan = 3, column = 0, row = 0)

        self.L1 = ttk.Label(self, text = "View Request")
        self.L1.grid(column = 0, row = 1)

        self.B1 = ttk.Button(self, text = "Go", \
            command = lambda : controller.show_frame(employee_req_view))
        self.B1.grid(column = 0, row = 2)

        self.L2 = ttk.Label(self, text = "New Request")
        self.L2.grid(column = 1, row = 1)

        self.B2 = ttk.Button(self, text = "Go", \
            command = lambda : controller.show_frame(request_window))
        self.B2.grid(column = 1, row = 2)

        self.L3 = ttk.Label(self, text = "Manager View")
        self.L3.grid(column = 2, row = 1)
        
        self.B3 = ttk.Button(self, text = "Go", \
            command = lambda : controller.show_frame(manager_view))
        self.B3.grid(column = 2, row = 2)
            
class request_window(ttk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((150,150))
        self.new_img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self, image = self.new_img)
        self.label.pack()

        self.Main = ttk.Frame(self)

        # ----- Section 1
        # pack options for section 1
        s1options = {'padx' : 5, 'pady' : 5, 'side' : 'left'}

        self.section1 = ttk.Frame(self.Main)
 
        self.L1 = ttk.Label(self.section1, text = "Name")
        self.L1.pack(**s1options)
 
        self.E1 = ttk.Entry(self.section1)
        self.E1.pack(**s1options)
 
        self.L2 = ttk.Label(self.section1, text = "Vorname")
        self.L2.pack(**s1options)
 
        self.E2 = ttk.Entry(self.section1)
        self.E2.pack(**s1options)

        self.L3 = ttk.Label(self.section1, text = "Abteilung")
        self.L3.pack(**s1options)

        self.E3 = ttk.Entry(self.section1)
        self.E3.pack(**s1options)
        
         
        self.section1.pack(padx = 5, pady = 5, expand = True, fill = 'x')
 
        # ----- Section 1
 

        # ----- Section 2
        # pack options for section 2
        s2options = {'padx' : 5, 'pady' : 5, 'side' : 'left'}

        self.section2 = ttk.Frame(self.Main)
        
        self.L4 = ttk.Label(self.section2, text = "Personal-Nr:")
        self.L4.pack(**s2options)
        
        ## ---- nEmployee
       
        self.nEmployee = ttk.Entry(self.section2)
        self.nEmployee.pack(**s2options)
        
        ## ---- nEmployee

        self.L5 = ttk.Label(self.section2, text = "Stellvertreter:")
        self.L5.pack(**s2options)
 
        self.E5 = ttk.Entry(self.section2)
        self.E5.pack(**s2options)
 
        self.L6 = ttk.Label(self.section2, text = "Resturlaub:")
        self.L6.pack(**s2options)
 
        self.E6 = ttk.Entry(self.section2)
        self.E6.pack(**s2options)
        ## ---- nEmployee

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = 'x')
 
        # ----- Section 2


        # ----- Section 3
        # pack options for section 3
        s3options = {'padx' : 5, 'pady' : 5, 'side' : 'left'}

        self.section3 = ttk.Frame(self.Main)
    
        self.L7 = ttk.Label(self.section3, text = "Urlaub am/vom")
        self.L7.pack(**s3options)

        ## ---- dDateStart

        self.dDateStart = ttk.Entry(self.section3)
        self.dDateStart.pack(**s3options)

        ## ---- dDateStart

        self.L8 = ttk.Label(self.section3, text = "bis einschl.")
        self.L8.pack(**s3options)
        
        ## ---- dDateEnd
        
        self.dDateEnd = ttk.Entry(self.section3)
        self.dDateEnd.pack(**s3options)
               
    
        ## ---- dDateEnd
        
        self.L9 = ttk.Label(self.section3, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L9.pack(**s3options)
 
        self.E9 = ttk.Entry(self.section3, width = 6)
        self.E9.pack(**s3options)
         
        self.section3.pack(padx = 5, pady = 5, expand = True, fill = 'x')
       
        # ----- Section 3
    
       
        # ------ Section 4

        self.section4 = ttk.Frame(self.Main)
        
        ## ---- Section 4 sub-frame 1

        self.section4_1 = ttk.Frame(self.section4)        
 
        self.L10 = ttk.Label(self.section4_1, text = "Urlaubsgrund:")
        self.L10.pack(padx = 5, pady = 5)

        self.T1 = tk.Text(self.section4_1, height = 2, width = 20)
        self.T1.pack(padx =5, pady = 5, expand = True, fill = 'x')

        self.section4_1.pack(padx = 50, pady = 5, side = 'left')
 
        ## ---- Section 4 sub-frame 1
 
 
        ## ---- Section 4 sub-frame 2
         
        self.section4_2 = ttk.Frame(self.section4)        
 
        self.L12 = ttk.Label(self.section4_2, text = "Nach Jahresplanung:")
        self.L12.pack(padx = 5, pady = 5)
              
        self.Rvar2 = tk.IntVar()

        self.R3 = ttk.Radiobutton(self.section4_2, text = "Ja", variable = self.Rvar2, value = 3)
        self.R3.pack(padx = 5, pady = 5)
        self.R4 = ttk.Radiobutton(self.section4_2, text = "Nein", variable = self.Rvar2, value = 4)
        self.R4.pack(padx = 5, pady = 5)
      
        self.section4_2.pack(padx = 50, pady = 5, side = 'right')
         
        ## ---- Section 4 sub-frame 2
         
        self.section4.pack(padx = 5, pady = 5, expand = True, fill = 'x')
        
        # ----- Section 4
        
        self.B1 = ttk.Button(self.Main, text = "Submit", \
            command = lambda : [controller.show_frame(loginbox), request_window.submit(self)])
        self.B1.pack(padx = 5, pady = 5, side = 'right')
        
        self.B2 = ttk.Button(self.Main, text = "Return", \
            command = lambda : controller.show_frame(emp_choose))
        self.B2.pack(padx = 5, pady = 5, side = 'left')
 
        self.Main.pack(padx = 5, pady = 5, expand = True, fill = 'x')

    def submit(self):
        start_date = self.dDateStart.get().strip()
        end_date = self.dDateEnd.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            data = (start_date, end_date, self.nEmployee.get(), self.T1.get("1.0", "end"), "anhängig")
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

        #command frame for the buttons on the bottom
        self.F2 = ttk.Frame(self)
        self.F2.pack(side = 'bottom', fill = 'x')
        self.F2.configure(relief = 'groove', \
            borderwidth = 2, padding = 5)

        self.cf_label = ttk.Label(self.F2, text = 'Update Requests:')
        self.cf_label.configure(font = header_font)
        self.cf_label.grid(columnspan = 5, column = 0, row = 0)
        
        self.cf_search_label = ttk.Label(self.F2, text = 'Antragsnummer:')
        self.cf_search_label.grid(column = 1, row = 1)

        self.cf_search_val = tk.StringVar()
        self.cf_search = ttk.Entry(self.F2, textvariable = self.cf_search_val)
        self.cf_search.grid(column = 2, row = 1)

        self.cf_search_button = ttk.Button(self.F2, text = 'Search', \
            command = lambda : manager_view.search(self))
        self.cf_search_button.grid(column = 3, row = 1)

        self.cf_options = {'padx' : 5, 'pady' : 5}

        self.cf_E1_val = tk.StringVar()
        self.cf_E1 = ttk.Entry(self.F2, textvariable = self.cf_E1_val)
        self.cf_E1.grid(column = 0, row = 2, **self.cf_options)

        self.cf_E2_val = tk.StringVar()
        self.cf_E2 = ttk.Entry(self.F2, textvariable = self.cf_E2_val)
        self.cf_E2.grid(column = 1, row = 2, **self.cf_options)

        self.cf_E3_val = tk.StringVar()
        self.cf_E3 = ttk.Entry(self.F2, textvariable = self.cf_E3_val)
        self.cf_E3.grid(column = 2, row = 2, **self.cf_options)

        self.cf_E4_val = tk.StringVar()
        self.cf_E4 = ttk.Entry(self.F2, textvariable = self.cf_E4_val)
        self.cf_E4.grid(column = 3, row = 2, **self.cf_options)

        self.cf_E5_val = tk.StringVar()
        self.cf_E5 = ttk.Entry(self.F2, textvariable = self.cf_E5_val)
        self.cf_E5.grid(column = 4, row = 2, **self.cf_options)

        self.B2 = ttk.Button(self.F2, text = "Return", \
            command = lambda : controller.show_frame(emp_choose))
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

        Controller.search_emp(int(self.E1.get()))
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
        Controller.search(int(self.cf_search.get()))
        self.cf_E1.delete(0, 'end')
        self.cf_E1.insert(0, [str(Controller.req_data[0])])
        self.cf_E2.delete(0, 'end')
        self.cf_E2.insert(0, [str(Controller.req_data[1])])

        self.cf_E3.config(state = 'enabled')
        self.cf_E3.delete(0, 'end')
        self.cf_E3.insert(0, [str(Controller.req_data[2])])
        self.cf_E3.config(state = 'disabled')

        self.cf_E4.delete(0, 'end')
        self.cf_E4.insert(0, [str(Controller.req_data[3]).strip()])
        self.cf_E5.delete(0, 'end')
        self.cf_E5.insert(0, [str(Controller.req_data[4])])

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
            borderwidth = 2, padding = 5)

        self.label = ttk.Label(self.Headerframe, text = "Your Requests:")
        self.label.configure(font = header_font)
        self.label.grid(column = 0, row = 0)

        self.B1 = ttk.Button(self.Headerframe, text = "Load", \
            command = lambda : employee_req_view.search_by_employee(self))
        self.B1.grid(column = 1, row = 0)

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
        self.cf_search.grid(column = 2, row = 1)

        self.cf_search_button = ttk.Button(self.F2, text = 'Search', \
            command = lambda : employee_req_view.search(self))
        self.cf_search_button.grid(column = 3, row = 1)

        self.cf_options = {'padx' : 5, 'pady' : 5}

        self.cf_E1_val = tk.StringVar()
        self.cf_E1 = ttk.Entry(self.F2, textvariable = self.cf_E1_val)
        self.cf_E1.grid(column = 0, row = 2, **self.cf_options)

        self.cf_E2_val = tk.StringVar()
        self.cf_E2 = ttk.Entry(self.F2, textvariable = self.cf_E2_val)
        self.cf_E2.grid(column = 1, row = 2, **self.cf_options)

        self.cf_E3_val = tk.StringVar()
        self.cf_E3 = ttk.Entry(self.F2, textvariable = self.cf_E3_val)
        self.cf_E3.grid(column = 2, row = 2, **self.cf_options)

        self.cf_E4_val = tk.StringVar()
        self.cf_E4 = ttk.Entry(self.F2, textvariable = self.cf_E4_val)
        self.cf_E4.grid(column = 3, row = 2, **self.cf_options)

        self.cf_E5_val = tk.StringVar()
        self.cf_E5 = ttk.Entry(self.F2, textvariable = self.cf_E5_val)
        self.cf_E5.grid(column = 4, row = 2, **self.cf_options)

        self.B2 = ttk.Button(self.F2, text = "Return", \
            command = lambda : controller.show_frame(emp_choose))
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
        
        Controller.search_emp(int(logininfo))
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
        Controller.search(int(self.cf_search.get()))
        self.cf_E1.delete(0, 'end')
        self.cf_E1.insert(0, [str(Controller.req_data[0])])
        self.cf_E2.delete(0, 'end')
        self.cf_E2.insert(0, [str(Controller.req_data[1])])

        self.cf_E3.config(state = 'enabled')
        self.cf_E3.delete(0, 'end')
        self.cf_E3.insert(0, [str(Controller.req_data[2])])
        self.cf_E3.config(state = 'disabled')
        
        self.cf_E4.delete(0, 'end')
        self.cf_E4.insert(0, [str(Controller.req_data[3]).strip()])

        self.cf_E5.config(state = 'enabled')
        self.cf_E5.delete(0, 'end')
        self.cf_E5.insert(0, [str(Controller.req_data[4])])
        self.cf_E5.config(state = 'disabled')

    def update(self):
        start_date = self.cf_E1.get().strip()
        end_date = self.cf_E2.get().strip()
        new_reason = self.cf_E4.get().strip()
        xnRequest = self.cf_search.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, xnRequest)
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

#ERROR MESSAGE GUI
class Error_message(tk.Toplevel):       
        def __init__(self, parent, controller, error_str):
            tk.Toplevel.__init__(self, parent)

            self.title('Error')
            self.geometry('200x100')
            self.create_Widgets(error_str)
        
        def create_Widgets(self, error_str):
            self.label = ttk.Label(self, text = error_str)
            self.label.pack(pady = 10)
            self.button = ttk.Button(self, text = 'Back', 
                                command = lambda: self.destroy())
            self.button.pack(pady = 10)
