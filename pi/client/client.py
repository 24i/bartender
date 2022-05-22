# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

from libs.Encoder import rotary_encoder
from libs import switch
from libs import gpio
from display import display_manager
import time
import sys
import spidev as SPI
sys.path.append("..")

A_PIN  = 21
B_PIN  = 9
SW_PIN = 8

last_button_state = 0

gpio = gpio.GPIO()
encoder = rotary_encoder.RotaryEncoder.Worker(gpio, A_PIN, B_PIN)
encoder.start()
switch = switch.Switch(gpio, SW_PIN)

# Show home screen 
displayManager = display_manager.DisplayManager()
displayManager.render()

while True:

    delta = encoder.get_steps()
    if delta!=0:
        # Re-render the screen if theres a change in encoder position
        # delta/2 because enconder seems to step in multiples of 2 to 4 
        displayManager.render(delta/2)
    else:
        time.sleep(0.05)

    sw_state = switch.get_state()
    if sw_state != last_button_state:
        last_button_state = sw_state

        # Trigger click handler when switch is toggled (but only on up state)
        if sw_state > 0:
            displayManager.on_click()


displayManager.disp.module_exit()