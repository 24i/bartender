from threading import Timer
from tkinter import *
from tkinter.ttk import *
import requests
from threading import Timer

class PourScreen(Frame):

    activeStep = 0
    keyPressEventId = False

    def __init__(self, root, app) -> None:        
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")
        self.app = app

        self.progress = Label(self, text="|__________________|", style="Bartender.TLabel")
        self.progress.grid(column=0, row=0)

    def enter(self, params):
        response = requests.post('http://127.0.0.1:8080/pour-recipe', json={
            "recipeId": params['recipeId'],
            "amount": params['amount']
        }).json()

        timer = Timer(response['time'], self.done)
        timer.start()
    
    def leave(self):
        pass

    def done(self):
        from screens.main import MainScreen
        self.master.navigate(MainScreen)