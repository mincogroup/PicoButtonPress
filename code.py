import board
import digitalio
import time
import usb_hid
import traceback
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

try:
    keyboard = Keyboard(usb_hid.devices)

    button_pin = board.GP8       # pin to connect button to
    led_pin = board.GP6   # pin to connect LED to

    # Initializing LED
    led = digitalio.DigitalInOut(led_pin)
    led.direction = digitalio.Direction.OUTPUT

    # Initializing Button
    button = digitalio.DigitalInOut(button_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.DOWN


    while True:
        if button.value:
            keyboard.send(Keycode.F13)
            led.value = True
            time.sleep(1)
            led.value = False
    
except Exception as e:
    file = open("/exception.txt", "a")
    lines = traceback.format_exception(e)
    for l in lines:
        file.write(l)
    file.close()