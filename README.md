# Meshtastic SOS Keyboard

Physical emergency button system for Meshtastic networks.

Designed for:
- elderly assistance
- remote homes
- off-grid communication
- emergency alerts

Works fully offline through LoRa mesh.

NOTE: After pressing the button for 2sec, it will send the message to the PRIMARY channel.

![Testing](https://github.com/2212467/meshtastic-sos-keyboard/blob/main/testing.jpeg)

---

# Features

- 🆘 SOS emergency button
- 📞 CALL request button
- ✅ OK status button
- ⚠️ Visit request button
- long-press protection
- LED + buzzer feedback
- works without Internet
- uses official Meshtastic firmware

NOTE: Default button messages can be changed on `config.sh`

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
- Raspberry Pi 4B (Raspberry Pi OS 64-bit - Debian GNU/Linux 13 (trixie))
- LILYGO TTGO LoRa32 V2.1 (Meshtastic 2.7.22 Alpha)

---

# GPIO Mapping

| GPIO | Function |
|---|---|
| 17 | SOS |
| 27 | CALL |
| 22 | OK |
| 23 | VISIT |
| O5 | RED COLOR |
| O6 | GREEN COLOR |
| 13 | BLUE COLOR |
| 18 | Buzzer |
| 06 | Groung |

![GPIO MAP](https://github.com/2212467/meshtastic-sos-keyboard/blob/main/wiring/gpio_map.png)
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

## LED Status Codes

| Color | Meaning |
|---|---|
| Blue | Booting |
| Purple | Connecting to Meshtastic |
| Green | Connected / ACK success |
| Yellow | Sending message |
| Red | Error / ACK failure |

## Buzzer Codes

| Sound | Meaning |
|---|---|
| Short beep | Success |
| Long beep | Error |
| Double short beep | Startup |

---

# Debug

### No Meshtastic Device Found
*(must be inside myenv)*
```bash
meshtastic --info
```
If not detected:
- replace USB cable
- verify Meshtastic firmware
- reconnect device

### Check GPIO access
```bash
ls /dev/gpiochip*
```

### Buttons Not Working
Verify wiring:

GPIO -> BUTTON -> GND

### RGB LED Always On
Possible causes:
- common anode vs common cathode mismatch
- wrong polarity
- missing resistor

---

# Safety Notes
This project is intended as:
- emergency aid tool
- offline communication system
- community resilience platform

It should not replace:
- certified emergency systems
- official rescue equipment
- medical alert systems

**Always test your mesh network coverage before real-world deployment.**

# License
Recommended license:
`MIT License`
*Simple, open-source, community-friendly.*

# Credits
Built using:
- [Meshtastic Portugal](https://meshtastic.pt/)
- [Meshtastic Official Website](https://meshtastic.org/)
- [Meshtastic Python API](https://github.com/meshtastic/python)
- [gpiozero Documentation](https://gpiozero.readthedocs.io/)
- [Raspberry Pi Official Website](https://www.raspberrypi.com/)
- [ChatGPT](https://chatgpt.com)
