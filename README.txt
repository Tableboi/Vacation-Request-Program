# Urlaubsanträge Management Application

This application enables the creation, alteration, and confirmation of vacation requests for employees of Core Solutions

## Installation
Python 3 is required for running this application

The below files must all be installed in the same folder:
 - app.py
 - views.py
 - conroller.py
 - models.py
 
 The following modules need to be installed/imported to the python environment that will be used to run this application.
 Using the pip installer via the terminal is the easiest way to install these modules:
 - tkinter (for GUI management)
 - PyQt5 (for GUI management)
 - PIL (for diplaying Core Solution Logo)
 - qdarktheme (for theming PyQt5 GUI)
 - calendar (for retrieving month range information)
 - pyodbc (for connecting and querying the SQL database)
 
 ## File Descriptions
  The app.py file is the file that must be run in order to start the application. This file initializes the base app as a tkinterApp and sets the color theme. Then imports classes defined in the views.py file as frames within an empty array. The frames are then iterated through and stacked on top of eachother. To switch which frame is displayed on top, the show_frame method is used.
  
  The views.py file contains all script relevant to the GUI in one place. The views file is divided into four main GUIs: loginbox, request_window, manager_view, UI form, which are all defined as classes within the views file. Other classes are present, but they are used as a means of supporting/simplifying the 4 main classes.
 1.) The loginbox handles logging in, updating requests of the user, confirming the user's acceptance or refusal as a stellvertreter, and buttons for navigation to the other views.
 2.) The request_window handles the creation of new requests and the verification of each input's format.
 3.) The manager_view handles all manager functions including the display of vacation requests filtered by various options, updating request information, confirmation or denial of requests, and contains buttons for navigation to the other views.
 4.) The UI form is used to display a table in a popup window. The GUI handler of this view is unlike the others, as it is a PyQt5 GUI rather than tkinter. The table contains filtering options like production group, month, and year. If accessed by someone that does not have managerial credentials, the table will only display the production group associated with the user.

 The controller.py file acts as a bridge between the views.py and models.py file. The Controller class contains all methods and variables that are used to prompt the fetching of data and alteration of data, or insertion of new data to the database. After the models.py fetches the data, the controller formats the information, then stores it temporarily to be displayed in the correct view. The controller also handles most (not all) exception/error popups that result in a failed connection to the database, incorrect input formatting, or missing required info.
 - The error_window method at the bottom of the file is responsible for the creation of these popups. It takes four parameters: self, error message to be displayed as a string, the type of message as a string, and the time in milliseconds as an integer with a default of 2000.
 
 The models.py contains the Model class, which is imported by the controller. This class contains the string and method required to establish a connection to the database. Methods are defined within this class, which handle the fetching, updating, and deleting of data in the SQL server database. Each method contains a string containing a list of the parameters required for each query and their respective datatype. This string is then followed by a variable, which defines the SQL query as a string. Finally, every method ends with the function required to execute the above query with the parameters supplied by the controller.py file. For methods that update or add new information within the SQL database, the method must end with the Model.cnxn.commit() method, in order to finalize changes to the table.

## Notable Methods
On the loginbox view:
 - submit_click(self, event) starts everything on this page, it first creates a global variable, login_info, which is then populated by the contents of the entry box. The method then validates the user's input and initiates the methods used to load the resturlaub counter, the current request table, and pending stellvertreter request table.
 - search_by_employee(self, event = None) checks for the existence of vacation requests associated with the user's login info, it then prompts the construction of the necessary table if there are requests by calling self.search_emp().
 - start_stell_stuff(self) checks if the user has been listed as a stellvertreter in any existing requests, it then prompts the construction of the stellvertreter table by calling self.stell_stuff().
 
 On the request_window view:
  - submit(self, event = None) is responsible for all actions on this page other than the return button. It first validates, formats, and passes the entered data to the controller by calling the Controller.sub_new_info(self, data) method.

On the manager_view:
- combo_handler(self, event = None) contains all the different search options, which are selected by a combobox whose value determines the search parameters
- build_table(self) builds a table used to contain the fetched vacation requests. It's structure is always the same but the data to be stored is determined by the combobox handler
- open_schedule(self) handles all methods, variables, etc necessary for calling the schedule to load on a button press
- unseen_view(self) builds the table used to display all vacation requests that are marked as 'unseen'. This table is different from the build_table because of different buttons within the table

## Schedule
- Controller.create_table(self) is run every time the TableModel class in the views.py file is called. It runs functions to get the dates, employee names/numbers, holidays/weekends, and requests applicable for the shown dates based on the production group, year, and month selected. Each time a new production group, year, or month is selected (via the combobox on the schedule window), the table is recreated with the new infromation. 
- The class Ui_Form(object) in views.py was originally a file converted into Python from QtDesigner. QtDesigner was used to make the visual elements of the window, and then the code in this file was altered in order to fit it to our usage. This class defines the schedule window and its widgets, including the combo boxes and an empty table widget.
- The class TableModel(QtCore.QAbstractTableModel) in views.py comes from PyQt5. This inserts a custom TableModel into the existing table widget from the Ui_Form. This class needs an __init__(self, data) function, a data(self, index, role) function, a rowCount(self, index) function, a columnCount(self, index) function, and a headerData(self, section, orientation, role) function. The data function uses a list of tuples to populate the table with data. The rowCount and columnCount functions determine how many rows and columns to create in the table. The headerData function determines the names for the rows and columns.

ORIGINAL CREATORS: Rebecca Francis, Alex Mesa, Roberto Paz
