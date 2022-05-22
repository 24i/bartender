from PIL import Image,ImageDraw,ImageFont

class ScreenBuilder:

    def __init__(self):
        self.width = 240
        self.height = 320

    def build_home_screen(self):
        # Create blank image for drawing.
        screen = Image.new("RGB", (self.height, self.width ), "BLACK")
        draw = ImageDraw.Draw(screen)

        # image = Image.open('../pic/LCD_2inch.jpg')	
        # image = image.rotate(180)
        # disp.ShowImage(image)
        Font1 = ImageFont.truetype("./fonts/Inter-Regular.ttf", 25)
        draw.text((20, 68), 'ENJOY OUR DRINKS', fill = "WHITE",font=Font1)

        return screen