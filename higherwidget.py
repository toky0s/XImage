from tkinter import *


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", textvariable=None, color='grey'):
        super().__init__(master, textvariable=textvariable)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class FrameInformationForm(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.variable_1 = StringVar()
        self.variable_2 = StringVar()
        self.setupUI()

    def setupUI(self):
        label_name = Label(self, text='Name:')
        label_name.grid(row=0, column=0, sticky=W)

        label_age = Label(self, text='Age:')
        label_age.grid(row=1, column=0, sticky=W)

        entry_name = Entry(self,textvariable=self.variable_1)
        entry_name.grid(row=0, column=1, sticky=W)
        entry_age = Entry(self,textvariable=self.variable_2)
        entry_age.grid(row=1, column=1, sticky=W)

        button_show_info = Button(self,text='Show info', command=self.showinfo)
        button_show_info.grid(row=2,column=0, sticky=W)

    def showinfo(self):
        print('Your name:',self.variable_1.get(),'\nYour age:',self.variable_1.get())


if __name__ == "__main__":
    root = Tk()
    form = FrameInformationForm(root)
    form.pack()
    root.mainloop()
