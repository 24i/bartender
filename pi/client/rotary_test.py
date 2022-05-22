# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

from libs.Encoder import rotary_encoder
from libs import switch
from libs import gpio
import time
import os
import sys
import math
from math import sin, cos, radians
import logging
import spidev as SPI
sys.path.append("..")
from libs.LCD  import LCD_2inch
from PIL import Image,ImageDraw

A_PIN  = 21
B_PIN  = 9
SW_PIN = 8

gpio = gpio.GPIO()
encoder = rotary_encoder.RotaryEncoder.Worker(gpio, A_PIN, B_PIN)
encoder.start() 
switch = switch.Switch(gpio, SW_PIN)
last_state = None
counter = 0


# display with hardware SPI:
''' Warning!!!Don't  creation of multiple displayer objects!!! '''
#disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
disp = LCD_2inch.LCD_2inch()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()

# Create blank image for drawing.
image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
draw = ImageDraw.Draw(image1)
logging.info("draw rectangle")


draw.rectangle([(35,95),(85 + counter,145)],fill = "RED",outline="RED")

# image1=image1.rotate(180)
disp.ShowImage(image1)
# time.sleep(3)
# logging.info("show image")

# image = Image.open('../pic/LCD_2inch.jpg')	
# image = image.rotate(180)
# disp.ShowImage(image)


while True:
    delta = encoder.get_steps()
    if delta!=0:
        counter = counter + delta
        print ("rotate %d, counter %d" % (delta, counter))

        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
        draw = ImageDraw.Draw(image1)

        draw = ImageDraw.Draw(image1)
        logging.info("draw rectangle")

        draw.rectangle([(35,95),(85 + counter,145)],fill = "RED",outline="RED")

        # image1=image1.rotate(180)
        disp.ShowImage(image1)
    else:
        time.sleep(0.05)

    sw_state = switch.get_state()
    if sw_state != last_state:
        print ("switch %d" % sw_state)
        last_state = sw_state
