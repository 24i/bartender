from tkinter import *
from tkinter.ttk import *
from screens.pour import PourScreen

class AmountSelectorScreen(Frame):

    activeStep = 0
    keyPressEventId = False

    def __init__(self, root, app) -> None:        
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")
        self.app = app

        self.steps = [100, 150, 200, 250, 300, 350, 400, 450, 500]
        self.amountBar = Label(self, text="|██________________|", style="Bartender.TLabel")
        self.amountBar.grid(column=0, row=0)
        
        self.amount = Label(self, text=str(self.steps[self.activeStep]) + "ml", style="Bartender.TLabel")
        self.amount.grid(column=0, row=1, pady=25)

    def enter(self, params):
        self.recipeId = params['recipeId']
        self.keyPressEventId = self.app.bind("<KeyPress>", self.handleKeyPress)
    
    def leave(self):
        if (self.keyPressEventId != False):
            self.app.unbind("<KeyPress>", self.keyPressEventId)
            self.keyPressEventId = False
    
    def handleKeyPress(self, e):
        max = len(self.steps)
        print(e.keysym)
        if (e.keysym == "Left" and self.activeStep > 0):
            self.activeStep -= 1
        if (e.keysym == "Right" and self.activeStep < max - 1):
            self.activeStep +=1
        
        n = self.activeStep + 1
    
        self.amountBar.configure(text="|" + ("██" * n) + ("__" * (max-n)) + "|" )
        self.amount.configure(text=str(self.steps[self.activeStep]) + "ml")

        if (e.keysym == "Return"):
            self.master.navigate(PourScreen, {
                "recipeId": self.recipeId,
                "amount": self.steps[self.activeStep]
            })