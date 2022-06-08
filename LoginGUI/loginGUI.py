from tkinter import *
from PIL import ImageTk, Image

ws = Tk()
ws.title('Core Solution: Login')
ws.config(bg='#0B5A81')

f = ('Times', 14)

left_frame = Frame(
    ws, 
    bd=2, 
    bg='#CCCCCC',   
    relief=SOLID, 
    padx=10, 
    pady=10
    )

Label(
    left_frame, 
    text="Personalnummer:", 
    bg='#CCCCCC',
    font=f).grid(row=0, column=0, sticky=W, pady=10)

email_tf = Entry(
    left_frame, 
    font=f
    )

login_btn = Button(
    left_frame, 
    width=15, 
    text='Login', 
    font=f, 
    relief=SOLID,
    cursor='hand2',
    command=None
    )

email_tf.grid(row=0, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.pack()

frame = Frame(ws, padx = 5, pady = 5)  
frame.pack()  
img = ImageTk.PhotoImage(Image.open("coresolutionlogo.jpg"))  
frame.create_image(20, 20, anchor=NW, image=img)


ws.mainloop()