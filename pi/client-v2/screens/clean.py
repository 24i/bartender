from tkinter import *
from tkinter.ttk import *
import requests
from threading import Timer

class CleanScreen(Frame):

    keyPressEventId = False
    isCleaning = False
    isLocked = False

    def __init__(self, root, app) -> None:        
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")

        self.app = app

        self.text = Label(self, text="Press button to START", style="Bartender.TLabel")
        self.text.grid(row=0, column=0)
    
    def enter(self, params):
        self.keyPressEventId = self.app.bind("<KeyPress>", self.handleKeyPress)
    
    def leave(self):
        if (self.keyPressEventId != False):
            self.app.unbind("<KeyPress>", self.keyPressEventId)
            self.keyPressEventId = False
    
    def handleKeyPress(self, e):
        if (self.isLocked):
            return
        
        if (e.keysym == "Return"):
            if (self.isCleaning == False):
                requests.post('http://127.0.0.1:8080/clean', json={
                    "method": "on"
                })
                self.isCleaning = True
                self.text.configure(text="Press button to STOP")
            else:
                requests.post('http://127.0.0.1:8080/clean', json={
                    "method": "off"
                })
                self.isCleaning = False
                self.text.configure(text="Cleaning done")
                self.isLocked = True
                timer = Timer(3, self.done)
                timer.start()
    
    def done(self):
        from screens.main import MainScreen
        self.master.navigate(MainScreen)

        # Back to initial state
        self.text.configure(text="Press button to START")
        self.isCleaning = False
        self.isLocked = False

