from tkinter import filedialog, messagebox
from tkinter import *
import os
import clipboard


def is_check():
    if is_all_var.get()==1:
        number_download_label.config(state=DISABLED)
        number_download_textbox.config(state=DISABLED)
    else:
        number_download_label.config(state=NORMAL)
        number_download_textbox.config(state=NORMAL)

def is_404():
    pass

def open_folder():
    folder_name = filedialog.askdirectory()
    folder_path_text.set(folder_name)

def check_path():
    if os.path.exists(folder_path_text.get()):
        pass # goto download
    else:
        if folder_path_text.get()=='':
            messagebox.showwarning('Warning','Please enter path!')
        elif messagebox.askyesno('Warning', 'The path does not exist, do you want create a new folder?'):
            print('create new folder {}'.format(folder_path_text.get()))
            messagebox.showinfo('Info', '{}'.format(folder_path_text.get()))

# Master========================================================
master = Tk()

master.title('ImageThief')
master.geometry('450x200')
master.iconbitmap('bandit.ico')
master.resizable(0, 0)

# Label=========================================================
frame = Frame(master, background='#229954', height=30, width=450)
frame.grid(row=0, column=0, columnspan=3)
frame.grid_propagate(0)
frame.update()
l = Label(master, background='#229954', text='Image Thief', foreground='white')
l.grid(row=0,column=0,columnspan=3)

folder_label = Label(master, text='Save at:')
folder_label.grid(row=1,sticky=W)

urls_label = Label(master, text='Url:')
urls_label.grid(row=2, sticky=W)

number_download_label = Label(master, text='How much:')
number_download_label.grid(row=3, sticky=W)

# Entry========================
folder_path_text = StringVar()
folder_path_textbox = Entry(master, textvariable=folder_path_text,width=30)
folder_path_textbox.grid(row=1, column=1, sticky=W)

urls_textbox = Entry(master, width=30)
urls_textbox.grid(row=2, column=1, sticky=W)

number_download_textbox = Entry(master, width=30)
number_download_textbox.grid(row=3, column=1,sticky=W)

# Button=================================
open_icon = PhotoImage(file='folder.png')
open_icon_image = open_icon.subsample(1,1)
open_folder_button = Button(master, text='Open', image=open_icon_image, compound=LEFT, width =115, command=open_folder)
open_folder_button.grid(row=1,column=2)

download_icon = PhotoImage(file='down-arrow.png')
download_icon_image = download_icon.subsample(1,1)
download_bt = Button(master, text='Download now!',
                     image=download_icon_image, compound=LEFT, width=115)
download_bt.config(command=check_path)
download_bt.grid(row=2, column=2)

is_all_var = IntVar()
is_all_checkbutton = Checkbutton(master,text='All',variable=is_all_var, command=is_check)
is_all_checkbutton.grid(row=4,column=1,sticky=W)

master.mainloop()
