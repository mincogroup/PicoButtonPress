# PicoButtonPress
code to make a raspberry pi pico send F13 and light an LED when a button is pressed

# Instructions
- Press `code` (green button) -> `download zip`
- Extract the downloaded folder and keep file explorer open.
- Wire up the pico using the attached diagram.
- Hold down BOOTSEL button on pico and plug into computer.
- Relaese BOOTSEL once pico appears like a flash drive in file explorer.
- Drag `adafruit-circuitpython-raspberry_pi_pico-en_US-9.0.0.uf2` from downloaded folder onto the pico.
- Once the file transfer is complete, the pico will automatically disconnect and reappear as "CIRCUITPY".
- Copy the `adafruit_hid` folder from the downloaded folder and paste it inside the `lib` folder on the pico.
- Copy `code.py`, `boot.py`, and `exception.txt` files from the downloaded folder onto the pico, replacing the existing ones if any.
- MAKE SURE ALL FILES ARE COPIED BEFORE UNPLUGGING THE PICO! The filesystem will become read only after the pico is restarted if the boot.py file was copied successfully. If any mistakes are made, unplug the pico and hold the green button while plugging it back in. Do not release the button until the device is recognized. This will make the filesystem writeable again until the next restart.
- When testing, keep in mind the LED will not light unless the pico is plugged into a computer (a power brick will not work).

# Updating a device
- Plug device into computer
- Copy the new `boot.py`, `code.py`, and `exception.txt` files onto the device
- WARNING: The filesystem will become read only after the pico is restarted if the `boot.py` file was copied successfully. If any mistakes are made, unplug the pico and hold the green button while plugging it back in. Do not release the button until the device is recognized. This will make the filesystem writeable again until the next restart.
- To check errors on the pico, open the `exception.txt` file.
- If you wish to clear out the file, use the above two steps to make the filesystem writeable. Then simply delete the contents of the file. DO NOT DELETE THE FILE!