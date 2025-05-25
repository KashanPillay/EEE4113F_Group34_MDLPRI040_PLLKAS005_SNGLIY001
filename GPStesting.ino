 // Define the RX and TX pins for Serial 2
#define RXD2 16
#define TXD2 17

// Create an instance of the HardwareSerial class for Serial 2
HardwareSerial gpsSerial(1);

void setup(){
  // Serial Monitor
  Serial.begin(115200);
  
  // Start Serial 2 with the defined RX and TX pins and a baud rate of 9600
  gpsSerial.begin(9600, SERIAL_8N1, RXD2, TXD2);
  Serial.println("Serial 2 started");
}

void loop(){
  while (gpsSerial.available() > 0){
    // get the byte data from the GPS
    char gpsData = gpsSerial.read();
    Serial.print(gpsData);
  }
  delay(1000);
  Serial.println("-------------------------------");
}
