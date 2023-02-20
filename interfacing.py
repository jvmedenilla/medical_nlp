#           this python file is where I test out interfacing because 
#           I can test features here with a smaller data set before
#           testing it with a much larger data set

from tkinter import *

root = Tk()

root.geometry("500x500")    # size of the first window
root.title("Welcome")       # title of the first window

options = ["patient", "doctor", "student/researcher", "other"]   # this would ideally change what kind of resources we should show them
clicked = StringVar()
clicked.set("patient")

drop = OptionMenu(root, clicked, *options).place(x=250, y=40)   # drop down menu in the first window
# drop.pack()    # use pack if you want a default location

def print_input():          # this would print any input from the interface in to the terminal
    occu_input = fn.get()
    print(occu_input)
    
def exit_window():          # for cancelling the program
    exit()

def second_win():           # define second window
    window=Tk()
    window.title("welcome to the second window")
    window.geometry("500x500")
    options1 = ['pain', 'Pain', 'back', 'excruciating', 'painful', 'tenderness', 'discomfort', 'feel', 'suffering', 'Knee'] # drop donw for the second window
    gn = StringVar()
    clicked1 = gn
    clicked1.set(options[0])
    drop1 = OptionMenu(window, clicked1, *options1).place(x=250, y=40)
    label2 = Label(window, text="Enter Words: ", width=20, font=("arial", 10, "bold")).place(x=120, y=125)
    entry2 = Entry(window,textvar=gn).place(x=250, y=125)
    button2_enter = Button(window, text="enter", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = gn.get()).place(x=200,y=200)  #enter button
    button2_cancel = Button(window, text="cancel", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = exit_window).place(x=300,y=200)  # cancel button


button_enter = Button(root, text="enter", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = print_input).place(x=200,y=200)  # enter button
button_cancel = Button(root, text="cancel", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = exit_window).place(x=300,y=200) # cancel button
button_next = Button(root, text="next", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = second_win).place(x=250,y=250) # next button


label1 = Label(root, text="Search: ", width=20, font=("arial", 10, "bold")).place(x=120, y=160)
entry1 = Entry(root,textvar=fn).place(x=250, y=160)

root.mainloop()


