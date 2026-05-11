#include <Arduino.h>
#include "modules/GpioAlertModule.h"

void setup() {

    Serial.begin(115200);

    initGpioAlertModule();
}

void loop() {

    loopGpioAlertModule();
}