/* Φ-LUCA Bio-Instrument v1.0 - REAL 500Hz ECG Stream */
#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const char* ssid = "SpectrumSetup-E8";      // ← YOUR WIFI NAME
const char* password = "dampdog595";        // ← YOUR WIFI PASSWORD
const int ECG_PIN = 34;                     // AD8232 OUTPUT
const int SAMPLE_RATE_HZ = 500;             // Medical standard

WebSocketsServer webSocket = WebSocketsServer(81);
unsigned long lastSample = 0;
int ecgBuffer[100];  // 200ms ring buffer
int bufferIndex = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ECG_PIN, INPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\
Φ-LUCA ECG ONLINE: " + WiFi.localIP().toString());
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
  
  unsigned long now = micros();
  if (now - lastSample >= (1000000UL / SAMPLE_RATE_HZ)) {
    int ecgValue = analogRead(ECG_PIN);
    ecgBuffer[bufferIndex] = ecgValue;
    bufferIndex = (bufferIndex + 1) % 100;
    
    // Stream JSON every 10 samples (50Hz UI update)
    if (bufferIndex % 10 == 0) {
      DynamicJsonDocument doc(256);
      doc["ecg"] = ecgValue;
      doc["buffer"] = ecgBuffer;
      doc["timestamp"] = millis();
      String packet; 
      serializeJson(doc, packet);
      webSocket.broadcastTXT(packet);
    }
    
    lastSample = now;
  }
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  // No-op for now
}
