from tkinter import *
from tkinter.ttk import *
from unsplash_ui import UnsplashUI
from graphicriver_ui import GraphicRiverUI
from PIL import Image, ImageTk

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
        frame_group_option.grid(row=0,column=0)

        self.var_frame_group_option = IntVar()
        self.var_frame_group_option.set(1) # set UI for app

        icon_unsplash = PhotoImage(file='icon/photo-camera.png')
        radiobutton_unsplash_ui = Radiobutton(
            frame_group_option, text='Unsplash',
            image=icon_unsplash,
            variable=self.var_frame_group_option,
            value=1, command=self.set_ui, compound='left')
        radiobutton_unsplash_ui.image = icon_unsplash
        
        # icon_graphicriver = PhotoImage(file='icon/graphicriver.png')
        radiobutton_graphicriver_ui = Radiobutton(frame_group_option,
            text='GraphicRiver',
            # image = icon_graphicriver,
            compound='left',
            variable=self.var_frame_group_option,
            value=2,
            command=self.set_ui)
        # radiobutton_graphicriver_ui.image = icon_graphicriver

        radiobutton_unsplash_ui.pack(side='left')
        radiobutton_graphicriver_ui.pack(side='left')

        self.unsplash_ui = UnsplashUI(self)
        self.unsplash_ui.grid(row=1, column=0, sticky='w')

    def set_ui(self):
        list_app = self.grid_slaves(row=1,column=0)
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
