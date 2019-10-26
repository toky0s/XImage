# python 3
from tkinter import *
from tkinter import filedialog, colorchooser
from tkinter.ttk import *
from bs4 import BeautifulSoup
from urllib import request
from unsplash import GraphicRiver
from PIL import Image, ImageTk
import requests
import time
import os
import shutil

class GraphicRiverUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.list_tag_a = [] # this list will contain <a> tags
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
        self.entry_amount = Entry(self, textvariable=self.var_amount)
        self.entry_amount.grid(row=2, column=1, sticky='we')

        # row 3
        self.button_download = Button(self,text='Download', command = self.change_ui)
        self.button_download.grid(row=3, column=1, sticky= 'we')

        self.button_usage = Button(self, text='Usage', command= self.show_user_manual)
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
        self.progress_bar.config(length=100, orient='horizontal', mode='determinate')

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
        self.progress_bar.grid(row=5, column=1, columnspan =2, sticky='we')
        self.label_image.grid(row=6, column=0, columnspan=3)
        self.master.after(1000,self.get_list_tag_a)
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
            list_tag_a = soup.find_all('a', limit=self.var_amount.get()) # set limit to download
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

        # check amount here
        if self.var_amount.get() == 0 and self.var_amount.get() > len(self.list_tag_a):
            # download all
            for i in self.get_list_tag_a(self, self.var_url):
                name_image = i.split('/')[6]
                request.urlretrieve(i, full_path_save+'/'+image_names)

                image_downloaded = Image.open(file=self.var_folder_name.get()+'/'+image_names)
                width = int(self.winfo_width())
                height = int(width*image_downloaded.height/image_downloaded.width)

                self.photo = ImageTk.PhotoImage(image_downloaded.resize((width, height), Image.ANTIALIAS))
                self.label_image.config(image=self.photo)
                self.label_image.image = self.photo
                self.var_progress.set('{}%'.format())
        else:
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
        self.label_title = Label(self, text='Usage')
        self.label_title.pack()

        
class GraphicRiverEdit(GraphicRiver):

    def __init__(self, folder_path):
        self.path = folder_path
