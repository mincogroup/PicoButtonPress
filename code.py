# pico_button_debounce.py
# CircuitPython (8.x/9.x) -- Raspberry Pi Pico
#
# Sampled-integrator debouncer for a macro button with LED:
#   * Raw GPIO is sampled on a strict 1 kHz schedule (busy-wait, zero drift).
#   * A state change is accepted only after DEBOUNCE_SAMPLES consecutive
#     samples agree. Bouncing can never "reset a timer", so a press is
#     never swallowed -- the integrator latches whatever the contact did.
#   * Every raw edge is timestamped into a ring buffer and dumped over
#     serial with the LED state at that instant, so you can correlate
#     phantom edges with LED switching (EMI/supply-droop diagnosis).
#   * Chatter / super-fast taps show up as logged "short pulse" lines
#     instead of spurious key events.
#   * on_press()/on_release() are the hooks for your F13 keycode.
#
# Wiring: button between GP8 and 3V3 (normally open).
#   Pin idles LOW (False = released); pressing pulls it HIGH (True = pressed).
# Keep the internal pull-down as a fallback, but fit an external 4.7k-10k
# pull-down from GP8 to GND for real noise immunity.
import board
import digitalio
import time
from collections import deque
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ----------------------- configuration -----------------------
BUTTON_PIN = board.GP8          # button input
LED_PIN = board.GP6             # LED control (on while pressed, plus LED_HOLD_MS)
SAMPLE_PERIOD_MS = 1            # 1 kHz raw sampling
DEBOUNCE_SAMPLES = 25           # consecutive agreeing samples => 25 ms to accept
SHORT_PULSE_MS = 15             # pulses shorter than this are logged as noise
LOG_DEPTH = 128                 # raw-edge ring buffer size
HEARTBEAT_MS = 1000             # periodic status line; 0 disables
LED_HOLD_MS = 1000              # LED stays lit this long after a release

# ----------------------- hardware -----------------------
button = digitalio.DigitalInOut(BUTTON_PIN)
button.switch_to_input(pull=digitalio.Pull.DOWN)

led = digitalio.DigitalInOut(LED_PIN)
led.switch_to_output(value=False)

keyboard = Keyboard(usb_hid.devices)

# ----------------------- raw edge log -----------------------
# entries: (ms, edge, led_state) -- edge: "R"=rising/press, "F"=falling/release
edge_log = deque((), LOG_DEPTH)
def log_edge(ms, edge):
    # Sampling must never stall on logging: ring buffer, drop oldest.
    if len(edge_log) >= LOG_DEPTH:
        edge_log.popleft()
    edge_log.append((ms, edge, led.value))
def drain_log():
    # Batch-drain over serial; runs rarely (only when edges occurred).
    while edge_log:
        ms, edge, led_state = edge_log.popleft()
        kind = "PRESS-raw  " if edge == "R" else "RELEASE-raw"
        print("t=%8d ms  %s  led=%d" % (ms, kind, led_state))
        
# ----------------------- debounced state -----------------------
debounced = False               # False = released (pull-down idles low)
counter = 0                     # consecutive samples disagreeing with debounced
press_count = 0
led_off_deadline = 0            # monotonic_ns time to turn LED off; 0 = none

# ----------------------- your hooks -----------------------
def on_press():
    print(">>> PRESS event #%d" % press_count)
def on_release():
    print(">>> release event")
    keyboard.send(Keycode.F13)
    
# ----------------------- main sampling loop -----------------------
period_ns = SAMPLE_PERIOD_MS * 1_000_000
next_sample = time.monotonic_ns() + period_ns
last_heartbeat = time.monotonic_ns()
while True:
    now = time.monotonic_ns()
    # Heartbeat/status line (does not interfere with sampling timing)
    if HEARTBEAT_MS and now - last_heartbeat >= HEARTBEAT_MS * 1_000_000:
        last_heartbeat = now
        print("status: debounced=%s counter=%d presses=%d"
              % ("PRESSED" if debounced else "RELEASED", counter, press_count))
    # Turn the LED off LED_HOLD_MS after a release (a new press cancels it)
    if led_off_deadline and not debounced and now >= led_off_deadline:
        led_off_deadline = 0
        led.value = False

    # Flush any logged edges before taking the next sample
    if edge_log:
        drain_log()
    # Busy-wait to the next sample instant -- keeps sample jitter near zero
    # (time.sleep() would not, and missed samples = missed presses).
    while now < next_sample:
        now = time.monotonic_ns()
    next_sample += period_ns
    # ---- raw sample ----
    raw = button.value          # True = pressed, False = released
    if raw != debounced:
        # Disagreeing sample: count consecutive disagreement.
        if counter == 0:
            log_edge(now // 1_000_000, "R" if raw else "F")
        counter += 1
        if counter >= DEBOUNCE_SAMPLES:
            # Confirmed state change -- latch it.
            debounced = raw
            counter = 0
            if raw:
                press_count += 1
                led.value = True
                led_off_deadline = 0      # cancel a pending LED turn-off
                on_press()
            else:
                # Keep the LED lit for LED_HOLD_MS after release; the
                # main loop turns it off when the deadline passes.
                led_off_deadline = now + LED_HOLD_MS * 1_000_000
                on_release()
    elif counter:
        # Raw snapped back to the debounced state before the window
        # completed: a short pulse (bounce or a tap faster than the
        # window). Log it for diagnosis, emit NO key event.
        pulse_ms = counter * SAMPLE_PERIOD_MS
        print("t=%8d ms  SHORT-PULSE %d ms ignored" % (now // 1_000_000, pulse_ms))
        counter = 0