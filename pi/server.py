from gpiozero import PWMLED
from time import sleep
from socket import *
import http.server

red = PWMLED(16)
green = PWMLED(20)
blue = PWMLED(21)

cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

with socketserver.TCPServer(("", 8000), Handler) as httpd:
    print("serving at port", 8000)
    httpd.serve_forever()

while True:

    print("UDP signal")
    cs.sendto('bartender_broadcast', ('255.255.255.255', 54545))

    sleep(2)