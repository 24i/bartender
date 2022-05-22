# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

from libs.Encoder import rotary_encoder
from libs import switch
from libs import gpio
from display import screen_builder
import time
import os
import sys
import math
from math import sin, cos, radians
import logging
import spidev as SPI
sys.path.append("..")
from libs.LCD  import LCD_2inch
from PIL import Image,ImageDraw,ImageFont

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

screenBuilder = screen_builder.ScreenBuilder()
screen = screenBuilder.build_home_screen()

# # Create blank image for drawing.
# image1 = Image.new("RGB", (disp.height, disp.width ), "BLACK")
# draw = ImageDraw.Draw(image1)

# # image = Image.open('../pic/LCD_2inch.jpg')	
# # image = image.rotate(180)
# # disp.ShowImage(image)
# logging.info("draw text")
# Font1 = ImageFont.truetype("./fonts/Inter-Regular.ttf", 25)

# #draw.rectangle([(0,65),(140,100)],fill = "WHITE")
# draw.text((20, 68), 'ENJOY OUR DRINKS', fill = "WHITE",font=Font1)

# image1=image1.rotate(180)
disp.ShowImage(screen)
# time.sleep(3)
# logging.info("show image")


time.sleep(3)
disp.module_exit()