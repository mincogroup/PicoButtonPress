import board
import digitalio
import time
import usb_hid
import traceback
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode    

button_pin = board.GP8       # pin to connect button to
led_pin = board.GP6   # pin to connect LED to

# Initializing LED
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

# Initializing Button
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN
    
try:
    keyboard = Keyboard(usb_hid.devices)
    
    while True:
        if button.value:
            keyboard.send(Keycode.F13)
            led.value = True
            time.sleep(1)
            led.value = False
    
except Exception as e:
    if os.stat("/exception.txt")[6] > 262144:
        os.remove("/exception.txt")
    
    file = open("/exception.txt", "a")
    lines = traceback.format_exception(e)
    for l in lines:
        file.write(l)
    file.close()
    
    for i in range(0, 1000):
        led.value = True
        time.sleep(0.3)
        led.value = False
        time.sleep(0.3)
    