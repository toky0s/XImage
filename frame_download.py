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
        # build UI base on URLS
        if self.option[2] == SEARCH:
            # title window
            label_title = Label(self, text='Search Photos')
            label_title.config(anchor='center', foreground='white', background='#8e44ad')
            label_title.grid(row=0, column=0, columnspan=6, sticky='we')

            # progress
            self.progress = Progressbar(self) 
            self.progress.config(orient='horizontal', length=100, mode='determinate')
            self.progress.grid(row=2, column=0, columnspan=5, sticky='we')

            self.var_progress = StringVar()
            self.var_progress.set('0%')
            self.label_show_progress = Label(self) 
            self.label_show_progress.config(textvariable=self.var_progress, anchor='center')
            self.label_show_progress.var = self.var_progress
            self.label_show_progress.grid(row=2, column=5, sticky='w')

            # query
            self.label_query = Label(self, text='Query')
            self.label_query.grid(row=1, column=0, sticky='e')

            self.var_entry_query = StringVar()
            self.entry_query = Entry(self)
            self.entry_query.config(textvariable=self.var_entry_query, state='readonly')
            self.entry_query.grid(row=1, column=1, sticky='w')

            # total
            self.var_total = StringVar()
            self.var_total.set('Total')
            self.label_total = Label(self, textvariable=self.var_total)
            self.label_total.grid(row=1, column=2, sticky='e')

            self.var_entry_total = IntVar()
            self.entry_total = Entry(self)
            self.entry_total.config(textvariable=self.var_entry_total, state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')

            # total pages
            self.label_total_page = Label(self, text='Total pages:')
            self.label_total_page.grid(row=1, column=4, sticky='e')

            self.var_entry_total_pages = IntVar()
            self.entry_total_page = Entry(self)
            self.entry_total_page.config(textvariable=self.var_entry_total_pages, state='readonly')
            self.entry_total_page.grid(row=1, column=5, sticky='w')

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
            self.label_image_downloaded.grid(row=3, column=0, columnspan=6, sticky='wesn')
            
            # self.change_ui()

        elif self.option[2] == LIST:
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
            self.entry_query.insert(0,'LIST')
            self.entry_query.config(state='readonly')
            self.entry_query.grid(row=1, column=1, sticky='w')

            # amount
            self.label_total = Label(self, text='Amount:')
            self.label_total.grid(row=1, column=2, sticky='e')

            self.entry_total = Entry(self)
            self.entry_total.insert(0,self.option[3]['per_page'])
            self.entry_total.config(state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
            self.label_image_downloaded.grid(
                row=3, column=0, columnspan=4, sticky='wesn')

            # self.change_ui()

        elif self.option[2] == RANDOM:
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
            self.entry_query.insert(0,'RANDOM')
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
            self.entry_total.config(textvariable=self.var_entry_total, state='readonly')
            self.entry_total.grid(row=1, column=3, sticky='w')
            

            # show image is downloaded
            self.label_image_downloaded = Label(self, anchor='center')
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

        elif self.option[2] == LIST:
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


class DownloadFrame(Frame):
    
    def __init__(self, master, option,**kw):
        super().__init__(master=master)
        self.option = option
        self.setupUI()

    def setupUI(self):
        self.label_download = Label(self)
        self.label_download['text'] = 'Download'
        self.label_download.grid()

        self.progressbar = Progressbar(self)
        self.

        self.label_image_downloaded = Label(self)
        
        self.update()
    def update(self):
        '''cập nhật lại giao diện'''
        self.after(100, self.update)

