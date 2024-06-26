# PicoButtonPress
code to make a raspberry pi pico send F13 and light an LED when a button is pressed

#instructions
- Press `code` (green button) -> `download zip`
- Extract the downloaded folder and keep file explorer open.
- Hold down BOOTSEL button on pico and plug into computer.
- Relaese BOOTSEL once pico appears like a flash drive in file explorer.
- Drag `adafruit-circuitpython-raspberry_pi_pico-en_US-9.0.0.uf2` from downloaded folder onto the pico.
- Once the file transfer is complete, the pico will automatically disconnect and reappear as "CIRCUITPY".
- Copy the `adafruit_hid` folder from the downloaded folder and paste it inside the `lib` folder on the pico.
- Copy `code.py`, `boot.py`, and `exception.txt` files from the downloaded folder onto the pico, replacing the existing ones if any.
- MAKE SURE ALL FILES ARE COPIED BEFORE UNPLUGGING THE PICO! The filesystem will be read only after the pico is restarted. If any mistakes are made, start over form the BOOTSEL step.
- Wire up the pico using the attached diagram.
- When testing, keep in mind the LED will not light unless the pico is plugged into a computer (a power brick will not work).
