#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "";
const char* password ="";
const char* serverUrl = "http://192.168.1.235:8000/api/get_data/";

const int tempraturepin=15;
float temperature;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  pinMode(tempraturepin,INPUT);

  while(WiFi.status() !=WL_CONNECTED){
    delay(500);
    Serial.println(".");
  }
  Serial.println("\nPolaczono z WIFI");

}

void loop() {

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

  int sensorValue = analogRead(tempraturepin);
  float voltage = sensorValue *(3.3 / 4095.0);
  temperature = voltage * 100.0;

    StaticJsonDocument<200> doc;
    doc["device_name"] = "ESP32_Sensor";
    doc["temperature"] = temperature;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    if (httpResponseCode > 0) {
          String response = http.getString();
          Serial.print("Odpowiedź serwera: ");
          Serial.print(httpResponseCode);
          Serial.println(response);
          
        } else {
          Serial.printf("Błąd POST: %s\n", http.errorToString(httpResponseCode).c_str());
        }

        http.end();
      }
      delay(20000);

}


