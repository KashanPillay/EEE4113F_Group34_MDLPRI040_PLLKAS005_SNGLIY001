//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 02_Send_Data_to_Google_Sheets
//----------------------------------------Including the libraries.
#include "WiFi.h"
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks
#include <HTTPClient.h>
#include "driver/ledc.h"
#include "types.h"
#include "TinyGPSPlus.h";
#include "HardwareSerial.h";

//----------------------------------------

// Defining LED PINs on the ESP32 Board.
#define On_Board_LED_PIN  2

//----------------------------------------SSID and PASSWORD of your WiFi network.
#define EAP_ANONYMOUS_IDENTITY "anonymous@uct.ac.za"
#define EAP_IDENTITY           "mdlpri040@wf.uct.ac.za"
#define EAP_PASSWORD           "Purplepineapple222003#"
#define EAP_USERNAME           "mdlpri040@wf.uct.ac.za"


//Uncomment for UCT WIFI and uncomment wifi.begin line BELOW 
const char* ssid = "eduroam";  //--> Your wifi name

//Uncomment for Kashan's Hotspot and uncomment Wifi.begin line with JUST ssid and password below. 
//const char* ssid = "Kashan's Samsung Galaxy";  //--> Your wifi name
//const char* password = "Priyalovescomsciquiz!"; //--> Your wifi password

//Uncomment for Priya's home wifi. If changing remember to switch wifi.begin line below
//const char* ssid = "TP-Link_B36E";  //--> Your wifi name
//const char* password = "12092122"; //--> Your wifi password

//----------------------------------------

// Google script Web_App_URL.
String Web_App_URL = "https://script.google.com/macros/s/AKfycbxKihxFumZTc68hDsiEUVm9dKvPEHj3SLJumiKThYdCwp3dBhs4Vu1rgJsc4blbUL5-uA/exec";


float ratio1 = 0; 
float ratio2 = 0; 
String lat = "TEST1";
String lng = "TEST2";
float ave = 0;
float Calibration=0; // Variable to store the ADC values for calibration
float value=0;
float pulse=0;


float avgHighValues;         // Stores average of highest 100 values
float avgLowValues;          // Stores average of lowest 100 values

//Array for ADC Sampling 
const int numSamples = 2000;  // Number of samples to store
float adcReadings[numSamples]; // Array to store the ADC values

//TinyGPS SetUp
TinyGPSPlus gps;
HardwareSerial SerialGPS(1);
//________________________________________________________________________________VOID SETUP()
void selectionSort(float arr[], int n) {
  for (int i = 0; i < n-1; i++) {
    // Find the minimum element in unsorted array
    int min_idx = i;
    for (int j = i+1; j < n; j++) {
      if (arr[j] < arr[min_idx]) {
        min_idx = j;
      }
    }
    
    // Swap the found minimum element with the first element in float array
    float temp = arr[min_idx];
    arr[min_idx] = arr[i];
    arr[i] = temp;
  }
}

void calculateAverages() {
  float sumLow = 0;
  float sumHigh = 0;
  
  // Calculate average of first 100 values (lowest)
  for (int i = 0; i < numSamples-1000; i++) {
    sumLow += adcReadings[i];
  }
  avgLowValues = sumLow / 1000.0;  // Using 100.0 for float division
  
  // Calculate average of last 100 values (highest)
  for (int i = numSamples - 1000; i < numSamples; i++) {
    sumHigh += adcReadings[i];
  }
  avgHighValues = sumHigh / 1000.0;
}



void setup() {
  //Setting up the sampling pins: 
  bool ledcSetClockSource(ledc_clk_cfg_t source);
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, 16, 17); //Serial port of GPS module

  Serial.println();
  delay(1000);

  pinMode(On_Board_LED_PIN, OUTPUT);

  //----------------------------------------Set Wifi to STA mode
  Serial.println("WIFI mode : STA");
  WiFi.mode(WIFI_STA);
  //---------------------------------------- 

  //----------------------------------------Connect to Wi-Fi (STA).
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //WiFi.begin(ssid, password);

  WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_IDENTITY, EAP_USERNAME, EAP_PASSWORD); // without CERTIFICATE, RADIUS server EXCEPTION "for old devices" required

  //:::::::::::::::::: The process of connecting ESP32 with WiFi Hotspot / WiFi Router.
  // The process timeout of connecting ESP32 with WiFi Hotspot / WiFi Router is 20 seconds.
  // If within 20 seconds the ESP32 has not been successfully connected to WiFi, the ESP32 will restart.
  // I made this condition because on my ESP32, there are times when it seems like it can't connect to WiFi, so it needs to be restarted to be able to connect to WiFi.

  int connecting_process_timed_out = 20; //--> 20 = 20 seconds.
  connecting_process_timed_out = connecting_process_timed_out * 2;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    digitalWrite(On_Board_LED_PIN, HIGH);
    delay(250);
    digitalWrite(On_Board_LED_PIN, LOW);
    delay(250);
    if (connecting_process_timed_out > 0) connecting_process_timed_out--;
    if (connecting_process_timed_out == 0) {
      delay(1000);
      ESP.restart();
    }
  }

  digitalWrite(On_Board_LED_PIN, LOW);
  
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("------------");
  //::::::::::::::::::
  //----------------------------------------

  delay(2000);
}
//________________________________________________________________________________

