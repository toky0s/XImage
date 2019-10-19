# # importing tkinter module
# from tkinter import * 
# from tkinter.ttk import *

# # creating tkinter window
# root = Tk()

# # Progress bar widget
# progress = Progressbar(root, orient=HORIZONTAL,
#                        length=100, mode='determinate')

# # Function responsible for the updation
# # of the progress bar value


# def bar():
#     import time
#     progress['value'] = 20
#     root.update_idletasks()
#     time.sleep(1)

#     progress['value'] = 40
#     root.update_idletasks()
#     time.sleep(1)

#     progress['value'] = 50
#     root.update_idletasks()
#     time.sleep(1)

#     progress['value'] = 60
#     root.update_idletasks()
#     time.sleep(1)

#     progress['value'] = 80
#     root.update_idletasks()
#     time.sleep(1)
#     progress['value'] = 100


# progress.pack(pady=10)

# # This button will initialize
# # the progress bar
# Button(root, text='Start', command=bar).pack(pady=10)

# # infinite loop
# mainloop()

# import tkinter as tk


# class Demo1:
#     def __init__(self, master):
#         self.master = master
#         self.frame = tk.Frame(self.master)
#         self.button1 = tk.Button(
#             self.frame, text='New Window', width=25, command=self.new_window)
#         self.button1.pack()
#         self.frame.pack()

#     def new_window(self):
#         self.newWindow = tk.Toplevel(self.master)
#         self.app = Demo2(self.newWindow)


# class Demo2:
#     def __init__(self, master):
#         self.master = master
#         self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(
#             self.frame, text='Quit', width=25, command=self.close_windows)
#         self.quitButton.pack()
#         self.frame.pack()

#     def close_windows(self):
#         self.master.destroy()


# def main():
#     root = tk.Tk()
#     app = Demo1(root)
#     root.mainloop()


# if __name__ == '__main__':
#     main()
import tkinter as tk


# class window2:
#     def __init__(self, master1):
#         self.panel2 = tk.Frame(master1)
#         self.panel2.grid()
#         self.button2 = tk.Button(
#             self.panel2, text="Quit", command=self.panel2.quit)
#         self.button2.grid()

#         vcmd = (master1.register(self.validate),
#                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
#         self.text1 = tk.Entry(self.panel2, validate='key',
#                               validatecommand=vcmd)
#         self.text1.grid()
#         self.text1.focus()

#     def validate(self, action, index, value_if_allowed,
#                  prior_value, text, validation_type, trigger_type, widget_name):
#         if value_if_allowed:
#             try:
#                 float(value_if_allowed)
#                 return True
#             except ValueError:
#                 return False
#         else:
#             return False


# root1 = tk.Tk()
# window2(root1)
# root1.mainloop()

import tkinter as tk
from tkinter import ttk


def about_window():
    top2 = tk.Toplevel(root)
    top2.title("About")
    top2.resizable(0, 0)

    explanation = "This program is my test program"

    ttk.Label(top2, justify=tk.LEFT, text=explanation).pack(padx=5, pady=2)
    ttk.Button(top2, text='OK', width=10, command=top2.destroy).pack(pady=8)

    top2.transient(root)
    top2.grab_set()
    root.wait_window(top2)


root = tk.Tk()
root.resizable(0, 0)

root.style = ttk.Style()
# ('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")

menu = tk.Menu(root)
root.config(menu=menu)

fm = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Settings", menu=fm)
fm.add_command(label="Preferances")

hm = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=hm)
hm.add_command(label="About", command=about_window)
hm.add_command(label="Exit", command=root.quit)
#

tk.mainloop()
