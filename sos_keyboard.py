from gpiozero import Device
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()

from gpiozero import Button, Buzzer, RGBLED
from signal import pause
from meshtastic.serial_interface import SerialInterface
from config import *

import time
import atexit
import sys

# =========================================
# RGB LED
# =========================================

from gpiozero import OutputDevice

RED = OutputDevice(5)
GREEN = OutputDevice(6)
BLUE = OutputDevice(13)

# =========================================
# RGB FUNCTIONS
# =========================================

def rgb_off():
    RED.off()
    GREEN.off()
    BLUE.off()

def rgb_red():
    RED.on()
    GREEN.off()
    BLUE.off()

def rgb_green():
    RED.off()
    GREEN.on()
    BLUE.off()

def rgb_blue():
    RED.off()
    GREEN.off()
    BLUE.on()

def rgb_yellow():
    RED.on()
    GREEN.on()
    BLUE.off()

def rgb_purple():
    RED.on()
    GREEN.off()
    BLUE.on()

# =========================================
# ALIASES (para não mexer no resto do código)
# =========================================

def led_boot():
    rgb_blue()

def led_connecting():
    rgb_purple()

def led_ready():
    rgb_green()

def led_sending():
    rgb_yellow()

def led_error():
    rgb_red()

# =========================================
# BUZZER
# =========================================

buzzer = Buzzer(BUZZER_PIN)

# =========================================
# GLOBALS
# =========================================

buttons = {}

SEND_COOLDOWN = 10
last_send = 0

# =========================================
# RGB STATES
# =========================================

def rgb_off():
    RED.off()
    GREEN.off()
    BLUE.off()

def rgb_red():
    RED.on(); GREEN.off(); BLUE.off()

def rgb_green():
    RED.off(); GREEN.on(); BLUE.off()

def rgb_blue():
    RED.off(); GREEN.off(); BLUE.on()

def rgb_yellow():
    RED.on(); GREEN.on(); BLUE.off()

def rgb_purple():
    RED.on(); GREEN.off(); BLUE.on()

# =========================================
# BUZZER
# =========================================

def beep(duration=0.2):

    buzzer.on()
    time.sleep(duration)
    buzzer.off()

# =========================================
# CLEANUP
# =========================================

def cleanup():

    print("\n[CLEANUP] Closing application")

    led_off()
    buzzer.off()

    try:
        iface.close()
    except:
        pass

atexit.register(cleanup)

# =========================================
# STARTUP
# =========================================

print("[BOOT] Starting SOS Keyboard")

led_boot()

time.sleep(1)

# =========================================
# CONNECT TO MESHTASTIC
# =========================================

try:

    print("[BOOT] Connecting to Meshtastic node...")

    led_connecting()

    iface = SerialInterface()

    time.sleep(2)

    if iface.nodes:

        print("[OK] Meshtastic connected")

        led_ready()
        beep(0.1)

        time.sleep(1)

        led_off()

    else:

        raise Exception("No Meshtastic nodes found")

except Exception as e:

    print(f"[ERROR] Failed to connect: {e}")

    led_error()
    beep(1)

    sys.exit(1)

# =========================================
# SEND MESSAGE
# =========================================

def send_message(message):

    global last_send

    # anti-spam cooldown
    if time.time() - last_send < SEND_COOLDOWN:

        print("[WARN] Cooldown active")

        beep(0.05)

        return

    last_send = time.time()

    try:

        print(f"[SEND] {message}")

        led_sending()

        print("[DEBUG] About to call sendText()")

        iface.sendText(
            text=message,
            wantAck=True
        )

        # Success
        led_ready()
        beep(0.2)

        time.sleep(1)

        led_off()

        print("[OK] Message sent")

    except Exception as e:

        print(f"[ERROR] Send failed: {e}")

        led_error()

        beep(0.5)

        time.sleep(1)

        led_off()


# =========================================
# BUTTON SETUP
# =========================================

for pin, message in BUTTONS.items():

    print(f"[INIT] GPIO {pin} -> {message}")

    buttons[pin] = {
        "button": Button(
            pin,
            pull_up=True,
            bounce_time=0.1
        ),
        "message": message,
        "pressed_time": None
    }

print("[READY] SOS Keyboard running")

# =========================================
# MAIN LOOP
# =========================================

try:

    while True:

        for pin, data in buttons.items():

            btn = data["button"]

            # botão carregado
            if btn.is_pressed:

                # primeira deteção
                if data["pressed_time"] is None:

                    data["pressed_time"] = time.time()

                # long press
                elif time.time() - data["pressed_time"] >= LONG_PRESS_SECONDS:

                    send_message(data["message"])

                    # esperar libertar botão
                    while btn.is_pressed:
                        time.sleep(0.1)

                    data["pressed_time"] = None

            else:

                data["pressed_time"] = None

        time.sleep(0.05)

except KeyboardInterrupt:

    print("\n[EXIT] CTRL+C detected")