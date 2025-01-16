import board
import digitalio
import storage

button_pin = board.GP8

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

storage.remount("/", button.value)