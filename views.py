#The View represents the GUI, which interact with the end
#user. It represents the model's data to the user.
import tkinter as tk
from tkinter import ttk
from datetime import date

from controller import Controller
from PIL import Image, ImageTk

class loginbox(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text = "Core Solution Einloggen")
        self.label.grid(column = 1, row = 0)
        
        self.L1 = ttk.Label(self, text = "Personal Nummer:")
        self.L1.grid(column = 0, row = 1, sticky = "E")

        self.E1_var = tk.StringVar()
        self.E1 = ttk.Entry(self, textvariable = self.E1_var)
        self.E1.focus()
        self.E1.grid(column = 1, row = 1, sticky = "W")

        self.B1 = ttk.Button(self, text = "Submit", \
            command = lambda : [controller.show_frame(emp_choose), loginbox.submit(self)])
        self.B1.grid(column = 2, row = 1, sticky = "")

    def submit(self):
        Controller.login(int(self.E1.get()))

class emp_choose(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text = "Options")
        self.label.grid(column = 1, row = 0)

        self.L1 = ttk.Label(self, text = "View Request")
        self.L1.grid(column = 0, row = 1)

        self.B1 = ttk.Button(self, text = "Go", \
            command = lambda : controller.show_frame(employee_req_view))
        self.B1.grid(column = 0, row = 2)

        self.L2 = ttk.Label(self, text = "New Request")
        self.L2.grid(column = 2, row = 1)

        self.B2 = ttk.Button(self, text = "Go", \
            command = lambda : controller.show_frame(request_window))
        self.B2.grid(column = 2, row = 2)
            
