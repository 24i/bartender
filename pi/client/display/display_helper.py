from PIL import Image,ImageDraw,ImageFont

class DisplayHelper:

    def __init__(self):
        self.width = 240
        self.height = 320

    def draw_header(self, draw, text):

        textFont = ImageFont.truetype("./fonts/Inter-Regular.ttf", 24)
        draw.text((15, 15), text, fill = "WHITE",font=textFont)

    def draw_footer(self, draw, text):

        textFont = ImageFont.truetype("./fonts/Inter-Regular.ttf", 22)
        draw.text((15, 200), text, fill = "WHITE",font=textFont)