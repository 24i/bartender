#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import math
from math import sin, cos, radians
import logging
import spidev as SPI
sys.path.append("..")
from libs.LCD import LCD_2inch
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0 
logging.basicConfig(level=logging.DEBUG)

def rotatePolygon(polygon, degrees, height, width):
    """ 
    Description:
    
        Rotate polygon the given angle about its center. 
        
    Input:
        polygon (list of tuples)  : list of tuples with (x,y) cordinates 
                                    e.g [(1,2), (2,3), (4,5)]
        
        degrees int               : Rotation Degrees
    
    Output:
    
        polygon (list of tuples)  : Polygon rotated on angle(degrees)
                                e.g [(1,2), (2,3), (4,5)]
    
    """
    # Convert angle to radians
    theta = radians(degrees)
    
    # Getting sin and cos with respect to theta
    cosang, sinang = cos(theta), sin(theta) 

    # find center point of Polygon to use as pivot
    y, x = [i for i in zip(*polygon)]
    
    # find center point of Polygon to use as pivot
    
    cx1 = width[0] / 2
    cy1 = height[0] / 2
    cx2 = width[1] / 2
    cy2 = height[1] / 2
    
    # Rotating every point
    new_points = []
    for x, y in zip(x, y):
        tx, ty = x-cx1, y-cy1
        new_x = (tx*cosang - ty*sinang) + cx2
        new_y = (tx*sinang + ty*cosang) + cy2
        new_points.append((new_y, new_x))
    return new_points

def hexagon_generator(edge_length, offset):
  """Generator for coordinates in a hexagon."""
  x, y = offset
  for angle in range(0, 360, 60):
    x += math.cos(math.radians(angle)) * edge_length
    y += math.sin(math.radians(angle)) * edge_length
    yield x, y

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device))
    
    #disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    
    # Clear display.
    disp.clear()
    # Font1 = ImageFont.truetype("../Font/Font01.ttf",30)
    
    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.height, disp.width ), "BLACK")
    draw = ImageDraw.Draw(image1)


    logging.info("draw rectangle")
    draw.rectangle([(135,95),(185,145)],fill = "WHITE",outline="BLUE")
    draw.rectangle([(85,60),(130,110)],fill = "BLUE")
    # draw.text((50, 120), 'Alcohol -> product', fill = "WHITE",font=Font1)
    # hexagon = hexagon_generator(40, offset=(30, 15))
    # hexagon = hexagon_generator(40, offset=(30, 15))
    # draw.polygon(rotatePolygon(polygon=list(hexagon), degrees=90, height=[0,240], width=[0,320]), outline='red', fill='red')
    # logging.info("draw point")

    # draw.rectangle((5,10,6,11), fill = "BLACK")
    # draw.rectangle((5,25,7,27), fill = "BLACK")
    # draw.rectangle((5,40,8,43), fill = "BLACK")
    # draw.rectangle((5,55,9,59), fill = "BLACK")

    # logging.info("draw line")
    # draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
    # draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
    # draw.line([(170,15),(170,55)], fill = "RED",width = 1)
    # draw.line([(150,35),(190,35)], fill = "RED",width = 1)

    # logging.info("draw rectangle")
    # draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
    # draw.rectangle([(85,10),(130,60)],fill = "BLUE")

    # logging.info("draw circle")
    # draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
    # draw.ellipse((150,65,190,105), fill = (0,255,0))

    # logging.info("draw text")
    # Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    # Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    # Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

    # draw.rectangle([(0,65),(140,100)],fill = "WHITE")
    # draw.text((5, 68), 'Hello world', fill = "BLACK",font=Font1)
    # draw.rectangle([(0,115),(190,160)],fill = "RED")
    # draw.text((5, 118), 'WaveShare', fill = "WHITE",font=Font2)
    # draw.text((5, 160), '1234567890', fill = "GREEN",font=Font3)
    # text= u"微雪电子"
    # draw.text((5, 200),text, fill = "BLUE",font=Font3)
    image1=image1.rotate(180)
    disp.ShowImage(image1)
    # time.sleep(3)
    # logging.info("show image")
    
    # image = Image.open('../pic/LCD_2inch.jpg')	
    # image = image.rotate(180)
    # disp.ShowImage(image)
    
    time.sleep(3)
    
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()