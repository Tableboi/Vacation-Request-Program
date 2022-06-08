from tkinter import *
from tkinter import messagebox
 
class Window:
    def __init__(self, master):
        self.master = master
 
        self.Main = Frame(self.master)
         
        self.L1 = Label(self.Main, text = "Welcome to Core Solution")
        self.L1.grid(row = 0, column = 1, padx = 5, pady = 5, columnspan = 2)
         
        # Username
        self.L2 = Label(self.Main, text = "Personalnummer : ")
        self.L2.grid(row = 1, column = 0, padx = 5, pady = 5)
 
        self.E1 = Entry(self.Main, width = 30)
        self.E1.grid(row = 1, column = 1, padx = 5, pady = 5, columnspan = 3)
 
        # Password
        self.L3 = Label(self.Main, text = "Passwort: ")
        self.L3.grid(row = 2, column = 0, padx = 5, pady = 5)
 
        self.E2 = Entry(self.Main, show = "*", width = 30)
        self.E2.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan = 3)
 
        # Buttons
        self.B1 = Button(self.Main, text = "Submit", command = self.verify)
        self.B1.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = "e")
 
        self.B2 = Button(self.Main, text = "Clear", command = self.clear)
        self.B2.grid(row = 3, column = 3, padx = 5, pady = 5)
 
        self.Main.pack(padx = 5, pady = 5)
 
    def clear(self):
        self.E1.delete(0, 'end')
        self.E2.delete(0, 'end')
 
    def verify(self):
        user = self.E1.get()
        password = self.E2.get()
 
        file = open("Accounts.txt", "r")
 
        for line in file:
            temp = line.strip("\n").split(",")
 
            if user == temp[0] and password == temp[1]:
                print("Your Login Credentials have been Verified")
                return 1
 
        prompt = messagebox.showerror(title = "Error!", message = "Incorrect Login Details")
        return 0
 
 
root = Tk()
window = Window(root)
root.mainloop()