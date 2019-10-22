# python 3
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from bs4 import BeautifulSoup
from urllib import request
from unsplash import GraphicRiver
import requests
import time

class GraphicRiverUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):

        # row 0
        self.label_url = Label(self,text='Url:')
        self.label_url.grid(row=0, column=0, sticky='w')

        self.var_url = StringVar()
        self.entry_url = Entry(self, textvariable=self.var_url)
        self.entry_url.grid(row=0, column=1, sticky='we')

        # row 1
        self.label_save = Label(self, text='Save:')
        self.label_save.grid(row=1, column=0, sticky='w')

        self.var_folder_name = StringVar()
        self.entry_save = Entry(self, textvariable=self.var_folder_name)
        self.entry_save.grid(row=1, column=1, sticky='we')

        self.button_browse = Button(self, text='Browse', command=self.choice_folder)
        self.button_browse.grid(row=1, column=2, sticky='we')

        # row 2
        self.label_amount = Label(self, text = 'Amount:')
        self.label_amount.grid(row=2, column=0, sticky='w')

        self.var_amount = IntVar()
        self.entry_amount = Entry(self)
        self.entry_amount.grid(row=2, column=1, sticky='we')

        # row 3
        self.button_download = Button(self,text='Download', command = self.download)
        self.button_download.grid(row=3, column=1, sticky= 'we')

        self.button_usage = Button(self, text='Usage', command= self.change_ui)
        self.button_usage.grid(row=3, column=2, sticky='we')

        # row 4
        self.label_download = Label(self, text='Download')
        self.label_download.config(
            anchor='center', background='#27ae60', foreground='white')
        self.label_download.grid(row=4, column=0, columnspan=3, sticky='we')
        self.label_download.grid_forget()

        # row 5
        self.var_progress = StringVar()
        self.label_progress = Label(self, textvariable=self.var_progress)
        self.label_progress.grid(row=5, column=0)
        self.label_progress.grid_forget()

        self.progress_bar = Progressbar(self)
        self.progress_bar.config(
            length=100, orient='horizontal', mode='determinate')
        self.progress_bar.grid(row=5, column=1, columnspan=2, sticky='we')
        self.progress_bar.grid_forget()

        # row 6
        self.label_image = Label(self, text='hi')
        self.label_image.grid(row=6, column=0, columnspan=3)
        self.label_image.grid_forget()

    def choice_folder(self):
        dialog_choice_folder = filedialog.askdirectory()
        self.var_folder_name.set(dialog_choice_folder)

    def get_name_presentation(self):
        self.name_presentation = 'Name Presentation'
        # process it
        return self.name_presentation

    def change_ui(self):
        self.self.label_download.grid()
        self.label_progress.grid()
        self.progress_bar.grid()
        self.label_image.grid()

    def download(self):
        self.master.after(100, self.download)
        for i in range(10):
            self.var_progress.set(i)
            self.label_progress.update_idletasks()
            time.sleep(0.5)

    def show_usage(self):
        self.usage_popup_window = Toplevel(self)
        self.usage_frame = FrameUsage(self.usage_popup_window)
        self.usage_frame.pack()


class FrameUsage(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.label_title = Label(self, text='Usage')
        self.label_title.pack()

        
class GraphicRiverEdit(GraphicRiver):

    def __init__(self, folder_path):
        self.path = folder_path
