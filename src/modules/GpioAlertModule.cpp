#include <Arduino.h>

// GPIO mapping
#define BTN_SOS   25
#define BTN_CALL  26
#define BTN_OK    27
#define BTN_HELP  32

static uint32_t lastSend = 0;

void sendMessage(const char *msg) {

    if (millis() - lastSend < 2500)
        return;

    lastSend = millis();

    Serial.println(msg); // aqui depois liga ao Meshtastic
}

void initGpioAlertModule() {

    pinMode(BTN_SOS, INPUT_PULLUP);
    pinMode(BTN_CALL, INPUT_PULLUP);
    pinMode(BTN_OK, INPUT_PULLUP);
    pinMode(BTN_HELP, INPUT_PULLUP);
}

static bool pressed(int pin) {

    if (digitalRead(pin) == LOW) {
        delay(40);
        return digitalRead(pin) == LOW;
    }

    return false;
}

void loopGpioAlertModule() {

    if (pressed(BTN_SOS)) {
        sendMessage("SOS");
        while (digitalRead(BTN_SOS) == LOW);
    }

    if (pressed(BTN_CALL)) {
        sendMessage("CALL");
        while (digitalRead(BTN_CALL) == LOW);
    }

    if (pressed(BTN_OK)) {
        sendMessage("OK");
        while (digitalRead(BTN_OK) == LOW);
    }

    if (pressed(BTN_HELP)) {
        sendMessage("HELP");
        while (digitalRead(BTN_HELP) == LOW);
    }
}