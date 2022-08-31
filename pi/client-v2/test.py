from asyncio import events
from threading import Event
from gpiozero import RotaryEncoder

done = Event()
rotor = RotaryEncoder(21, 9)

def test():
    print("ROTATE\n")

rotor.when_rotated = test
done.wait()