from tkinter import *

root = Tk();
root.geometry("320x240")

frame = Frame(root)
frame.pack()

button = Button(frame, text = "BUTTON")
button.pack()

root.mainloop()