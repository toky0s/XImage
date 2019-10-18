from tkinter import *


master = Tk()
master.geometry('300x200')

f = Frame(master, background='red')
f.pack()

l_name = Label(f, text='Name:')
l_name.grid(row=0, column=0, sticky=W)

l_age = Label(f, text='Age:')
l_age.grid(row=1, column=0, sticky=W)

var_name = StringVar()
entry_name = Entry(f, textvariable=var_name)
entry_name.grid(row=0, column=1, sticky=W)

var_age = StringVar()
entry_age = Entry(f, textvariable=var_age)
entry_age.grid(row=1, column=1, sticky=W)


def show_info():
    print("Your name: {}\nYour age: {}".format(var_name.get(), var_age.get()))


button_print = Button(f, text='Show info', command=show_info)
button_print.grid(row=2, column=0, sticky=W)

master.mainloop()

