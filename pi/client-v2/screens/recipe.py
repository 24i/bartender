from tkinter import *
from tkinter.ttk import *
from screens.amount import AmountSelectorScreen
import requests

class RecipeSelectorScreen(Frame):

    selectedRecipe = 0
    keyPressEventId = False

    def __init__(self, root, app) -> None:        
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")

        self.app = app

        self.recipes = requests.get('http://127.0.0.1:8080/recipes').json()

        self.left = Label(self, text="", style="Bartender.TLabel")
        self.left.grid(column=0, row=0)

        self.label = Label(self, text=self.recipes[self.selectedRecipe]['name'], style="Bartender.TLabel",)
        self.label.grid(column=1, row=0, padx=10)

        self.right = Label(self, text=">>", style="Bartender.TLabel")
        self.right.grid(column=2, row=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def enter(self, params):
        self.keyPressEventId = self.app.bind("<KeyPress>", self.handleKeyPress)
    
    def leave(self):
        if (self.keyPressEventId != False):
            self.app.unbind("<KeyPress>", self.keyPressEventId)
            self.keyPressEventId = False
    
    def handleKeyPress(self, e):
        if (e.keysym == "Left" and self.selectedRecipe > 0):
            self.selectedRecipe -= 1
        if (e.keysym == "Right" and self.selectedRecipe < len(self.recipes) - 1):
            self.selectedRecipe +=1

        # Hide left arrow if we can no longer go left
        if (self.selectedRecipe == 0):
            self.left.configure(text="")
        else:
            self.left.configure(text="<<")

        # Hide right arrow if we can no longer go right
        if (self.selectedRecipe == len(self.recipes) - 1):
            self.right.configure(text="")
        else:
            self.right.configure(text=">>")

        if (e.keysym == "Return"):
            self.master.navigate(AmountSelectorScreen)

        self.label.configure(text=self.recipes[self.selectedRecipe]['name'])