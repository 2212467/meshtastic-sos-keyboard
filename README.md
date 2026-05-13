# Meshtastic SOS Keyboard

Physical emergency button system for Meshtastic networks.

Designed for:
- elderly assistance
- remote homes
- off-grid communication
- emergency alerts

Works fully offline through LoRa mesh.

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

## Main Controller
- Raspberry Pi Zero 2 W

## Meshtastic Node
- LILYGO TTGO LoRa32 V2.1

## Buttons
- 4x momentary push buttons

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

---

# Links used

https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
https://app.cirkitdesigner.com/project
https://pinouthub.com/raspberry-pi-zero/

---

# Installation

```bash
git clone https://github.com/2212467/meshtastic-sos-keyboard.git

cd meshtastic-sos-keyboard

chmod +x install.sh

./install.sh
