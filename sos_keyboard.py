from meshtastic.serial_interface import SerialInterface
from gpiozero import Buzzer
import gpiod
import time
import atexit
import sys

# =========================================
# CONFIG (ajusta no teu config.py se quiseres)
# =========================================
from config import BUTTONS, BUZZER_PIN, LONG_PRESS_SECONDS

# =========================================
# GPIO CHIP (AJUSTA SE NECESSÁRIO)
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
# MESHTASTIC
# =========================================
iface = None

# =========================================
# BUTTON SETUP (GPIOD MODERNO)
# =========================================
buttons = {}

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

print("[READY] SOS Keyboard running")

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
# CONNECT MESHTASTIC
# =========================================
try:
    print("[BOOT] Connecting to Meshtastic node...")

    iface = SerialInterface()

    time.sleep(1)

    print("[OK] Meshtastic connected")

except Exception as e:
    print(f"[ERROR] Meshtastic failed: {e}")
    sys.exit(1)

# =========================================
# SEND MESSAGE
# =========================================
def send_message(message):
    print(f"[SEND] {message}")

    try:
        iface.sendText(
            text=message,
            wantAck=True
        )

        beep(0.2)
        print("[OK] Sent")

    except Exception as e:
        print(f"[ERROR] {e}")
        beep(0.6)

# =========================================
# LOOP PRINCIPAL
# =========================================
try:
    while True:

        for pin, data in buttons.items():

            value = data["request"].get_value(pin)

            # ativo LOW (pull-up)
            if value == gpiod.line.Value.INACTIVE:

                if data["pressed_time"] is None:
                    data["pressed_time"] = time.time()

                elif time.time() - data["pressed_time"] >= LONG_PRESS_SECONDS:

                    send_message(data["message"])

                    # esperar libertar botão
                    while data["request"].get_value(pin) == gpiod.line.Value.INACTIVE:
                        time.sleep(0.05)

                    data["pressed_time"] = None

            else:
                data["pressed_time"] = None

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n[EXIT] CTRL+C")