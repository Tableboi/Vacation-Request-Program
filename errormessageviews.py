import pandas as pd
from tkinter import *
from tkinter import messagebox

#ERROR MESSAGE GUI
class Error_message(Tk):
        def create_Widgets(self, error_str):
            self.label = Label(self, text = error_str)
            self.label.pack(pady = 10)
            self.button = Button(self, text = 'Back', 
                                command = lambda: self.destroy())
            self.button.pack(pady = 10)
        
        def __init__(self, error_str):
            Tk.__init__(self)
            self.title('Error')
            self.geometry('200x100')
            self.create_Widgets(error_str)

app = Error_message('This input is incorrect')
app.mainloop()