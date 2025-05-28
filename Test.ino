const int adcPin = 34;       // ADC pin (e.g., A0 on Arduino)
const float baseline = 1.19;  // Adjust based on your low-state voltage
const int samplesPerPeriod = 4;  // 4 samples per 10ms period (2.5ms each)
float prevValue = 0;
float currentMax = 0;
int peakCount = 0;
bool isRising = false;
int pulseRate=0;

void setup() {
  Serial.begin(9600);
  analogReadResolution(12);  // For 10-bit ADC (adjust if needed)

  
  float adcValue = analogRead(adcPin) * (3.3 / 4095.0);  // Convert to voltage (adjust if needed)
  for (int i =0; i<4000; i++){
    // Detect if signal is rising or falling
  if (adcValue > prevValue) {
    isRising = true;
  } 
  else if (adcValue < prevValue && isRising) {
    // A peak occurs when the signal was rising and now starts falling
    if (adcValue > baseline) {  // Only count if above baseline
      peakCount++;
      Serial.print("Peak detected! Value: ");
      Serial.println(adcValue);
      Serial.print("Total peaks: ");
      Serial.println(peakCount);
    }
    isRising = false;
  }
  
  prevValue = adcValue;
  delayMicroseconds(2500);  // Sample every 2.5ms (adjust if needed)
  
  }
  
}

void loop() {
}