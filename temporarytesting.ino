#include "driver/ledc.h"

  float sample=0;
  float voltage =0;

void setup() {
  bool ledcSetClockSource(ledc_clk_cfg_t source);

  ledcAttach(18, 100, 10);
  ledcAttach(19, 100, 10);
  ledcWrite(18,512);
  ledcWrite(19,512);
  ledcOutputInvert(18,true);


   // Initialize serial communication
  Serial.begin(115200);
  delay(1000);
  Serial.println("Starting continuous ADC sampling...");
  float myArray[4000];
  float sample=0;
  float voltage =0;

  for (int i = 0; i < 4000; i++) {
    sample = analogRead(34);
    myArray[i] = (float)sample / 4095.0 * 3.3;
    Serial.print(myArray[i]);
    if (i < 3999) Serial.print(","); // Comma-separated
    delayMicroseconds(200);
  }
}
void loop() { 
    sample = analogRead(34);
    voltage = (float)sample / 4095.0 * 3.3;
    Serial.println(voltage);
    delayMicroseconds(200);

  }

  