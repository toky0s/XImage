# from tkinter import filedialog, messagebox
# # from tkinter import *
# from tkinter.ttk import *
# from urllib import request
# from PIL import Image, ImageTk

from CallTipWindow import createToolTip
from frame_download import FrameDownload

import os
import requests
import json
import time

from tkinter import messagebox, filedialog, StringVar, IntVar, PhotoImage, Tk, Toplevel
from tkinter.ttk import Label, Progressbar, Entry, Frame, Radiobutton, Button, Checkbutton
from PIL import Image, ImageTk
from urllib import request

import json
import time
import requests

class FrameGroupRadiobutton(Frame):

    def __init__(self, master=None, side='left', variable=None, dict_option={}, initialize=""):
        super().__init__(master=master)
        self.side = side
        self.variable = variable
        self.dict_option = dict_option
        self.initialize = initialize
        self.setupUI()

    def setupUI(self):

        self.variable.set(self.initialize)  # initialize
        for text, value in self.dict_option.items():
            radiobt_quality = Radiobutton(
                self, text=text, variable=self.variable, value=value)
            radiobt_quality.pack(side=self.side, anchor='w')


class DownloadInfomation(Toplevel):

    def __init__(self, master=None, option=()):
        super().__init__(master=master)
        self.master = master
        self.option = option
        self.frame = FrameDownload(self,self.option)
        self.frame.pack()

class UnsplashUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.label_name = Label(self, text='Query:')
        self.label_name.grid(row=0, column=0, sticky='w')

        self.label_amount = Label(self, text='Per page:')
        self.label_amount.grid(row=1, column=0, sticky='w')

        self.label_page_number = Label(self, text='Page:')
        self.label_page_number.grid(row=2, column=0, sticky='w')

        label_save = Label(self, text='Save:')
        label_save.grid(row=3, column=0, sticky='w')

        label_quality = Label(self, text='Quality:')
        label_quality.grid(row=4, column=0, sticky='w')

        self.label_order_by = Label(self, text='Order by:')
        self.label_order_by.grid(row=5, column=0, sticky='w')

        label_random = Label(self, text='Random:')
        label_random.grid(row=6, column=0, sticky='w')

        self.var_name = StringVar()
        self.entry_name = Entry(self, textvariable=self.var_name)
        self.entry_name.grid(row=0, column=1, sticky='we')

        self.var_amount = IntVar()
        self.var_amount.set(10)
        self.entry_amount = Entry(self, textvariable=self.var_amount)
        self.entry_amount.grid(row=1, column=1, sticky='we')

        self.var_page_number = IntVar()
        self.var_page_number.set(1)
        self.entry_page_number = Entry(self, textvariable=self.var_page_number)
        self.entry_page_number.grid(row=2, column=1, sticky='we')

        self.var_folder_name = StringVar()
        entry_save = Entry(self, textvariable=self.var_folder_name)
        entry_save.grid(row=3, column=1, sticky='we')

        button_browse = Button(self, text='Browse', command=self.choice_folder)
        button_browse.grid(row=3, column=2, sticky='we')

        QUALITIES = {
            'Raw': 'raw',
            'Regular': 'regular',
            'Small': 'small',
            'Thumnail': 'thumnail',
        }

        self.var_quality_rb = StringVar()
        group_quality_radiobutton = FrameGroupRadiobutton(
            self, side='left', variable=self.var_quality_rb, dict_option=QUALITIES, initialize='raw')
        group_quality_radiobutton.grid(row=4, column=1, sticky='w')

        ORDER_BY = {
            'Latest': 'latest',
            'Oldest': 'oldest',
            'Popular': 'popular',
        }

        self.var_order_by_rb = StringVar()
        self.group_order_by_radiobutton = FrameGroupRadiobutton(
            self, side='left', variable=self.var_order_by_rb, dict_option=ORDER_BY, initialize='latest')
        self.group_order_by_radiobutton.grid(row=5, column=1, sticky='w')

        self.var_random = IntVar()
        checkbutton_random = Checkbutton(
            self, variable=self.var_random, command=self.disable_order_by_for_random)
        checkbutton_random.grid(row=6, column=1, sticky='w')
        createToolTip(checkbutton_random, 'Max amount is 30')

        image_icon_download = PhotoImage(file='icon/down-arrow.png')
        button_download = Button(self, text='Download now!', image=image_icon_download,
                                 compound='left', command=self.check_paramenter_is_valid)
        button_download.image = image_icon_download
        button_download.grid(row=7, column=1)

    def disable_order_by_for_random(self):
        if self.var_random.get() == 1:
            self.label_order_by.config(state='disable')
            self.label_name.config(state='disable')
            self.entry_name.config(state='disable')
            self.label_page_number.config(state='disable')
            self.entry_page_number.config(state='disable')
            for child in self.group_order_by_radiobutton.winfo_children():
                child.config(state='disable')
        else:
            self.label_order_by.config(state='normal')
            self.label_name.config(state='normal')
            self.entry_name.config(state='normal')
            self.label_page_number.config(state='normal')
            self.entry_page_number.config(state='normal')
            for child in self.group_order_by_radiobutton.winfo_children():
                child.config(state='normal')

    def choice_folder(self):
        dialog_choice_folder = filedialog.askdirectory()
        self.var_folder_name.set(dialog_choice_folder)

    def check_paramenter_is_valid(self):
        # check valid value
        if os.path.isdir(self.var_folder_name.get()):
            self.show_download_info_window()
        else:
            if self.var_folder_name.get() == '':
                message_please_enter_path = messagebox.showwarning(
                    'Warning', 'Please enter a path, where save images')
            elif os.path.isdir(self.var_folder_name.get()) == False:
                message_folder_is_not_exist = messagebox.showwarning(
                    'Warning', 'Path is not exist')

    def choice_request(self):
        if self.var_random.get() == 1:
            # call random request
            request = 'https://unsplash.com/napi/photos/random'
            params = {'count': self.var_amount.get()}
            folder_name = self.var_folder_name.get()
            quality = self.var_quality_rb.get()
            return (folder_name, quality, request, params)
        else:
            if self.var_name.get() == '':
                request = 'https://unsplash.com/napi/photos'
                params = params = {'query': self.var_name.get(),
                    'page': self.var_page_number.get(), 'per_page': self.var_amount.get()}
                folder_name = self.var_folder_name.get()
                quality = self.var_quality_rb.get()
                return (folder_name, quality, request, params)
            else:
                # call searchPhoto request
                request = 'https://unsplash.com/napi/search/photos'
                params = {'query': self.var_name.get(
                ), 'page': self.var_page_number.get(), 'per_page': self.var_amount.get()}
                folder_name = self.var_folder_name.get()
                quality = self.var_quality_rb.get()
                return (folder_name, quality, request, params)

    def show_download_info_window(self):
        download_info = DownloadInfomation(
            master=self.master, option=self.choice_request())

        self.after(100, download_info.frame.change_ui)

        download_info.transient(self.master)
        download_info.grab_set()
        self.master.wait_window(download_info)


def main_UnsplashUI():
    master = Tk()
    ui = UnsplashUI(master)
    ui.pack()
    master.mainloop()


if __name__ == '__main__':
    main_UnsplashUI()
