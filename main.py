# complete code here
from CallTipWindow import createToolTip

from tkinter import messagebox, filedialog, StringVar, IntVar, PhotoImage, Tk, Toplevel
from tkinter.ttk import Label, Progressbar, Entry, Frame, Radiobutton, Button, Checkbutton
from PIL import Image, ImageTk
from urllib import request
from bs4 import BeautifulSoup

import os
import json
import requests
import time
import shutil

# unsplash


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


class FrameDownload(Frame):

    def __init__(self, master=None, option=()):
        super().__init__(master=master)
        self.master = master
        self.master.title('Download information')
        self.option = option
        self.LIST = 'https://unsplash.com/napi/photos'
        self.RANDOM = 'https://unsplash.com/napi/photos/random'
        self.SEARCH = 'https://unsplash.com/napi/search/photos'
        self.setupUI()

    def setupUI(self):
        # build UI base on URLS
        if self.option[2] == self.SEARCH:
            # title window
            label_title = Label(self, text='Search Photos')
            label_title.config(
                anchor='center', foreground='white', background='#8e44ad')
            label_title.grid(row=0, column=0, columnspan=6, sticky='we')

            # progress
            self.progress = Progressbar(self)
            self.progress.config(orient='horizontal',
                                 length=100, mode='determinate')
            self.progress.grid(row=2, column=0, columnspan=5, sticky='we')

            self.var_progress = StringVar()
            self.var_progress.set('0%')
            self.label_show_progress = Label(self)
            self.label_show_progress.config(
                textvariable=self.var_progress, anchor='center')
            self.label_show_progress.var = self.var_progress
            self.label_show_progress.grid(row=2, column=5, sticky='w')

            # query
            self.label_query = Label(self, text='Query')
            self.label_query.grid(row=1, column=0, sticky='e')

            self.var_entry_query = StringVar()
            self.entry_query = Entry(self)
            self.entry_query.config(
                textvariable=self.var_entry_query, state='readonly')
            self.entry_query.grid(row=1, column=1, sticky='w')

            # total
            self.var_total = StringVar()
            self.var_total.set('Total')
            self.label_total = Label(self, textvariable=self.var_total)
            self.label_total.grid(row=1, column=2, sticky='e')

            self.var_entry_total = IntVar()
            self.entry_total = Entry(self)
            self.entry_total.config(
                textvariable=self.var_entry_total, state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')

            # total pages
            self.label_total_page = Label(self, text='Total pages:')
            self.label_total_page.grid(row=1, column=4, sticky='e')

            self.var_entry_total_pages = IntVar()
            self.entry_total_page = Entry(self)
            self.entry_total_page.config(
                textvariable=self.var_entry_total_pages, state='readonly')
            self.entry_total_page.grid(row=1, column=5, sticky='w')

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
            self.label_image_downloaded.grid(
                row=3, column=0, columnspan=6, sticky='wesn')

            # self.change_ui()

        elif self.option[2] == self.LIST:
            # title window
            label_title = Label(self, text='List of Photos')
            label_title.config(
                anchor='center', foreground='white', background='#2c3e50')
            label_title.grid(row=0, column=0, columnspan=4, sticky='we')

            # progress
            self.progress = Progressbar(self)
            self.progress.config(orient='horizontal',
                                 length=100, mode='determinate')
            self.progress.grid(row=2, column=0, columnspan=3, sticky='we')

            self.var_progress = StringVar()
            self.var_progress.set('0%')
            self.label_show_progress = Label(self)
            self.label_show_progress.config(
                textvariable=self.var_progress, anchor='center')
            self.label_show_progress.var = self.var_progress
            self.label_show_progress.grid(row=2, column=3, sticky='w')

            # query
            self.label_query = Label(self, text='Query:')
            self.label_query.grid(row=1, column=0, sticky='e')

            self.entry_query = Entry(self)
            self.entry_query.insert(0, 'LIST')
            self.entry_query.config(state='readonly')
            self.entry_query.grid(row=1, column=1, sticky='w')

            # amount
            self.label_total = Label(self, text='Amount:')
            self.label_total.grid(row=1, column=2, sticky='e')

            self.entry_total = Entry(self)
            self.entry_total.insert(0, self.option[3]['per_page'])
            self.entry_total.config(state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
            self.label_image_downloaded.grid(
                row=3, column=0, columnspan=4, sticky='wesn')

            # self.change_ui()

        elif self.option[2] == self.RANDOM:
            # title window
            label_title = Label(self, text='Random Photos')
            label_title.config(
                anchor='center', foreground='white', background='#16a085')
            label_title.grid(row=0, column=0, columnspan=4, sticky='we')

            # progress
            self.progress = Progressbar(self)
            self.progress.config(orient='horizontal',
                                 length=100, mode='determinate')
            self.progress.grid(row=2, column=0, columnspan=3, sticky='we')

            self.var_progress = StringVar()
            self.var_progress.set('0%')
            self.label_show_progress = Label(self)
            self.label_show_progress.config(
                textvariable=self.var_progress, anchor='center')
            self.label_show_progress.var = self.var_progress
            self.label_show_progress.grid(row=2, column=3, sticky='w')

            # query
            self.label_query = Label(self, text='Query')
            self.label_query.grid(row=1, column=0, sticky='e')

            self.entry_query = Entry(self)
            self.entry_query.insert(0, 'RANDOM')
            self.entry_query.config(state='readonly')
            self.entry_query.grid(row=1, column=1, sticky='w')

            # amount
            self.label_total = Label(self, text='Amount')
            self.label_total.grid(row=1, column=2, sticky='e')

            self.var_entry_total = IntVar()
            if self.option[3]['count'] > 30:
                self.var_entry_total.set(30)
            else:
                self.var_entry_total.set(self.option[3]['count'])
            self.entry_total = Entry(self)
            self.entry_total.config(
                textvariable=self.var_entry_total, state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
            self.label_image_downloaded.grid(
                row=3, column=0, columnspan=4, sticky='wesn')

    def change_ui(self):
        if self.option[2] == self.SEARCH:
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

        # random photos
        elif self.option[2] == self.RANDOM:
            r = requests.get(self.option[2], params=self.option[3])
            if r.status_code == 200:

                # get result
                j = json.loads(r.text)
                results = j

        elif self.option[2] == self.LIST:
            r = requests.get(self.option[2], params=self.option[3])
            if r.status_code == 200:

                # get result
                j = json.loads(r.text)
                results = j

        self.download(results)

    def download(self, results):
        for i in results:
            name = i['id']
            url = i['urls'][self.option[1]]
            time.sleep(1)  # delay time to send request
            try:
                request.urlretrieve(url, self.option[0]+'/'+name+'.jpg')
            except Exception as x:  # re download if have a problem
                print('have problem', x)
                time.sleep(1)

            self.progress['value'] += 100/len(results)
            self.var_progress.set('{}%'.format(self.progress['value']))

            # show image downloaded
            image = Image.open(self.option[0]+'/'+name+'.jpg')
            width = int(self.winfo_width())
            height = int(width*image.height/image.width)
            self.photo = ImageTk.PhotoImage(
                image.resize((width, height), Image.ANTIALIAS))
            self.label_image_downloaded.config(image=self.photo)
            self.label_image_downloaded.image = self.photo

            self.progress.update_idletasks()

        self.message_done = messagebox.showinfo('Info', 'Done')
        self.master.destroy()


class DownloadInfomation(Toplevel):

    def __init__(self, master=None, option=()):
        super().__init__(master=master)
        self.master = master
        self.option = option
        self.frame = FrameDownload(self, self.option)
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
            'Full': 'full',
            'Regular': 'regular',
            'Small': 'small',
            'Thumnail': 'thumb',
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
                params = params = {
                    'page': self.var_page_number.get(), 'per_page': self.var_amount.get()}
                folder_name = self.var_folder_name.get()
                quality = self.var_quality_rb.get()
                return (folder_name, quality, request, params)
            else:
                # call searchPhoto request
                request = 'https://unsplash.com/napi/search/photos'
                params = {
                    'query': self.var_name.get(),
                    'page': self.var_page_number.get(),
                    'per_page': self.var_amount.get()
                }
                folder_name = self.var_folder_name.get()
                quality = self.var_quality_rb.get()
                return (folder_name, quality, request, params)

    def show_download_info_window(self):
        download_info = DownloadInfomation(
            master=self.master, option=self.choice_request())

        download_info.after(100, download_info.frame.change_ui)

        # download_info.transient(self.master)
        # download_info.grab_set()
        # self.master.wait_window(download_info)

        # fix bug render toplevel when active it or it's parent widget


class GraphicRiverUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.list_tag_a = []  # this list will contain <a> tags
        self.setupUI()

    def setupUI(self):

        # row 0
        self.label_url = Label(self, text='Url:')
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

        self.button_browse = Button(
            self, text='Browse', command=self.choice_folder)
        self.button_browse.grid(row=1, column=2, sticky='we')

        # row 2
        self.label_amount = Label(self, text='Amount:')
        self.label_amount.grid(row=2, column=0, sticky='w')

        self.var_amount = IntVar()
        self.entry_amount = Entry(self, textvariable=self.var_amount)
        self.entry_amount.grid(row=2, column=1, sticky='we')

        # row 3
        self.button_download = Button(
            self, text='Download', command=self.change_ui)
        self.button_download.grid(row=3, column=1, sticky='we')

        self.button_usage = Button(
            self, text='Usage', command=self.show_user_manual)
        self.button_usage.grid(row=3, column=2, sticky='we')

        # HIDE===========================================
        # row 4
        self.label_download = Label(self, text='Download')
        self.label_download.config(
            anchor='center', background='#27ae60', foreground='white')

        # row 5
        self.var_progress = StringVar()
        self.label_progress = Label(self, textvariable=self.var_progress)

        self.progress_bar = Progressbar(self)
        self.progress_bar.config(
            length=100, orient='horizontal', mode='determinate')

        # row 6
        self.label_image = Label(self, text='hi')

    def choice_folder(self):
        dialog_choice_folder = filedialog.askdirectory()
        self.var_folder_name.set(dialog_choice_folder)

    def get_name_presentation(self):
        self.name_presentation = 'Name Presentation'
        # process it
        return self.name_presentation

    def change_ui(self):
        self.label_download.grid(row=4, column=0, columnspan=3, sticky='we')
        self.label_progress.grid(row=5, column=0)
        self.progress_bar.grid(row=5, column=1, columnspan=2, sticky='we')
        self.label_image.grid(row=6, column=0, columnspan=3)
        self.master.after(1000, self.get_list_tag_a)
        self.master.after(1000, self.download)

    def __has_a_http_jpg(self, tag):
        # check image's link is https://www.somthing.jpg
        if (tag['class'] == 'is-hidden') and (tag.name == 'a') and (('.jpg' == tag['href'][-4:len(tag['href'])])or('.JPG' == tag['href'][-4:len(tag['href'])])):
            return True

    def get_list_tag_a(self):
        # return a list, which containe <a> tags
        r = requests.get(self.var_url.get())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            # get link to download
            div = soup.find(class_='js- item-preview-image__gallery')
            soup = BeautifulSoup(str(div), 'lxml')
            list_tag_a = soup.find_all(
                'a', limit=self.var_amount.get())  # set limit to download
            for i in list_tag_a:
                self.list_tag_a.append(i['href'])

    def download(self):
        # https:, ,graphicriver.net, item, i9-template-system, 10955645
        # create dir, where contain images
        dir_name = self.var_url.get().split('/')[4]
        if os.path.exists(self.var_folder_name.get()+'/'+dir_name):
            shutil.rmtree(self.var_folder_name.get()+'/'+dir_name)

        full_path_save = self.var_folder_name.get()+'/'+dir_name
        os.mkdir(full_path_save)

        per = 0
        for i in self.list_tag_a:
            name_image = i.split('/')[-1]
            request.urlretrieve(i, full_path_save+'/'+name_image)

            image_downloaded = Image.open(full_path_save+'/'+name_image)
            width = int(self.winfo_width())
            height = int(width*image_downloaded.height /
                         image_downloaded.width)

            image_complete = ImageTk.PhotoImage(
                image_downloaded.resize((width, height), Image.ANTIALIAS))
            self.label_image.config(image=image_complete)
            self.label_image.image = image_complete

            per = per + 100/self.var_amount.get()
            self.var_progress.set('{}%'.format(per))
            self.progress_bar['value'] += per

            self.progress_bar.update_idletasks()

    def show_user_manual(self):
        # User manual
        self.usage_popup_window = Toplevel(self)
        self.usage_frame = FrameUserManual(self.usage_popup_window)
        self.usage_frame.pack()


class FrameUserManual(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.label_title = Label(
            self.master, text='Usage', background='#8854d0', anchor='center')
        self.label_title.pack(fill='x')

        self.image_graphicriver = ImageTk.PhotoImage(file='image/graphicriver.png')
        self.text = 'Copy path of a template, and paste it into this entry'
        self.label_text = Label(self.master, text=self.text, image = self.image_graphicriver,compound='left')
        self.label_text.image = self.image_graphicriver
        self.label_text.pack()


class MyApp(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.master.title('Image Thief')
        self.master.iconbitmap('icon/bandit.ico')
        title_app = Label(self.master, text='Image Thief',
                          background='#229954', foreground='white', anchor='center')
        title_app.pack(fill='x')
        self.setupUI()

    def setupUI(self):
        frame_group_option = Frame(self)
        frame_group_option.grid(row=0, column=0)

        self.var_frame_group_option = IntVar()
        self.var_frame_group_option.set(1)  # set UI for app

        icon_unsplash = PhotoImage(file='icon/photo-camera.png')
        radiobutton_unsplash_ui = Radiobutton(
            frame_group_option, text='Unsplash',
            image=icon_unsplash,
            variable=self.var_frame_group_option,
            value=1, command=self.set_ui, compound='left')
        radiobutton_unsplash_ui.image = icon_unsplash

        icon_graphicriver = ImageTk.PhotoImage(file='icon/graphicriver.png')
        radiobutton_graphicriver_ui = Radiobutton(frame_group_option)
        radiobutton_graphicriver_ui['text'] = 'GraphicRiver'
        radiobutton_graphicriver_ui['image'] = icon_graphicriver
        radiobutton_graphicriver_ui.image = icon_graphicriver
        radiobutton_graphicriver_ui['compound'] = 'left'
        radiobutton_graphicriver_ui['variable'] = self.var_frame_group_option
        radiobutton_graphicriver_ui['value'] = 2
        radiobutton_graphicriver_ui['command'] = self.set_ui

        radiobutton_unsplash_ui.pack(side='left')
        radiobutton_graphicriver_ui.pack(side='left')

        self.unsplash_ui = UnsplashUI(self)
        self.unsplash_ui.grid(row=1, column=0, sticky='w')

    def set_ui(self):
        list_app = self.grid_slaves(row=1, column=0)
        if self.var_frame_group_option.get() == 1:
            list_app[0].destroy()
            self.unsplash_ui = UnsplashUI(self)
            self.unsplash_ui.grid(row=1, column=0)

        elif self.var_frame_group_option.get() == 2:
            list_app[0].destroy()
            self.graphicriver_ui = GraphicRiverUI(self)
            self.graphicriver_ui.grid(row=1, column=0)


if __name__ == '__main__':
    master = Tk()
    a = MyApp(master)
    a.pack()
    master.mainloop()
