from asyncio import events
from threading import Event
from gpiozero import RotaryEncoder,Button

done = Event()
rotor = RotaryEncoder(21, 9)

def test():
    print("ROTATE\n")

rotor.when_rotated = test

def say_hello():
    print("Hello!")

button = Button(8)

button.when_pressed = say_hello

done.wait()