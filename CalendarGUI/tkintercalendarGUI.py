# import all methods and classes from tkinter
from tkinter import *

# import calendar module
import calendar

# Function for showing the calendar of the given year
def showCal():
    # Create a GUI window
    new_gui = Tk()
    # Set background color of GUI window
    new_gui.config(background = "white")
    # Set name of tkinter GUI window
    new_gui.title("CALENDAR")
    # Set configuration of GUI window
    new_gui.geometry("550x600")
    # Get method returns current text as string
    fetch_year = int(year_field.get())
    # Calendar method of calendar module return the calendar of given year
    cal_content = calendar.calendar(fetch_year)
    # Create a label for showing the content of the calendar
    cal_year = Label(new_gui, text = cal_content, font = "Consolas 10 bold")
    # Grid method is used for placing the widgets at respective positions in the table like structure
    cal_year.grid(row = 5, column = 1, padx = 20)
    # Start the GUI
    new_gui.mainloop()

# Driver code
if __name__ == "__main__":
    # Create a GUI window
    gui = Tk()
    # Set the background color of GUI window
    gui.config(background = "white")
    # Set the name of tkinter GUI window
    gui.title("CALENDAR")
    # Set configuration of GUI window
    gui.geometry("250x140")
    # Create a CALENDAR: label with specified font and size
    cal = Label(gui, text = "CALENDAR", bg = "dark gray", font = ("times", 28, 'bold'))
    # Create an Enter Year : label
    year = Label(gui, text = "Enter Year", bg = "light green")
    # Create a text entry box for filling or typing information
    year_field = Entry(gui)
    # Create a Show Calendar Button and attached showCal function
    Show = Button(gui, text = "Show Calendar", fg = "Black", bg = "Red", command = showCal)
    # Create an Exit Button and attached exit function
    Exit = Button(gui, text = "Exit", fg = "Black", bg = "Red", command = exit)
    # grid method is used for placing the widgets at respective positions in table like structure
    cal.grid(row = 1, column = 1)
    year.grid(row = 2, column = 1)
    year_field.grid(row = 3, column = 1)
    Show.grid(row = 4, column = 1)
    Exit.grid(row = 6, column = 1)
    # Start the GUI
    gui.mainloop()