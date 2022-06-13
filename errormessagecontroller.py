import errormessageviews as views

#ERROR MESSAGE
#Anywhere where an error messagebox should pop up, type: error_message('error message string')
def error_message(error_str):
    
    errmess = views.Error_message(error_str)
    errmess.mainloop()
    
error_message('Error: This shit dont work')