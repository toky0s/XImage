from tkinter import *
from unsplash_ui import UnsplashUI

class MyApp(Tk):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        # Main windows
        self.title("Image Thief")
        self.iconbitmap('bandit.ico')
        frame = UnsplashUI(self)
        frame.pack()
        self.mainloop()


if __name__ == '__main__':
    a = MyApp()