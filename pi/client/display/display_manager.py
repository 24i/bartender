from PIL import Image,ImageDraw,ImageFont
from libs.LCD  import LCD_2inch
import json
import time
import RPi.GPIO as GPIO
from . import display_helper
from api import api_client

class DisplayManager:
    
    HOME_SCREEN = 'homeScreen'
    INFO_SCREEN = 'infoScreen'
    VOLUME_SCREEN = 'volumeScreen'
    DRINK_SELECT_SCREEN = 'drinkSelectScreen'
    LED_PIN = 13 #BCM

    def __init__(self, activeScreen=HOME_SCREEN):
        self.width = 240
        self.height = 320
        self.counter = 50
        self.ledOn = False
        self.drinkSelected = False
        self.inputDelta = 0
        self.activeScreen = activeScreen
        self.disp = LCD_2inch.LCD_2inch()
        self.disp.Init()
        self.disp.clear()
        self.screen = Image.new("RGB", (self.height, self.width ), "BLACK")
        self.helper = display_helper.DisplayHelper()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_PIN,GPIO.OUT)

    def render(self, counterDelta=0):
        self.inputDelta = counterDelta

        if self.activeScreen == self.HOME_SCREEN:

            self.update_counter(counterDelta)

            self.render_home_screen()
            return

        if self.activeScreen == self.VOLUME_SCREEN:

            self.update_counter(counterDelta)

            self.render_volume_screen()
            return

        if self.activeScreen == self.DRINK_SELECT_SCREEN:

            # Ensure if we're moving away from a selected drink that we dont select the next
            if self.drinkSelected == True:
                self.drinkSelected = False
                self.turn_off_button_led()
            
            self.update_counter(counterDelta)

            self.render_drink_select_screen()
            return

        if self.activeScreen == self.INFO_SCREEN:

            self.update_counter(counterDelta)

            self.render_info_screen()
            return
    
    def on_push(self):
        
        if self.drinkSelected == True:
            print('POURING')
            time.sleep(3)
            self.drinkSelected = False
            self.turn_off_button_led()
            self.return_home()
        else:
            print('NO DRINK SELECTED')

    def on_click(self):
        
        if self.activeScreen == self.HOME_SCREEN:

            # For now a click on home screen can mean we show volume screen
            self.activeScreen = self.VOLUME_SCREEN

            # fa-circle-info
            if self.counter < 33 and self.counter > 0: #info
                self.render_info_screen()
            elif self.counter < 66 and self.counter: #drink select
                self.drinkSelected = False
                self.render_drink_select_screen()
            elif self.counter < 101 and self.counter > 66: #volume
                self.render_volume_screen()
            else:
                return

            return

        if self.activeScreen == self.VOLUME_SCREEN:
            # For now a click on volume screen can mean we show home screen
            self.return_home()
            return

        if self.activeScreen == self.DRINK_SELECT_SCREEN:
            roundedCounter = round(self.counter/50)
            if roundedCounter == 0:
                self.drinkSelected = False
                self.turn_off_button_led()
                self.return_home()
                return

            if self.drinkSelected == False:
                self.drinkSelected = True
            else:
                self.drinkSelected = False
            
            self.render_drink_select_screen()
            return

        if self.activeScreen == self.INFO_SCREEN:
            self.return_home()
            return
    
    def render_home_screen(self):
        self.activeScreen = self.HOME_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()

        textFont = ImageFont.truetype("./fonts/Inter-Regular.ttf", 30)
        draw.text((80, 30), 'ENJOY', fill = "WHITE",font=textFont)
        draw.text((170, 70), 'OUR', fill = "WHITE",font=textFont)
        draw.text((120, 120), 'DRINKS', fill = "WHITE",font=textFont)

        iconFont = ImageFont.truetype("./fonts/fa.otf", 50)

        # fa-circle-info
        infoColour = "RED" if self.counter < 33 and self.counter > 0 else "WHITE"
        draw.text((30, 180), '', fill = infoColour,font=iconFont)

        # glass-water
        volumeColour = "RED" if self.counter < 66 and self.counter > 33 else "WHITE"
        draw.text((150, 180), '', fill = volumeColour,font=iconFont)

        # droplet
        pourColour = "RED" if self.counter < 101 and self.counter > 66 else "WHITE"
        draw.text((260, 180), '', fill = pourColour,font=iconFont)

        self.disp.ShowImage(self.screen)

    def render_volume_screen(self):
        self.activeScreen = self.VOLUME_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()
        iconFontSmall = ImageFont.truetype("./fonts/fa.otf", 30)
        iconFontLarge = ImageFont.truetype("./fonts/fa.otf", 60)

        self.helper.draw_header(draw=draw, text='VOLUME ADJUSTMENT')

        draw.rectangle([(33,93),(287,147)],outline="RED")
        draw.rectangle([(35,95),(35 + (self.counter * 2.5),145)],fill = "RED",outline="RED")

        draw.text((18, 185), "", fill = "WHITE",font=iconFontSmall)
        draw.text((250, 160), "", fill = "WHITE",font=iconFontLarge)
        self.disp.ShowImage(self.screen)

    def render_drink_select_screen(self):
        self.activeScreen = self.DRINK_SELECT_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()
        self.helper.draw_header(draw=draw, text='DRINK SELECTION')
        apiClient = api_client.APIClient()
        iconFontSmall = ImageFont.truetype("./fonts/fa.otf", 30)
        iconFontLarge = ImageFont.truetype("./fonts/fa.otf", 70)

        # cocktail-glass, whiskey-glass, glass-water, wine-glass
        icons = ["","","",""]

        drinks = apiClient.fetch_drinks()

        iconCounter = 0
        for drink in drinks:
            drink['icon'] = icons[iconCounter]
            
            if (iconCounter + 1) == len(icons):
                iconCounter = 0
            else:
                iconCounter = iconCounter + 1

        # Add home option
        home = {"icon":"","name":"Home"}
        drinks.insert(0, home)

        # round counter
        roundedCounter = round(self.counter/50)

        if roundedCounter >= len(drinks):
            roundedCounter = len(drinks) - 1

        selectedDrink = drinks[roundedCounter]

        # Resolve items to render
        mainIconColour = "RED" if self.drinkSelected == True else "WHITE"
        draw.text((125, 90), selectedDrink['icon'], fill = mainIconColour,font=iconFontLarge)
        self.helper.draw_footer(draw=draw, text=selectedDrink['name'])

        if roundedCounter >= 1:
            previousDrink = drinks[roundedCounter - 1]
            draw.text((40, 90), previousDrink['icon'], fill = "WHITE",font=iconFontSmall)

        if (len(drinks) - 1) > roundedCounter:
            nextDrink = drinks[roundedCounter + 1]
            draw.text((235, 90), nextDrink['icon'], fill = "WHITE",font=iconFontSmall)
        
        if self.drinkSelected == True:
            self.turn_on_button_led()
        else:
            self.turn_off_button_led()

        self.disp.ShowImage(self.screen)

    def render_info_screen(self):
        self.activeScreen = self.INFO_SCREEN

        # Create blank image for drawing.
        draw = self.build_fresh_screen()

        self.helper.draw_header(draw=draw, text='BARTENDER INFO')

        self.disp.ShowImage(self.screen)

    def toggle_button_led(self):
        if self.ledOn == False:
            self.turn_on_button_led()
            return
        if self.ledOn == True:
            self.turn_off_button_led()
            return

    def turn_off_button_led(self):
        self.ledOn = False
        GPIO.output(self.LED_PIN,GPIO.LOW)
    
    def turn_on_button_led(self):
        self.ledOn = True
        GPIO.output(self.LED_PIN,GPIO.HIGH)

    # Build & set screen obj and return associated draw obj
    def build_fresh_screen(self):
        self.screen = Image.new("RGB", (self.height, self.width ), "BLACK")
        return ImageDraw.Draw(self.screen)

    def update_counter(self, delta, scale=True, limit=True, lowerLimit=0, upperLimit=100):

         # delta/2 because enconder seems to step in multiples of 2 to 4 
        if scale == True:
            delta = delta/2
        
        if limit == True:
            self.counter = self.counter + delta
            return
        
        if (self.counter + delta) > 100:
            self.counter=100
        elif (self.counter + delta) < 0:
            self.counter=0
        else:
            self.counter = self.counter + delta

    def return_home(self):
        self.counter= 50
        self.activeScreen = self.HOME_SCREEN
        self.render_home_screen()