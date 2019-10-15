import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", textvariable=None,color='grey'):
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


if __name__ == "__main__":

    def update_text_in_entry():
        value_1.set('update 1')
        value_2.set('update 2')

    root = tk.Tk()

    value_1 = tk.StringVar()
    value_2 = tk.StringVar()
    username = EntryWithPlaceholder(root, "username",textvariable=value_1).pack()
    password = EntryWithPlaceholder(root, "password", textvariable=value_2,color='blue').pack()
    
    b = tk.Button(root,text='Update entry', command=update_text_in_entry)
    b.pack()
    
    root.mainloop()
