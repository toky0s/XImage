from tkinter import messagebox, StringVar, IntVar
from tkinter.ttk import Label,Progressbar, Entry, Frame
from PIL import Image, ImageTk
from urllib import request

import json
import time
import requests

LIST ='https://unsplash.com/napi/photos'
RANDOM = 'https://unsplash.com/napi/photos/random'
SEARCH = 'https://unsplash.com/napi/search/photos'

class FrameDownload(Frame):

    def __init__(self, master=None, option=()):
        super().__init__(master=master)
        self.master = master
        self.master.title('Download information')
        self.option = option
        self.setupUI()

    def setupUI(self):

        label_title = Label(self, text='Download information')
        label_title.config(anchor='center', foreground='white', background='#2c3e50')
        label_title.grid(row=0, column=0, columnspan=6, sticky='we')

        self.progress = Progressbar(self, orient='horizontal', length=100, mode='determinate')
        if self.option[2] == SEARCH:
            self.progress.grid(row=1, column=0, columnspan=5, sticky='we')
        else:
            self.progress.grid(row=1, column=0, columnspan=3, sticky='we')

        self.var_progress = StringVar()
        self.var_progress.set('0%')
        self.label_show_progress = Label(self, textvariable=self.var_progress, anchor='center')
        self.label_show_progress.var = self.var_progress
        if self.option[2] == SEARCH:
            self.label_show_progress.grid(row=1, column=5, sticky='w')
        else:
            self.label_show_progress.grid(row=1, column=3, sticky='w')

        self.label_query = Label(self, text='Query')
        self.label_query.grid(row=2, column=0, sticky='w')

        self.var_entry_query = StringVar()
        self.entry_query = Entry(
                self, textvariable=self.var_entry_query, state='readonly')
        self.entry_query.grid(row=2, column=1, sticky='w')

        self.var_total = StringVar()
        self.var_total.set('Total')
        self.label_total = Label(self, textvariable=self.var_total)
        self.label_total.grid(row=2, column=2, sticky='w')

        self.var_entry_total = IntVar()
        self.entry_total = Entry(self) 
        self.entry_total.config(textvariable=self.var_entry_total, state='readonly')
        self.entry_total.grid(row=2, column=3, sticky='w')

        if self.option[2] == SEARCH:
            self.label_total_page = Label(self, text='Total pages:')
            self.label_total_page.grid(row=2, column=4, sticky='w')

            self.var_entry_total_pages = IntVar()
            self.entry_total_page = Entry(
                self, textvariable=self.var_entry_total_pages, state='readonly')
            self.entry_total_page.grid(row=2, column=5, sticky='w')

        self.label_image_downloaded = Label(self, anchor='center')
        if self.option[2] == SEARCH:
            self.label_image_downloaded.grid(row=3, column=0, columnspan=6, sticky='wesn')
        else:
            self.label_image_downloaded.grid(
                row=3, column=0, columnspan=4, sticky='wesn')

    def change_ui(self):
        if self.option[2] == SEARCH:
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
        elif self.option[2] == RANDOM:
            r = requests.get(self.option[2], params=self.option[3])
            if r.status_code == 200:

                # get result
                j = json.loads(r.text)
                results = j

                # change data
                self.var_entry_query.set('random')
                if self.option[3]['count'] > 30:
                    self.var_entry_total.set(30)
                self.var_total.set('Amount')
                self.var_entry_total.set(self.option[3]['count'])

                # update widget
                self.entry_query.update_idletasks()
                self.label_total.update_idletasks()
                self.entry_total.update_idletasks()

        elif self.option[2] == LIST:
            r = requests.get(self.option[2], params=self.option[3])
            if r.status_code == 200:

                # get result
                j = json.loads(r.text)
                results = j

                # change data
                self.var_entry_query.set('get a list of images')
                if self.option[3]['per_page'] > 30:
                    self.var_entry_total.set(30)
                self.var_total.set('Amount')
                self.var_entry_total.set(self.option[3]['per_page'])

                # update widget
                self.entry_query.update_idletasks()
                self.label_total.update_idletasks()
                self.entry_total.update_idletasks()

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

            self.label_image_downloaded.update_idletasks()
            self.label_show_progress.update_idletasks()
            self.progress.update_idletasks()
            
        self.message_done = messagebox.showinfo('Info', 'Done')
        self.master.destroy()
