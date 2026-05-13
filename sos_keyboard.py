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

rgb = RGBLED(
    red=5,
    green=6,
    blue=13
)

# =========================================
# BUZZER
# =========================================

buzzer = Buzzer(BUZZER_PIN)

# =========================================
# GLOBALS
# =========================================

buttons = []

SEND_COOLDOWN = 10
last_send = 0

# =========================================
# RGB STATES
# =========================================

def led_off():
    rgb.off()

def led_boot():
    rgb.color = (0, 0, 1)   # azul

def led_connecting():
    rgb.color = (1, 0, 1)   # roxo

def led_ready():
    rgb.color = (0, 1, 0)   # verde

def led_sending():
    rgb.color = (1, 1, 0)   # amarelo

def led_error():
    rgb.color = (1, 0, 0)   # vermelho

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
# BUTTONS
# =========================================

for pin, message in BUTTONS.items():

    print(f"[INIT] GPIO {pin} -> {message}")

    btn = Button(
        pin,
        pull_up=True,
        hold_time=LONG_PRESS_SECONDS,
        bounce_time=0.2
    )

    btn.when_held = lambda m=message: send_message(m)

    buttons.append(btn)

# =========================================
# READY
# =========================================

print("[READY] SOS Keyboard running")

try:

    pause()

except KeyboardInterrupt:

    print("\n[EXIT] CTRL+C detected")