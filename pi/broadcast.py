from time import sleep
from socket import *

cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    cs.sendto('bartender_broadcast', ('255.255.255.255', 54545))
    sleep(5)