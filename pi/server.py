from gpiozero import PWMLED
from time import sleep

red = PWMLED(16)
green = PWMLED(20)
blue = PWMLED(21)

from socket import *
cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    cs.sendto('This is a test', ('255.255.255.255', 54545))
    sleep(2)