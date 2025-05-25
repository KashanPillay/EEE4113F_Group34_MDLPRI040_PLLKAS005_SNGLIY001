#include "types.h"
#include "TinyGPSPlus.h";
#include "HardwareSerial.h";

TinyGPSPlus gps;
HardwareSerial SerialGPS(1);

void setup() {
  Serial.begin(9600); //Serial port of USB
  SerialGPS.begin(9600, SERIAL_8N1, 16, 17); //Serial port of GPS module
}

void loop() {

  while (SerialGPS.available() >0) {
    gps.encode(SerialGPS.read());
  }

  Serial.print("LAT=");  Serial.println(gps.location.lat(), 6);
  Serial.print("LONG="); Serial.println(gps.location.lng(), 6);
  Serial.print("ALT=");  Serial.println(gps.altitude.meters());
    Serial.print("SAT=");  Serial.println(gps.satellites.value());
}