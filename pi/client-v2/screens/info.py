from tkinter import *
from tkinter.ttk import *

class InfoScreen(Frame):

    keyPressEventId = False

    def __init__(self, root, app) -> None:        
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")

        self.app = app

        pump1 = Label(self, text="Pump 1", style="Bartender.TLabel")
        pump1.grid(column=0, row=0, padx=30, pady=20)

        pump2 = Label(self, text="Pump 2", style="Bartender.TLabel")
        pump2.grid(column=1, row=0, padx=30, pady=20)

        pump3 = Label(self, text="Pump 3", style="Bartender.TLabel")
        pump3.grid(column=0, row=1, padx=30, pady=20)

        pump4 = Label(self, text="Pump 4", style="Bartender.TLabel")
        pump4.grid(column=1, row=1, padx=30, pady=20)

        pump5 = Label(self, text="Pump 5", style="Bartender.TLabel")
        pump5.grid(column=0, row=2, padx=30, pady=20)

        pump6 = Label(self, text="Pump 6", style="Bartender.TLabel")
        pump6.grid(column=1, row=2, padx=30, pady=20)
    
    def enter(self, params):
        self.keyPressEventId = self.app.bind("<KeyPress>", self.handleKeyPress)
    
    def leave(self):
        if (self.keyPressEventId != False):
            self.app.unbind("<KeyPress>", self.keyPressEventId)
            self.keyPressEventId = False
    
    def handleKeyPress(self, e):
        if (e.keysym == "Return"):
            # Import screen here to avoid circular reference
            from screens.main import MainScreen

            # Master is the root object which contains the navigation method (see client.py)
            self.master.navigate(MainScreen)