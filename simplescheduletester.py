import datetime
import re
from asyncio.windows_events import NULL
from datetime import timedelta
from tkinter import *
from tkinter.ttk import *
from turtle import width

import pyodbc
from requests import request

cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                    "Server=SOPCP01DE;"
                    "Database=PulseCoreTest5;"
                    "UID=PCDev2;"
                    "PWD=PCCSDev2PC5_!;")
    
cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor()
    



class Schedule():
    def __init__(self,  master, empnum):
        self.master = master
        master.title('Schedule')
        master.geometry('800x800')
        self.Main = Frame(self.master)
        self.Main.pack(fill = BOTH)
        
        ProduktionsGruppe = {0:'Wissenträger', 1:'Produktions Gruppe 1', 2:'Produktions Gruppe 2', 
                     3:'Produktions Gruppe 3', 4:'Produktions Gruppe 4', 5:'Produktionsunterstützung',
                     6: 'Keine Gruppe'}
        
        months = {0:'Januar', 1:'Februar', 2:'März', 3:'April', 4:'Mai', 5:'Juni', 
          6:'Juli', 7:'August', 8:'September', 9:'Oktober', 10:'November', 11:'Dezember'}
        
        numberofdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        listofnumberlists = []
       
        sqlgetnumbers = """SELECT [nEmployee]
                            FROM [PulseCoreTest5].[dbo].[PO_employee]
                            WHERE [nProduktionsGruppe] = ?"""
        
        sqlgetnumbersnotingroups = """ SELECT [nEmployee]
                                        FROM [PulseCoreTest5].[dbo].[PO_employee]
                                        WHERE [nProduktionsGruppe] IS NULL"""
        
        sqlgetholidays = """SELECT [Feiertag], [Datum] 
                            FROM [PulseCoreTest5].[dbo].[PC_Holidays]"""
                            
        sqlgetrequests = """SELECT [xnRequest] 
                                ,[dDateStart]
                                ,[dDateEnd]
                                ,[nEmployee]
                                ,[sReasons]
                                ,[sStatus]
                            FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]"""
        
        #get holidays
        cursor.execute(sqlgetholidays)
        holidays = cursor.fetchall()
        listofholidaydates = []
        for holiday in holidays:
            holidayname = holiday[0]
            holidaydate = holiday[1]
            listofholidaydates.append(holidaydate.strftime('%Y.' + '%m.' + '%d'))   
        
        #get lists of emp numbers
        pgvaluelist = [0, 1, 2, 3, 4, 5]
        for i in pgvaluelist:
            cursor.execute(sqlgetnumbers, i)
            columnlist = cursor.fetchall()
            columnlist.sort()
            columnlist.insert(0, 'Date')
            listofnumberlists.append(columnlist)
        
            #format emp numbers
            for i in range(1, len(columnlist)):
                item = str(columnlist[i])
                item = re.sub(r'[(,)]', '', item)
                newitem = item.replace('"', "")
                columnlist.remove(columnlist[i])
                columnlist.insert(i, int(newitem[0:-1]))
        
        #get NULL list of emp numbers        
        cursor.execute(sqlgetnumbersnotingroups)
        columnlist = cursor.fetchall()
        columnlist.sort()
        columnlist.insert(0, 'Date')
        for i in range(1, len(columnlist)):
                item = str(columnlist[i])
                item = re.sub(r'[(,)]', '', item)
                newitem = item.replace('"', "")
                columnlist.remove(columnlist[i])
                columnlist.insert(i, int(newitem[0:-1]))
        listofnumberlists.append(columnlist)
        
        cursor.execute(sqlgetrequests)
        requestlistraw = cursor.fetchall()
       
        #create request dictionary
        requestdictionary = {}
        
        #necessary to make requests between start and end date  
        def date_range(start, end):
            delta = end - start
            days = [start + timedelta(days = i) for i in range(delta.days + 1)]
            return days

        for item in requestlistraw:
            selectedemployeenumber = item[3]
            for numlist in listofnumberlists:
                if selectedemployeenumber in numlist:
                        requestdictionary[item[0]] = [selectedemployeenumber, item[1].strftime('%Y.' + '%m.' + '%d')]
                        start_date = item[1]
                        end_date = item[2]
                        daterangelist = date_range(start_date, end_date)
                
                        for i in range(0, len(daterangelist)):
                            requestdictionary[item[0] + (i * .01)] = [selectedemployeenumber, 
                                                daterangelist[i].strftime('%Y.' + '%m.' + '%d'), item[5]]
                else:
                    pass
        
        #get information on current date
        current_date = datetime.datetime.now()
        current_month = int(current_date.strftime('%m'))
        current_year = int(current_date.strftime('%Y'))
        
        #make a list of the next 5 years starting from current
        years = {0:current_year, 1:current_year + 1, 2: current_year + 2, 3: current_year + 3, 
                 4:current_year + 4, 5:current_year + 5}
           
        def change_value():
            
            #get request info
            for key, value in requestdictionary.items():
                req_list = value
                nameentered = req_list[0]
                dateentered = req_list[1]
                status = req_list[2]
                
                #check if requests are in the selected production group
                for item in listofnumberlists:
                    if nameentered in listofnumberlists[PGselectionint]:
                        nameindex = listofnumberlists[PGselectionint].index(nameentered)    
                    else:
                        nameindex = None
                    
                #isolate day, month, and year values
                dayentered = (dateentered[8:10:1]).lstrip('0')
                monthentered = (dateentered[5:7:1]).lstrip('0')
                yearentered = dateentered[0:4:1]
                
                #check if date is on the weekend
                weekend = set([5, 6])
                if datetime.datetime(int(yearentered), int(monthentered), int(dayentered)).weekday() in weekend:
                    pass
                elif datetime.datetime(int(yearentered), int(monthentered), int(dayentered)).strftime('%Y.'
                                                + '%m.' + '%d') in listofholidaydates:
                    pass
                else:         
                
                    #check if date is in shown month
                    if int(monthentered) == month_shown:
                        if int(yearentered) == year_shown:    
                            #select day
                            tree.selection_set(dayentered)
                            for item in tree.selection():
                                item_values = tree.item(item, "values")
                            
                            #update value and delete old value    
                            temp = list(item_values)
                            if nameindex is not None:                  
                                if status == 'bestätigt':
                                    temp[nameindex] = 'VACATION'
                                if status == 'geplant':
                                    temp[nameindex] = 'Requested'
                                temptuple = tuple(temp)
                                tree.delete(tree.selection()[0])
                                tree.insert(parent = '', index = int(dayentered) - 1, iid = int(dayentered), text = '', values = temptuple)
                                                
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
            
        
        def select_PG(a):
            
            #delete existing tree
            for i in tree.get_children():
                tree.delete(i)
            
            #get production group selection
            PGselection = self.PGvariable.get()
            global PGselectionint
            if PGselection != 'Gruppe auswählen':
                PGselectionint = [k for k, v in ProduktionsGruppe.items() if v == PGselection][0]
            else:
                for numlist in listofnumberlists:
                    if empnum in numlist:
                        PGselectionint = listofnumberlists.index(numlist)
            self.PGvariable.set(ProduktionsGruppe[PGselectionint])
            
            #create tree with list of selected group's names as columns
            treeview_columns = listofnumberlists[PGselectionint]
            tree['columns'] = treeview_columns
            create_tree(treeview_columns)
                    
        def select_year(c):
            Yearselection = self.Yearvariable.get()
            if Yearselection != 'Jahr auswählen':
                Yearselectionint = int(Yearselection)
            else:
                Yearselectionint = current_year
            global year_shown
            year_shown = Yearselectionint
            select_month(b=1)
          
        def select_month(b):
            
            #clear existing tree
            tree.delete(*tree.get_children())
            
            #get month selection
            Monthselection = self.Monthvariable.get()
            if Monthselection != 'Monat auswählen':
                Monthselectionint = [k for k, v in months.items() if v == Monthselection][0] + 1
            else:
                Monthselectionint = current_month
            global month_shown
            month_shown = Monthselectionint    
            self.Monthvariable.set(months[Monthselectionint-1])
            
            #populate tree
            for c in range (0, 31):
                datebeingused = datetime.datetime(year_shown, month_shown, 1) + timedelta(days = c)
                datevalue = datebeingused.strftime('%d' + ' %b' + ' %y' + ' %a')
                
                if c <= numberofdays[Monthselectionint - 1]-1:
                    weekend = set([5, 6])
                    numberofcolumns = len(listofnumberlists[PGselectionint])
                    
                    if datebeingused.weekday() in weekend:    
                        treevalueslist = [datevalue]
                        for i in range (0, numberofcolumns):
                            treevalueslist.append('Weekend')
                        treevalues = tuple(treevalueslist)
                        tree.insert('', index = c, iid = c + 1, text = '', values = treevalues, tags = ('weekend',))
                        tree.tag_configure('weekend', background = 'light gray')
                        
                    elif datebeingused.strftime('%Y.' + '%m.' + '%d') in listofholidaydates:
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
           
            change_value()
                    
        
        #Widgets        
        self.treeFrame = Frame(self.Main, height = 690, width = 800)
        self.treeFrame.pack(side = BOTTOM, expand = False)
        
        self.optionsFrame = Frame(self.Main, height = 140, width = 800)
        self.optionsFrame.pack(side = TOP, expand = False)
        
        self.PGvariable = StringVar()
        self.PGvariable.set(ProduktionsGruppe[0])
        self.ProduktionsGruppeOptionMenu = OptionMenu(self.optionsFrame, self.PGvariable, 
                    'Gruppe auswählen', *ProduktionsGruppe.values(), command = select_PG)
        self.ProduktionsGruppeOptionMenu.pack(pady = 10)
        
        self.Monthvariable = StringVar()
        self.Monthvariable.set(months[0])
        self.MonthOptionMenu = OptionMenu(self.optionsFrame, self.Monthvariable, 
                    'Monat auswählen', *months.values(), command = select_month)
        self.MonthOptionMenu.pack(pady = 10)
        
        self.Yearvariable = StringVar()
        self.Yearvariable.set(years[0])
        self.YearOptionMenu = OptionMenu(self.optionsFrame, self.Yearvariable,
                    'Jahr auswählen', *years.values(), command = select_year)
        self.YearOptionMenu.pack(pady = 10)
         
        
        def create_tree(columnlist):
            tree.column('#0', anchor = CENTER, stretch = 0, width = 100)
            tree.heading('Date', text = 'Date')
            for i, val in enumerate(columnlist):
                    tree.column(str(i), anchor = CENTER, stretch = 0, width = 100)
                    tree.heading(columnlist[i], text = columnlist[i])

            tree.pack(fill = BOTH)    
            
            select_year(c = 1) 
       
        tree = Treeview(self.treeFrame, show = 'headings', height = 32)
         
        #create scrollbar
        hbar = Scrollbar(self.treeFrame, orient = HORIZONTAL, command = tree.xview)
        tree.configure(xscrollcommand = hbar.set)
        hbar.pack(side = BOTTOM, fill = 'x')
            
        zebra = 1
        if zebra:
            style = Style()
            aktualTheme = style.theme_use()
            style.theme_create("dummy", parent=aktualTheme)
            style.theme_use("dummy")
            Style().configure('Treeview', background = 'white', foregound = 'white', fieldbackground = 'white')
        
        select_PG(empnum)
        
if __name__ == '__main__':
    root = Tk()
    Schedule(root, 50020)
    root.mainloop()
    
cursor.close()
cnxn.close()