//________________________________________________________________________________VOID LOOP()
void loop() {

  Calibration = 0;

  ledcAttach(18, 100, 10); //Sets up PWM signal
  ledcAttach(19, 100, 10);
  ledcWrite(18,512);
  ledcWrite(19,512);
  ledcOutputInvert(18,true); //Inverts second PWM signal so the pulse are HIGH at alternate intervals 

  delay(1000); //Slight delay to ensure PWM signals are set 

  //Sample from ADC and calculate average values:
  for (int i = 0; i < numSamples; i++) {
    adcReadings[i] = (float)analogRead(34)/ 4095.0 * 3.3;
    delayMicroseconds(2500); // Small delay between samples if needed
  }

  selectionSort(adcReadings, numSamples);
  calculateAverages();
  ratio1 = avgLowValues;
  ratio2 = avgHighValues;


  //Calibration function:
  ledcDetach(18);
  ledcDetach(19);

  pinMode(18, OUTPUT);
  pinMode(19, OUTPUT);

  digitalWrite(18, LOW);
  digitalWrite(19, LOW);

  for (int i =0; i<50;i++){
    value = (float)analogRead(34)/ 4095.0 * 3.3;
    Calibration += value;
    delayMicroseconds(2500); // Small delay between samples if needed
  }

  ave = Calibration/200;
  

  //GPS MODULE get lat and long 
  while (SerialGPS.available() >0) {
    gps.encode(SerialGPS.read());
  }

  lat = gps.location.lat();
  lng = gps.location.lng();


//removed functions being called

  //----------------------------------------Conditions that are executed when WiFi is connected.
  // This condition is the condition for sending or writing data to Google Sheets.
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(On_Board_LED_PIN, HIGH);

    String Send_Data_URL = Web_App_URL + "?sts=write" + "&ratio1=" + String(ratio1) + "&ratio2=" + String(ratio2) + "&ave=" + String(ave) +"&pulse=" + String(pulse);

     if ((lat != "0.00") &&(lng != "0.00")) {
      Send_Data_URL = Web_App_URL + "?sts=write" + "&ratio1=" + String(ratio1) + "&ratio2=" + String(ratio2)+ "&lat=" + String(lat)+ "&long=" + String(lng) + "&ave=" + String(ave)+ "&pulse=" + String(pulse);   
    } 


    // Create a URL for sending or writing data to Google Sheets.
    //String Send_Data_URL = Web_App_URL + "?sts=write" + "&ratio1=" + String(ratio1) + "&ratio2=" + String(ratio2)+ "&lat=" + String(lat)+ "&long=" + String(lng);
    //Send_Data_URL += "&ratio=" + String(ratio);
    //Send_Data_URL += "&ratio2=" + String(ratio2);
   

    Serial.println();
    Serial.print("Sending data to URL : ");
    Serial.println(Send_Data_URL);

    //::::::::::::::::::The process of sending or writing data to Google Sheets.
      // Initialize HTTPClient as "http".
      HTTPClient http;
  
      // HTTP GET Request.
      http.begin(Send_Data_URL.c_str());
      http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
  
      // Gets the HTTP status code.
      int httpCode = http.GET(); 
  
      // Getting response from google sheets.
      String payload;
      if (httpCode > 0) {
        payload = http.getString();
        Serial.println("Payload : " + payload);    
      }
            
      http.end();
    //::::::::::::::::::
    
    digitalWrite(On_Board_LED_PIN, LOW);
    Serial.println("-------------");
  }
  //----------------------------------------  
  delay(5000);
}
//________________________________________________________________________________
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<