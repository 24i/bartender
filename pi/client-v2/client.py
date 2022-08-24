from textwrap import fill
from tkinter import *
from tkinter import font
from tkinter.ttk import *
from turtle import color, st, width
from screens.main import MainScreen
from screens.info import InfoScreen
from screens.recipe import RecipeSelectorScreen
from screens.amount import AmountSelectorScreen

class App(Frame):

    def __init__(self, root) -> None:
        Frame.__init__(self, root)

        self.configure(style="Bartender.TFrame")
        self.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.screens = {}
        for Screen in (MainScreen, InfoScreen, RecipeSelectorScreen, AmountSelectorScreen):
            screen = Screen(self, root)
            self.screens[Screen] = screen
        
        self.navigate(MainScreen)

    def navigate(self, screen):
        for s in self.screens:
            self.screens[s].grid_forget()
            self.screens[s].leave()
        
        screen = self.screens[screen]
        screen.grid(row=0, column=0)
        screen.enter()

window = Tk()
window.geometry("320x240")
# window.attributes("-fullscreen", True)

style = Style()
style.theme_use('default')
style.configure("Bartender.TFrame", background="black")
style.configure("Bartender.TLabel", font="Courier 16")
style.configure("TLabel", background="black", foreground="white")

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

app = App(window)
window.mainloop()