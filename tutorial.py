# importing tkinter module
from time import sleep
import tkinter
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

# Button(root, text='Start', command=bar).pack(pady=10)

# mainloop()


main = tkinter.Tk()
txt = tkinter.Text(main)
txt.grid()


def update_txt(event=None):
    vals = ['This is some text.',
            'This is some more.',
            'Blah blah blah']
    i = 0
    while i < len(vals):
        txt.delete('1.0', 'end')
        txt.insert('1.0', vals[i])
        txt.update_idletasks()
        sleep(2)
        i = i+1

main.after(1000, update_txt)
main.mainloop()
