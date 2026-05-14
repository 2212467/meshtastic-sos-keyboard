# Meshtastic SOS Keyboard

Physical emergency button system for Meshtastic networks.

Designed for:
- elderly assistance
- remote homes
- off-grid communication
- emergency alerts

Works fully offline through LoRa mesh.

NOTE: After pressing the button for 2sec, it will send the message to the PRIMARY channel.

---

# Features

- 🚨 SOS emergency button
- 📞 CALL request
- ✅ OK status
- 🆘 HELP request
- long-press protection
- LED + buzzer feedback
- works without Internet
- uses official Meshtastic firmware

---

# Hardware
- Raspberry Pi (Zero / 3 / 4 / 5)
- Node Meshtastic connected by USB (ex: LILYGO / T-Beam / etc.) (must accept serial connection)
- 4x push buttons
- 3x 220Ω resistor
- 1x RBG led
- 1x Buzzer
- Lots of breadboard jumper wires
- USB cable to connect Rasp <-> Meshtastic

## Tested with
- Raspberry Pi 4B (Debian GNU/Linux 13 (trixie))
- LILYGO TTGO LoRa32 V2.1 (Meshtastic 2.7.22 Alpha)

---

# GPIO Mapping

| GPIO | Function |
|---|---|
| 17 | SOS |
| 27 | CALL |
| 22 | OK |
| 23 | HELP |
| O5 | RED COLOR |
| O6 | GREEN COLOR |
| 13 | BLUE COLOR |
| 18 | Buzzer |
| 06 | Groung |

Check: https://github.com/2212467/meshtastic-sos-keyboard/blob/main/wiring/gpio_map.png

---

# Installation

```bash
curl -sSL https://raw.githubusercontent.com/2212467/meshtastic-sos-keyboard/refs/heads/main/install.sh | bash
```

---

# health-check LED (GPIO status systemd)
- Blue = boot
- Green = ready
- Red = error

---

# Debug
- Led color is RED

Check meshtastic connection (must be inside myenv)
```bash
meshtastic --info
```

---

# Links used

https://www.raspberrypi.com/documentation/computers/raspberry-pi.html

https://app.cirkitdesigner.com/project

https://pinouthub.com/raspberry-pi-zero/

http://chatgpt.com
