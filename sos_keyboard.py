from meshtastic.serial_interface import SerialInterface
from gpiozero import Buzzer
import gpiod
import serial.tools.list_ports

import time
import atexit
import sys

# =========================================
# CONFIG
# =========================================

from config import (
    BUTTONS,
    BUZZER_PIN,
    LONG_PRESS_SECONDS
)

# optional configs
try:
    from config import MESHTASTIC_PORT
except:
    MESHTASTIC_PORT = None

try:
    from config import SEND_COOLDOWN
except:
    SEND_COOLDOWN = 10

# =========================================
# GPIO CHIP
# =========================================

GPIO_CHIP = "/dev/gpiochip0"

chip = gpiod.Chip(GPIO_CHIP)

# =========================================
# BUZZER
# =========================================

buzzer = Buzzer(BUZZER_PIN)

def beep(t=0.2):

    buzzer.on()
    time.sleep(t)
    buzzer.off()

# =========================================
# GLOBALS
# =========================================

iface = None
buttons = {}

last_send = 0

# =========================================
# CLEANUP
# =========================================

def cleanup():

    print("\n[CLEANUP] Closing application")

    try:
        buzzer.off()
    except:
        pass

    try:
        if iface:
            iface.close()
    except:
        pass

atexit.register(cleanup)

# =========================================
# DETECT SERIAL DEVICES
# =========================================

def list_serial_ports():

    print("[DEBUG] Available serial ports:")

    ports = serial.tools.list_ports.comports()

    for port in ports:
        print(f" - {port.device} | {port.description}")

# =========================================
# CONNECT MESHTASTIC
# =========================================

def connect_meshtastic():

    global iface

    while True:

        try:

            print("[CONNECT] Searching Meshtastic node...")

            list_serial_ports()

            # =====================================
            # MANUAL PORT
            # =====================================

            if MESHTASTIC_PORT:

                print(f"[CONNECT] Using manual port: {MESHTASTIC_PORT}")

                iface = SerialInterface(
                    devPath=MESHTASTIC_PORT
                )

            # =====================================
            # AUTO-DETECT
            # =====================================

            else:

                print("[CONNECT] Using auto-detect")

                iface = SerialInterface()

            time.sleep(2)

            # validate connection
            if iface.nodes:

                print("[OK] Meshtastic connected")

                beep(0.1)

                return True

            else:

                raise Exception("No nodes detected")

        except Exception as e:

            print(f"[ERROR] Connection failed: {e}")

            beep(0.5)

            try:
                iface.close()
            except:
                pass

            print("[RETRY] Reconnecting in 5 seconds...")

            time.sleep(5)

# =========================================
# SEND MESSAGE
# =========================================

def send_message(message):

    global last_send
    global iface

    # =====================================
    # COOLDOWN
    # =====================================

    if time.time() - last_send < SEND_COOLDOWN:

        print("[WARN] Cooldown active")

        beep(0.05)

        return

    last_send = time.time()

    print(f"[SEND] {message}")

    # =====================================
    # SEND + ACK
    # =====================================

    try:

        response = iface.sendText(
            text=message,
            wantAck=True
        )

        # =================================
        # ACK OK
        # =================================

        if response:

            print("[ACK] Message acknowledged")

            beep(0.2)

        else:

            print("[WARN] No ACK received")

            beep(0.5)

    # =====================================
    # CONNECTION LOST
    # =====================================

    except Exception as e:

        print(f"[ERROR] Send failed: {e}")

        beep(0.6)

        print("[RECONNECT] Attempting reconnect...")

        connect_meshtastic()

        # =================================
        # RETRY ONCE
        # =================================

        try:

            response = iface.sendText(
                text=message,
                wantAck=True
            )

            if response:

                print("[OK] Message sent after reconnect")

                beep(0.2)

            else:

                print("[WARN] Reconnected but no ACK")

                beep(0.5)

        except Exception as e:

            print(f"[FATAL] Retry failed: {e}")

            beep(1)

# =========================================
# BUTTON SETUP
# =========================================

for pin, message in BUTTONS.items():

    print(f"[INIT] GPIO {pin} -> {message}")

    request = chip.request_lines(
        config={
            pin: gpiod.LineSettings(
                direction=gpiod.line.Direction.INPUT,
                bias=gpiod.line.Bias.PULL_UP
            )
        }
    )

    buttons[pin] = {
        "request": request,
        "message": message,
        "pressed_time": None
    }

print("[READY] GPIO initialized")

# =========================================
# CONNECT
# =========================================

connect_meshtastic()

# =========================================
# MAIN LOOP
# =========================================

print("[READY] SOS Keyboard running")

try:

    while True:

        for pin, data in buttons.items():

            value = data["request"].get_value(pin)

            # active LOW
            if value == gpiod.line.Value.INACTIVE:

                # first press
                if data["pressed_time"] is None:

                    data["pressed_time"] = time.time()

                # long press detected
                elif time.time() - data["pressed_time"] >= LONG_PRESS_SECONDS:

                    send_message(data["message"])

                    # wait release
                    while data["request"].get_value(pin) == gpiod.line.Value.INACTIVE:
                        time.sleep(0.05)

                    data["pressed_time"] = None

            else:

                data["pressed_time"] = None

        time.sleep(0.05)

except KeyboardInterrupt:

    print("\n[EXIT] CTRL+C")