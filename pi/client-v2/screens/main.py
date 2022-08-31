from tkinter import *
from tkinter.ttk import *
from screens.info import InfoScreen
from screens.recipe import RecipeSelectorScreen
import os

class MainScreen(Frame):

    activeButton = 0
    keyPressEventId = False

    def __init__(self, root, app) -> None:
        Frame.__init__(self, root, width=320, height=240, style="Bartender.TFrame")

        self.app = app

        path = os.path.dirname(__file__)

        self.icons = {
            "cocktail": {
                "normal": PhotoImage(file = os.path.join(path, "../icons/cocktail.png")),
                "focus": PhotoImage(file = os.path.join(path, "../icons/cocktail_focus.png"))
            },
            "clean": {
                "normal": PhotoImage(file = os.path.join(path, "../icons/clean.png")),
                "focus": PhotoImage(file = os.path.join(path, "../icons/clean_focus.png"))
            },
            "info": {
                "normal": PhotoImage(file=os.path.join(path, "../icons/info.png")),
                "focus": PhotoImage(file=os.path.join(path, "../icons/info_focus.png"))
            }
        }

        self.callbacks = {
            "info": lambda: root.navigate(InfoScreen),
            "cocktail": lambda: root.navigate(RecipeSelectorScreen)
        }

        cocktailButton = Label(self, image=self.icons["cocktail"]["focus"], name="cocktail")
        cocktailButton.grid(column=1, row=0, padx=20)
        cleanButton = Label(self, image=self.icons["clean"]["normal"], name="clean")
        cleanButton.grid(column=2, row=0, padx=20)
        infoButton = Label(self, image=self.icons["info"]["normal"], name="info")
        infoButton.grid(column=3, row=0, padx=20)

        self.buttons = [ cocktailButton, cleanButton, infoButton ]

    def enter(self, params):
        self.keyPressEventId = self.app.bind("<KeyPress>", self.handleKeyPress)
    
    def leave(self):
        if (self.keyPressEventId != False):
            self.app.unbind("<KeyPress>", self.keyPressEventId)
            self.keyPressEventId = False

    def handleKeyPress(self, e):
        if (e.keysym == "Right" and self.activeButton < len(self.buttons) - 1):
            self.activeButton += 1
            self.setActiveButtonFocus()

        if (e.keysym == "Left" and self.activeButton > 0):
            self.activeButton -= 1
            self.setActiveButtonFocus()
            
        if (e.keysym == "Return"):
            button = self.buttons[self.activeButton]
            name = str(button).split(".")[-1]
            self.callbacks[name]()

    def setActiveButtonFocus(self):
        for index,button in enumerate(self.buttons):
            name = str(button).split(".")[-1]
            icon = "focus" if index == self.activeButton else "normal"
            button.configure(image = self.icons[name][icon])
        