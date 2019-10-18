from tkinter import *
from tkinter.filedialog import askdirectory

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


class UnsplashUI(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.setupUI()

    def setupUI(self):
        label_name = Label(self, text='Query:')
        label_name.grid(row=0, column=0, sticky=W)

        label_amount = Label(self, text='Amount:')
        label_amount.grid(row=1, column=0, sticky=W)

        label_save = Label(self, text='Save:')
        label_save.grid(row=2, column=0, sticky=W)

        label_quality = Label(self, text='Quality:')
        label_quality.grid(row=3, column=0, sticky=W)

        label_order_by = Label(self, text='Order by:')
        label_order_by.grid(row=4, column=0, sticky=W)

        label_random = Label(self, text='Random:')
        label_random.grid(row=5, column=0, sticky=W)

        entry_name = Entry(self)
        entry_name.grid(row=0, column=1, sticky='we')

        entry_amount = Entry(self)
        entry_amount.grid(row=1, column=1, sticky='we')

        self.var_file_name = StringVar()
        entry_save = Entry(self, textvariable=self.var_file_name)
        entry_save.grid(row=2, column=1, sticky='we')

        QUALITIES = {
            'Raw': 'raw',
            'Regular': 'regular',
            'Small': 'small',
            'Thumnail': 'thumnail',
        }

        var_quality_rb = StringVar()
        group_quality_radiobutton = FrameGroupRadiobutton(
            self, side=LEFT, variable=var_quality_rb, dict_option=QUALITIES, initialize='raw')
        group_quality_radiobutton.grid(row=3, column=1, sticky=W)

        ORDER_BY = {
            'Latest': 'latest',
            'Oldest': 'oldest',
            'Popular': 'popular',
        }
        var_order_by_rb = StringVar()
        group_order_by_radiobutton = FrameGroupRadiobutton(
            self, side=LEFT, variable=var_order_by_rb, dict_option=ORDER_BY, initialize='latest')
        group_order_by_radiobutton.grid(row=4, column=1, sticky=W)

        var_random = IntVar()
        checkbutton_random = Checkbutton(self,variable = var_random)
        checkbutton_random.grid(row=5, column=1, sticky=W)

        button_browse = Button(self,text='Browse',command=self.choice_folder)
        button_browse.grid(row=2, column=2, sticky=W)
    
        self.grid_rowconfigure(0, weight=1)

    def choice_folder(self):
        dialog_choice_folder = askdirectory()
        self.var_file_name.set(dialog_choice_folder)


if __name__ == '__main__':
    root = Tk()
    ui = UnsplashUI(root)
    ui.pack()
    root.mainloop()
