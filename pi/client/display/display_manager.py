from PIL import Image,ImageDraw,ImageFont
from libs.LCD  import LCD_2inch

class DisplayManager:
    
    HOME_SCREEN = 'homeScreen'
    VOLUME_SCREEN = 'volumeScreen'
    DRINK_SELECT_SCREEN = 'drinkSelectScreen'

    def __init__(self, activeScreen=HOME_SCREEN):
        self.width = 240
        self.height = 320
        self.counter = 0
        self.activeScreen = activeScreen
        self.disp = LCD_2inch.LCD_2inch()
        self.disp.Init()
        self.disp.clear()
        self.screen = Image.new("RGB", (self.height, self.width ), "BLACK")

    def render(self, counterDelta=0):
        self.update_counter(counterDelta)

        if self.activeScreen == self.HOME_SCREEN:
            self.render_home_screen()
            return

        if self.activeScreen == self.VOLUME_SCREEN:
            self.render_volume_screen()
            return

        if self.activeScreen == self.DRINK_SELECT_SCREEN:
            self.render_drink_select_screen()
            return

    def on_click(self):
        
        if self.activeScreen == self.HOME_SCREEN:
            # For now a click on home screen can mean we show volume screen
            self.activeScreen = self.VOLUME_SCREEN
            self.render_volume_screen()
            return

        if self.activeScreen == self.VOLUME_SCREEN:
            # For now a click on home screen can mean we show volume screen
            self.activeScreen = self.HOME_SCREEN
            self.render_home_screen()
            return

        if self.activeScreen == self.DRINK_SELECT_SCREEN:
            print("SELECT CLICK")
            return
    
    def render_home_screen(self):
        self.activeScreen = self.HOME_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()

        Font1 = ImageFont.truetype("./fonts/Inter-Regular.ttf", 25)
        draw.text((20, 68), 'ENJOY OUR DRINKS', fill = "WHITE",font=Font1)
        self.disp.ShowImage(self.screen)

    def render_volume_screen(self):
        self.activeScreen = self.VOLUME_SCREEN

         # Create blank image for drawing.
        draw = self.build_fresh_screen()

        draw.rectangle([(35,95),(85 + self.counter,145)],fill = "RED",outline="RED")

        self.disp.ShowImage(self.screen)

    def render_drink_select_screen(self):
        self.activeScreen = self.DRINK_SELECT_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()

        Font1 = ImageFont.truetype("./fonts/Inter-Regular.ttf", 25)
        draw.text((20, 68), 'SELECT', fill = "WHITE",font=Font1)
        self.disp.ShowImage(self.screen)

    # Build & set screen obj and return associated draw obj
    def build_fresh_screen(self):
        self.screen = Image.new("RGB", (self.height, self.width ), "BLACK")
        return ImageDraw.Draw(self.screen)

    def update_counter(self, delta):
        if (self.counter + delta) > 100:
            self.counter=100
        elif (self.counter + delta) < 0:
            self.counter=0
        else:
            self.counter = self.counter + delta