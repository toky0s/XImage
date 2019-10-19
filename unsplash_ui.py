from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.ttk import *
from CallTipWindow import createToolTip
from urllib import request
import os
import requests
import logging
import json
import time



logging.basicConfig(level=logging.INFO)

class FrameGroupRadiobutton(Frame):

    def __init__(self, master=None, side=LEFT, variable=None, dict_option={}, initialize=""):
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
            radiobt_quality.pack(side=self.side, anchor=W)

    def disableGroup(self):
        list_widget = self.pack_slaves()
        for i in list_widget:
            i.state=DISABLED

class DownloadInfomationUI(Frame):

    def __init__(self, master=None, save='', requests='', params={}):
        super().__init__(master=master)
        self.save = save
        self.request = request
        self.params = params
        self.setupUI()

    def setupUI(self):

        progress = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')
        progress.grid(row=0, column=0, columnspan=5,sticky='we')
        
        var_progress = StringVar()
        var_progress.set('0%')
        label_show_progress = Label(self,textvariable=var_progress, anchor=CENTER)
        label_show_progress.var = var_progress
        label_show_progress.grid(row=0, column=5, sticky='we')

        label_query = Label(self,text='Query:')
        label_query.grid(row=1,column=0, sticky='w')

        entry_query = Entry(self)
        entry_query.grid(row=1,column=1, sticky='w')

        label_total = Label(self,text='Total:')
        label_total.grid(row=1,column=2, sticky='w')

        entry_total = Entry(self)
        entry_total.grid(row=1,column=3, sticky='w')

        label_total_page = Label(self,text='Total pages:')
        label_total_page.grid(row=1,column=4, sticky='w')

        entry_total_page = Entry(self)
        entry_total_page.grid(row=1,column=5, sticky='w')

        image_downloaded = PhotoImage(file='icon/folder.png')
        label_image_downloaded = Label(self,image=image_downloaded)
        label_image_downloaded.image = image_downloaded
        label_image_downloaded.grid(row=2,column=0)
    
    def download(self):
        r = requests.get(self.request, params=self.params)
        if r.status_code == 200:
            # get urls based on quality
            j = json.loads(r.text)
            results = j['results']
            for i in results:
                name = i['id']
                url = i['urls'][self.var_quality_rb]
                time.sleep(1)
                request.urlretrieve(self.save, self.path+'/'+name+'.jpg')


class DownloadInfomationToplevelWindow(Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.title('Download information')
        label_title = Label(self, text='Download information',
                            anchor=CENTER, foreground='white', background='#2c3e50')
        label_title.pack(fill=X)

        self.transient()
        self.grab_set()


class UnsplashUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.label_name = Label(self, text='Query:')
        self.label_name.grid(row=0, column=0, sticky=W)

        self.label_amount = Label(self, text='Per page:')
        self.label_amount.grid(row=1, column=0, sticky=W)

        self.label_page_number = Label(self,text='Page:')
        self.label_page_number.grid(row=2, column=0, sticky=W)

        label_save = Label(self, text='Save:')
        label_save.grid(row=3, column=0, sticky=W)

        label_quality = Label(self, text='Quality:')
        label_quality.grid(row=4, column=0, sticky=W)

        self.label_order_by = Label(self, text='Order by:')
        self.label_order_by.grid(row=5, column=0, sticky=W)

        label_random = Label(self, text='Random:')
        label_random.grid(row=6, column=0, sticky=W)


        self.var_name = StringVar()
        self.entry_name = Entry(self, textvariable=self.var_name)
        self.entry_name.grid(row=0, column=1, sticky='we')

        self.var_amount = IntVar()
        self.var_amount.set(10)
        self.entry_amount = Entry(self, textvariable=self.var_amount)
        self.entry_amount.grid(row=1, column=1, sticky='we')

        self.var_page_number = IntVar()
        self.var_page_number.set(1)
        self.entry_page_number = Entry(self,textvariable=self.var_page_number)
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
            self, side=LEFT, variable=self.var_quality_rb, dict_option=QUALITIES, initialize='raw')
        group_quality_radiobutton.grid(row=4, column=1, sticky=W)

        ORDER_BY = {
            'Latest': 'latest',
            'Oldest': 'oldest',
            'Popular': 'popular',
        }
        
        self.var_order_by_rb = StringVar()
        self.group_order_by_radiobutton = FrameGroupRadiobutton(
            self, side=LEFT, variable=self.var_order_by_rb, dict_option=ORDER_BY, initialize='latest')
        self.group_order_by_radiobutton.grid(row=5, column=1, sticky=W)

        self.var_random = IntVar()
        checkbutton_random = Checkbutton(self,variable = self.var_random, command=self.disable_order_by_for_random)
        checkbutton_random.grid(row=6, column=1, sticky=W)
        createToolTip(checkbutton_random,'Max amount is 30')

        image_icon_download = PhotoImage(file='icon/down-arrow.png')
        button_download = Button(self, text='Download now!',image=image_icon_download,compound=LEFT, command=self.check_paramenter_is_valid)
        button_download.image = image_icon_download
        button_download.grid(row=7, column=1)

    def disable_order_by_for_random(self):
        if self.var_random.get() == 1:
            self.label_order_by.config(state=DISABLED)
            self.label_name.config(state=DISABLED)
            self.entry_name.config(state=DISABLED)
            self.label_page_number.config(state=DISABLED)
            self.entry_page_number.config(state=DISABLED)
            for child in self.group_order_by_radiobutton.winfo_children():
                child.config(state=DISABLED)
        else:
            self.label_order_by.config(state=NORMAL)
            self.label_name.config(state=NORMAL)
            self.entry_name.config(state=NORMAL)
            self.label_page_number.config(state=NORMAL)
            self.entry_page_number.config(state=NORMAL)
            for child in self.group_order_by_radiobutton.winfo_children():
                child.config(state=NORMAL)

    def choice_folder(self):
        dialog_choice_folder = filedialog.askdirectory()
        self.var_folder_name.set(dialog_choice_folder)

    def check_paramenter_is_valid(self):
        # choice requests
        # query empty --> listPhotos
        if self.var_name.get() != '':
            pass
        # check valid value
        if os.path.isdir(self.var_folder_name.get()):
            self.download()
        else:
            if self.var_folder_name.get() == '':
                message_please_enter_path = messagebox.showwarning('Warning','Please enter a path, where save images')
            elif os.path.isdir(self.var_folder_name.get()) == False:
                message_folder_is_not_exist = messagebox.showwarning('Warning','Path is not exist')
            

    def download(self):
        download_info_toplevel_window = DownloadInfomationToplevelWindow(self)
        download_info_ui = DownloadInfomationUI(download_info_toplevel_window,save=self.var_folder_name)
        download_info_ui.pack()

        
def main_DownloadInformationUI():
    master = Tk()
    ui = DownloadInfomationUI(master)
    ui.pack()
    master.mainloop()


def main_UnsplashUI():
    master = Tk()
    ui = UnsplashUI(master)
    ui.pack()
    master.mainloop()

if __name__ == '__main__':
    # main_DownloadInformationUI()
    main_UnsplashUI()
