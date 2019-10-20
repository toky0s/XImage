from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.ttk import *
from CallTipWindow import createToolTip
from urllib import request
from PIL import Image, ImageTk
import os
import requests
import json
import time


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


class DownloadInfomationToplevelWindow(Toplevel):

    def __init__(self, master=None, option=()):
        super().__init__(master=master)
        self.master = master
        self.option = option
        self.setupUI()

    def setupUI(self):
        self.title('Download information')
        label_title = Label(self, text='Download information',
                            anchor=CENTER, foreground='white', background='#2c3e50')
        label_title.grid(row=0,column=0, columnspan=6)

        self.progress = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.grid(row=0, column=0, columnspan=5,sticky='we')
        
        self.var_progress = StringVar()
        self.var_progress.set('0%')
        self.label_show_progress = Label(self,textvariable=self.var_progress, anchor=CENTER)
        self.label_show_progress.var = self.var_progress
        self.label_show_progress.grid(row=0, column=5, sticky='we')

        self.label_query = Label(self,text='Query:')
        self.label_query.grid(row=1, column=0, sticky='w')

        self.var_entry_query=StringVar()
        self.entry_query = Entry(
            self, textvariable=self.var_entry_query, state='readonly')
        self.entry_query.grid(row=1, column=1, sticky='w')

        self.label_total = Label(self, text='Total:')
        self.label_total.grid(row=1, column=2, sticky='w')

        self.var_entry_total = IntVar()
        self.entry_total = Entry(
            self, textvariable=self.var_entry_total, state='readonly')
        self.entry_total.grid(row=1, column=3, sticky='w')

        self.label_total_page = Label(self, text='Total pages:')
        self.label_total_page.grid(row=1, column=4, sticky='w')

        self.var_entry_total_pages = IntVar()
        self.entry_total_page = Entry(
            self, textvariable=self.var_entry_total_pages, state='readonly')
        self.entry_total_page.grid(row=1, column=5, sticky='w')

        self.label_image_downloaded = Label(self)
        self.label_image_downloaded.grid(row=2, column=0, columnspan=6, sticky='wesn')

    def download(self):
        if  self.option[2] == 'https://unsplash.com/napi/search/photos':
            r = requests.get(self.option[2], params=self.option[3])
            if r.status_code == 200:
                # get urls based on quality
                j = json.loads(r.text)
                total = j['total']
                total_pages = j['total_pages']
                results = j['results']

                self.var_entry_query.set(self.option[3]['query'])
                self.var_entry_total.set(total)
                self.var_entry_total_pages.set(total_pages)

                self.entry_query.update_idletasks()
                self.entry_total.update_idletasks()
                self.entry_total_page.update_idletasks()

                for i in results:
                    name = i['id']
                    url = i['urls'][self.option[1]]
                    time.sleep(1)
                    request.urlretrieve(url, self.option[0]+'/'+name+'.jpg')
                    self.progress['value'] += 100/len(results)
                    self.var_progress.set('{}%'.format(self.progress['value']))

                    # show image downloaded
                    image = Image.open(self.option[0]+'/'+name+'.jpg')
                    self.photo = ImageTk.PhotoImage(image)
                    self.label_image_downloaded.config(image=self.photo)
                    self.label_image_downloaded.image = self.photo

                    self.label_image_downloaded.update_idletasks()
                    self.label_show_progress.update_idletasks()
                    self.progress.update_idletasks()

                self.message_done = messagebox.showinfo('Info', 'Done')

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
        # check valid value
        if os.path.isdir(self.var_folder_name.get()):
            self.show_download_info_window()
        else:
            if self.var_folder_name.get() == '':
                message_please_enter_path = messagebox.showwarning('Warning','Please enter a path, where save images')
            elif os.path.isdir(self.var_folder_name.get()) == False:
                message_folder_is_not_exist = messagebox.showwarning('Warning','Path is not exist')
            
    def choice_request(self):
        if self.var_random == '1':
            # call random request
            pass
        else:
            if self.var_name.get() == '':
                # call listPhotos request
                pass
            else:
                # call searchPhoto request
                request = 'https://unsplash.com/napi/search/photos'
                params = {'query': self.var_name.get(
                ), 'page': self.var_page_number.get(), 'per_page': self.var_amount.get()}
                folder_name = self.var_folder_name.get()
                quality = self.var_quality_rb.get()
                return (folder_name,quality,request,params)

    def show_download_info_window(self):
        download_info = DownloadInfomationToplevelWindow(master=self.master,option=self.choice_request())
        self.master.after(1000,download_info.download)

        download_info.transient(self.master)
        download_info.grab_set()
        self.master.wait_window(download_info)


def main_UnsplashUI():
    master = Tk()
    ui = UnsplashUI(master)
    ui.pack()
    master.mainloop()

if __name__ == '__main__':
    # main_DownloadInformationUI()
    main_UnsplashUI()
