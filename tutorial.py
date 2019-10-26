from tkinter import *

master = Tk()

frame = Frame(width=768, height=576, bg="", colormap="new")
frame.pack()

video.attach_window(frame.window_id())

mainloop()