class request_window(ttk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Create an object of tkinter ImageTk
        self.path = 'S:/Öffentliche Ordner/Logos/Core Solution/Logo/CoreSolution_Logo_RGB.jpg'
        self.img = Image.open(self.path)
        self.img.thumbnail((150,150))
        self.new_img = ImageTk.PhotoImage(self.img)
# Create a Label Widget to display the text or Image
        self.label = ttk.Label(root, image = self.new_img)
        self.label.pack()

        self.Main = ttk.Frame(self)

        # ----- Section 1
 
        self.section1 = ttk.Frame(self.Main)
 
        self.L1 = ttk.Label(self.section1, text = "Name")
        self.L1.pack(padx = 5, pady = 5, side = 'left')
 
        self.E1 = ttk.Entry(self.section1)
        self.E1.pack(padx = 5, pady = 5, side = 'left')
 
        self.L2 = ttk.Label(self.section1, text = "Vorname")
        self.L2.pack(padx = 5, pady = 5, side = 'left')
 
        self.E2 = ttk.Entry(self.section1)
        self.E2.pack(padx = 5, pady = 5, side = 'left')

        self.L3 = ttk.Label(self.section1, text = "Abteilung")
        self.L3.pack(padx = 5, pady = 5, side = 'left')

        self.E3 = ttk.Entry(self.section1)
        self.E3.pack(padx = 5, pady = 5, side = 'left')
        
         
        self.section1.pack(padx = 5, pady = 5, expand = True, fill = 'x')
 
        # ----- Section 1
 

        # ----- Section 2
 
        self.section2 = ttk.Frame(self.Main)
        
        self.L4 = ttk.Label(self.section2, text = "Personal-Nr:")
        self.L4.pack(padx = 5, pady = 5, side = 'left')
        
        ## ---- nEmployee
       
        self.nEmployee = ttk.Entry(self.section2)
        self.nEmployee.pack(padx = 5, pady = 5, side = 'left')
        
        ## ---- nEmployee

        self.L5 = ttk.Label(self.section2, text = "Stellvertreter:")
        self.L5.pack(padx = 5, pady = 5, side = 'left')
 
        self.E5 = ttk.Entry(self.section2)
        self.E5.pack(padx = 5, pady = 5, side = 'left')
 
        self.L6 = ttk.Label(self.section2, text = "Resturlaub:")
        self.L6.pack(padx = 5, pady = 5, side = 'left')
 
        self.E6 = ttk.Entry(self.section2)
        self.E6.pack(padx = 5, pady = 5, side = 'left')
        ## ---- nEmployee

        self.section2.pack(padx = 5, pady = 5, expand = True, fill = 'x')
 
        # ----- Section 2


        # ----- Section 3
        
        self.section3 = ttk.Frame(self.Main)
    
        self.L7 = ttk.Label(self.section3, text = "Urlaub am/vom")
        self.L7.pack(padx = 5, pady = 5, side = 'left')

        ## ---- dDateStart

        self.dDateStart = ttk.Entry(self.section3)
        self.dDateStart.pack(padx = 5, pady = 5, side = 'left')

        ## ---- dDateStart

        self.L8 = ttk.Label(self.section3, text = "bis einschl.")
        self.L8.pack(padx = 5, pady = 5, side = 'left')
        
        ## ---- dDateEnd
        
        self.dDateEnd = ttk.Entry(self.section3)
        self.dDateEnd.pack(padx = 5, pady = 5, side = 'left')
               
    
        ## ---- dDateEnd
        
        self.L9 = ttk.Label(self.section3, text = "Urlaubsdauer (Anzahl der  Arbeitstage)")
        self.L9.pack(padx = 5, pady = 5, side = 'left')
 
        self.E9 = ttk.Entry(self.section3, width = 6)
        self.E9.pack(padx = 5, pady = 5, side = 'left')
         
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

class employee_req_view(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text = "Request Search")
        self.label.grid(column = 2, row = 0)

        self.E1_var = tk.StringVar()
        self.E1 = ttk.Entry(self, textvariable = self.E1_var)
        self.E1.focus()
        self.E1.grid(column = 2, row = 1)

        self.L0 = ttk.Label(self, text = 'Antragsnummer:')
        self.L0.grid(column = 1, row = 1)

        self.B1 = ttk.Button(self, text = "Search", \
            command = lambda : employee_req_view.search(self))
        self.B1.grid(column = 3, row = 1)

        self.L1 = ttk.Label(self, text = 'Startdatum')
        self.L1.grid(column = 0, row = 2)

        self.text1 = tk.StringVar()
        self.T1 = ttk.Entry(self, textvariable = self.text1)
        self.T1.grid(column = 0, row = 3)

        self.L2 = ttk.Label(self, text = 'Endedatum')
        self.L2.grid(column = 1, row = 2)

        self.text2 = tk.StringVar()
        self.T2 = ttk.Entry(self, textvariable = self.text2)
        self.T2.grid(column = 1, row = 3)

        self.L3 = ttk.Label(self, text = 'Personalnummer')
        self.L3.grid(column = 2, row = 2)

        self.text3 = int()
        #the widget below uses the tk.Entry class rather than ttk.Entry
        # because the background and foreground options of ttk.Entry do not work
        self.T3 = tk.Entry(self, textvariable = self.text3, \
            background = "grey", foreground = "white")
        self.T3.grid(column = 2, row = 3)

        self.L4 = ttk.Label(self, text = 'Grund')
        self.L4.grid(column = 3, row = 2)

        self.text4 = tk.StringVar()
        self.T4 = ttk.Entry(self, textvariable = self.text4)
        self.T4.grid(column = 3, row = 3)

        self.L5 = ttk.Label(self, text = 'Status')
        self.L5.grid(column = 4,  row = 2)

        self.text5 = tk.StringVar()
        #the widget below uses the tk.Entry class rather than ttk.Entry
        # because the background and foreground options of ttk.Entry do not work
        self.T5 = tk.Entry(self, textvariable = self.text5, \
            background = "grey", foreground = "white")
        self.T5.grid(column = 4, row = 3)

        self.B2 = ttk.Button(self, text = "Return", \
            command = lambda : controller.show_frame(emp_choose))
        self.B2.grid(column = 1, row = 4)

        self.B3 = ttk.Button(self, text = "Update", \
            command = lambda : employee_req_view.update(self))
        self.B3.grid(column = 3, row = 4)

    def search(self):
        Controller.search(int(self.E1.get()))
        self.T1.delete(0, 'end')
        self.T1.insert(0, [str(Controller.req_data[0])])
        self.T2.delete(0, 'end')
        self.T2.insert(0, [str(Controller.req_data[1])])
        self.T3.delete(0, 'end')
        self.T3.insert(0, [str(Controller.req_data[2])])
        self.T4.delete(0, 'end')
        self.T4.insert(0, [str(Controller.req_data[3])])
        self.T5.delete(0, 'end')
        self.T5.insert(0, [str(Controller.req_data[4])])

    def update(self):
        start_date = self.T1.get().strip()
        end_date = self.T2.get().strip()
        new_reason = self.T4.get().strip()
        xnRequest = self.E1.get().strip()
        if start_date or end_date:
            if end_date == '':
                end_date = start_date
            updated = (start_date, end_date, new_reason, xnRequest)
        Controller.update(updated)
