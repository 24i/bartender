from gpiozero import PWMLED
from time import sleep

red = PWMLED(16)
green = PWMLED(20)
blue = PWMLED(21)

while True:
    red.on()
    green.on()
    blue.on()
    sleep(1)
    red.off()
    green.on()
    sleep.on()
    sleep(1)