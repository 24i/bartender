from textwrap import fill
from tkinter import *
from tkinter import font
from tkinter.ttk import *
from turtle import color, st, width
from screens.main import MainScreen
from screens.info import InfoScreen
from screens.recipe import RecipeSelectorScreen
from screens.amount import AmountSelectorScreen
from screens.pour import PourScreen
from gpiozero import RotaryEncoder,Button,Device
import requests
import time
import sys

# Mock GPIO in local mode
from gpiozero.pins.mock import MockFactory
args = sys.argv[1:]

try:
	if (args[0] == 'local'):
		Device.pin_factory = MockFactory()
except:
	print("Running in PI mode")

class App(Frame):

    def __init__(self, root) -> None:
        Frame.__init__(self, root)

        self.configure(style="Bartender.TFrame")
        self.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.screens = {}
        for Screen in (MainScreen, InfoScreen, RecipeSelectorScreen, AmountSelectorScreen, PourScreen):
            screen = Screen(self, root)
            self.screens[Screen] = screen
        
        self.navigate(MainScreen)

    def navigate(self, screen, params={}):
        for s in self.screens:
            self.screens[s].grid_forget()
            self.screens[s].leave()
        
        screen = self.screens[screen]
        screen.grid(row=0, column=0)
        screen.enter(params)

window = Tk()
window.geometry("320x240")
window.attributes("-fullscreen", True)

style = Style()
style.theme_use('default')
style.configure("Bartender.TFrame", background="black")
style.configure("Bartender.TLabel", font="Courier 16")
style.configure("TLabel", background="black", foreground="white")

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

rotor = RotaryEncoder(5, 3)
button = Button(19)

def sendReturn():
    window.event_generate("<KeyPress>", keysym="Return")

def sendRight():
    window.event_generate("<KeyPress>", keysym="Right")

def sendLeft():
    window.event_generate("<KeyPress>", keysym="Left")

rotor.when_rotated_clockwise = sendRight
rotor.when_rotated_counter_clockwise = sendLeft
button.when_pressed = sendReturn

foundServer = False
while foundServer != True:
    try:
        requests.get('http://127.0.0.1:8080/pumps') 
        foundServer = True
    except:
        foundServer = False
        time.sleep(1)

app = App(window)
window.mainloop()