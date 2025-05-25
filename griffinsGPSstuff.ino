#include <HardwareSerial.h>

static const int RXPin = 16, TXPin = 17;
static const uint32_t GPSBaud = 9600;

// The serial connection to the GPS module
HardwareSerial gpsSerial(1);

void setup(){
  Serial.begin(9600);
  gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);
}

void loop(){
  while (gpsSerial.available() > 0){
    // get the byte data from the GPS
    byte gpsData = gpsSerial.read();
    Serial.write(gpsData);
  }
}