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
import urllib.request
import shutil
import threading
import logging

# logging.basicConfig(level=logging.INFO)


# unsplash
class UnsplashImage:

    def __init__(self, data):
        self.id = data['id']
        self.alt_description = data['alt_description']
        self.raw = data['urls']['raw']
        self.full = data['urls']['full']
        self.regular = data['urls']['regular']
        self.small = data['urls']['small']
        self.thumb = data['urls']['thumb']

    def getRawUrl(self):
        return self.raw

    def getFullUrl(self):
        return self.full

    def getRegularUrl(self):
        return self.regular

    def getSmallUrl(self):
        return self.small

    def getThumbUrl(self):
        return self.thumb

    def downloadThisImage(self, quality: str, save_at: str, **kw):
        quality_dict = {
            'raw': self.getRawUrl,
            'full': self.getFullUrl,
            'regular': self.getRegularUrl,
            'small': self.getSmallUrl,
            'thumb': self.getThumbUrl
        }
        link = quality_dict[quality]()
        urllib.request.urlretrieve(link, f'{save_at}/{self.id}.jpg')
        return f'{save_at}/{self.id}.jpg'


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


class UnsplashUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.listUnsplashImage = []
        self.setupUI()

    def setupUI(self):
        self.label_name = Label(self, text='Query:')
        self.label_name.grid(row=0, column=0, sticky='w')

        self.label_amount = Label(self, text='Per page:')
        self.label_amount.grid(row=1, column=0, sticky='w')

        self.label_page_number = Label(self, text='Page:')
        self.label_page_number.grid(row=2, column=0, sticky='w')

        self.label_save = Label(self, text='Save:')
        self.label_save.grid(row=3, column=0, sticky='w')

        self.label_quality = Label(self, text='Quality:')
        self.label_quality.grid(row=4, column=0, sticky='w')

        self.label_order_by = Label(self, text='Order by:')
        self.label_order_by.grid(row=5, column=0, sticky='w')

        self.label_random = Label(self, text='Random:')
        self.label_random.grid(row=6, column=0, sticky='w')

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
        self.entry_save = Entry(self, textvariable=self.var_folder_name)
        self.entry_save.grid(row=3, column=1, sticky='we')

        self.button_browse = Button(
            self, text='Browse', command=self.choice_folder)
        self.button_browse.grid(row=3, column=2, sticky='we')

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
        self.checkbutton_random = Checkbutton(self)
        self.checkbutton_random['variable'] = self.var_random
        self.checkbutton_random['command'] = self.disable_order_by_for_random
        self.checkbutton_random.grid(row=6, column=1, sticky='w')
        createToolTip(self.checkbutton_random, 'Max amount is 30')

        self.image_icon_download = PhotoImage(file='icon/down-arrow.png')
        self.button_download = Button(self)
        self.button_download['text'] = 'Download now!'
        self.button_download['image'] = self.image_icon_download
        self.button_download['compound'] = 'left'
        self.button_download['command'] = self.startDownload
        self.button_download.image = self.image_icon_download
        self.button_download.grid(row=7, column=1)

    def startDownload(self):
        # check folder
        if self.var_folder_name.get() == '':
            messagebox.showwarning('Thông báo','Bạn chưa chọn nơi lưu trữ!')
            return
        else:
            self.lock = threading.Lock()
            self.th_sendRequest = threading.Thread(target=self.getListUnsplashImages)
            self.th_sendRequest.start()
            
            logging.info('Initialize the Download UI')
            self.toplevel_info = Toplevel(self)
            self.toplevel_info.title('Downloading...')

            self.var_progress = StringVar()
            self.label_progress = Label(self.toplevel_info)
            self.label_progress['textvariable'] = self.var_progress
            self.label_progress.pack(fill='x')

            self.progress_bar = Progressbar(self.toplevel_info)
            self.progress_bar['length']=100
            self.progress_bar['orient']='horizontal'
            self.progress_bar['mode']='determinate'
            self.progress_bar['value'] = 0
            self.progress_bar.pack(fill='x')

            self.label_image = Label(self.toplevel_info)
            self.label_image.pack(fill='x')

            self.th_download = threading.Thread(target=self.download)
            self.th_download.start()

            self.toplevel_info.protocol('WM_DELETE_WINDOW', self.closeToplevelWidget)

    def download(self):
        self.lock.acquire()
        per = 0
        self.show = 1
        for image in self.listUnsplashImage:
            path = image.downloadThisImage(self.var_quality_rb.get(),self.var_folder_name.get())

            per = per + 100/len(self.listUnsplashImage)
            self.var_progress.set('{}%'.format(int(per)))
            self.progress_bar['value'] = per

            self.image_downloaded = Image.open(path)
            self.image_complete = ImageTk.PhotoImage(self.image_downloaded)


            self.label_image['image'] = self.image_complete
            self.label_image.image = self.image_complete

            if self.show == 0:
                break
        
        # release data
        logging.info('show warning')
        messagebox.showinfo('Thông báo','Đã tải xong !')
        self.toplevel_info.destroy()
        self.listUnsplashImage = []

        self.lock.release()

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

    def getListUnsplashImages(self):
        '''Thực hiện gửi chọn và request, sau đó đưa data lấy về thành một list chứa UnsplashImage'''
        self.lock.acquire()
        if self.var_random.get() == 1:
            # call random request
            request = 'https://unsplash.com/napi/photos/random'
            params = {'count': self.var_amount.get()}
            r = requests.get(request, params=params)
            data = json.loads(r.text)
        elif self.var_name.get() == '':
            request = 'https://unsplash.com/napi/photos'
            params = params = {
                'page': self.var_page_number.get(),
                'per_page': self.var_amount.get()
            }
            r = requests.get(request, params=params)
            data = json.loads(r.text)
        else:
            # call searchPhoto request
            request = 'https://unsplash.com/napi/search/photos'
            params = {
                'query': self.var_name.get(),
                'page': self.var_page_number.get(),
                'per_page': self.var_amount.get()
            }
            r = requests.get(request, params=params)
            data = json.loads(r.text)
            data = data['results']

        for i in data:
            img = UnsplashImage(i)
            self.listUnsplashImage.append(img)

        self.lock.release()

    def closeToplevelWidget(self):
        self.show = 0

class GraphicRiverUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.list_tag_a = []  # this list will contain <a> tags
        self.setupUI()

    def setupUI(self):

        self.label_url = Label(self, text='Url:')
        self.label_url.grid(row=0, column=0, sticky='w')

        self.var_url = StringVar()
        self.entry_url = Entry(self, textvariable=self.var_url)
        self.entry_url.grid(row=0, column=1, sticky='we')

        self.label_save = Label(self, text='Save:')
        self.label_save.grid(row=1, column=0, sticky='w')

        self.var_folder_name = StringVar()
        self.entry_save = Entry(self)
        self.entry_save['textvariable'] = self.var_folder_name
        self.entry_save.grid(row=1, column=1, sticky='we')

        self.button_browse = Button(self)
        self.button_browse['text']='Browse'
        self.button_browse['command'] = self.choice_folder
        self.button_browse.grid(row=1, column=2, sticky='we')

        self.label_amount = Label(self, text='Amount:')
        self.label_amount.grid(row=2, column=0, sticky='w')

        self.var_amount = IntVar()
        self.entry_amount = Entry(self, textvariable=self.var_amount)
        self.entry_amount.grid(row=2, column=1, sticky='we')

        # row 3
        self.button_download = Button(self)
        self.button_download['text'] = 'Download'
        self.button_download['command'] = self.startDownload
        self.button_download.grid(row=3, column=1, sticky='we')

        self.button_usage = Button(self)
        self.button_usage['text']='Usage'
        self.button_usage['command'] = self.show_user_manual
        self.button_usage.grid(row=3, column=2, sticky='we')

    def choice_folder(self):
        logging.info('Choose a folder to save')
        dialog_choice_folder = filedialog.askdirectory()
        self.var_folder_name.set(dialog_choice_folder)

    def get_name_presentation(self):
        self.name_presentation = 'Name Presentation'
        return self.name_presentation

    def __has_a_http_jpg(self, tag):
        # check image's link is https://www.somthing.jpg
        if (tag['class'] == 'is-hidden') and (tag.name == 'a') and (('.jpg' == tag['href'][-4:len(tag['href'])])or('.JPG' == tag['href'][-4:len(tag['href'])])):
            return True

    def get_list_tag_a(self):
        '''Trả về một list chứa các link để tải ảnh'''
        logging.info('Get list tag <a>')
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

    def startDownload(self):
        logging.info('Prepair data to download')
        # prepair data
        self.dir_name = self.var_url.get().split('/')[4]
        if os.path.exists(self.var_folder_name.get()+'/'+self.dir_name):
            shutil.rmtree(self.var_folder_name.get()+'/'+self.dir_name)

        self.full_path_save = self.var_folder_name.get()+'/'+self.dir_name
        os.mkdir(self.full_path_save)
        self.get_list_tag_a()

        logging.info('Initialize the Download UI')
        self.toplevel_info = Toplevel(self)
        self.toplevel_info.title('Downloading...')

        self.var_progress = StringVar()
        self.label_progress = Label(self.toplevel_info)
        self.label_progress['textvariable'] = self.var_progress
        self.label_progress.pack(fill='x')

        self.progress_bar = Progressbar(self.toplevel_info)
        self.progress_bar['length']=100
        self.progress_bar['orient']='horizontal'
        self.progress_bar['mode']='determinate'
        self.progress_bar['value'] = 0
        self.progress_bar.pack(fill='x')

        self.label_image = Label(self.toplevel_info)
        self.label_image.pack(fill='x')

        self.th_download = threading.Thread(target=self.download)
        self.th_download.start()

    def download(self):
        logging.info('downloading')
        per = 0
        for i in self.list_tag_a:
            name_image = i.split('/')[-1]
            request.urlretrieve(i, self.full_path_save+'/'+name_image)
            
            per = per + 100/self.var_amount.get()
            self.var_progress.set('{}%'.format(int(per)))
            self.progress_bar['value'] = per

            self.image_downloaded = Image.open(self.full_path_save+'/'+name_image)
            self.image_complete = ImageTk.PhotoImage(self.image_downloaded)


            self.label_image['image'] = self.image_complete
            self.label_image.image = self.image_complete

        # release data
        logging.info('show warning')
        messagebox.showinfo('Thông báo','Đã tải xong !')
        self.toplevel_info.destroy()
        self.list_tag_a = []

    def show_user_manual(self):
        # User manual
        logging.info('Show the user manual')



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
