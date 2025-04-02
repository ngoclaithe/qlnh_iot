#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include <DHT.h>

#define WIFI_SSID "tang2"
#define WIFI_PASSWORD "12345678"
#define API_KEY "AIzaSyCrFVyK4Ekpfi_PXHOuBQ2bxNwYUUeeWOw"
#define USER_EMAIL "newli5737@gmail.com"
#define USER_PASSWORD "12345678"
#define DATABASE_URL "https://giamsatkholanh-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define DATABASE_SECRET "DATABASE_SECRET"
#define DHTPIN D4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
unsigned long dataMillis = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(300); }
  Serial.println(WiFi.localIP());
  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;
  config.token_status_callback = tokenStatusCallback;
  Firebase.reconnectNetwork(true);
  fbdo.setBSSLBufferSize(4096, 1024);
  fbdo.setResponseSize(4096);
  Firebase.begin(&config, &auth);
  dht.begin();
}

void loop() {
  if (millis() - dataMillis > 5000 && Firebase.ready()) {
    dataMillis = millis();
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Lỗi đọc DHT!");
      return;
    }
    if (Firebase.setFloat(fbdo, "/nhietdo", temperature))
      Serial.printf("Nhiệt độ: %s\n", String(temperature).c_str());
    else
      Serial.printf("Lỗi nhiệt độ: %s\n", fbdo.errorReason().c_str());
    if (Firebase.setFloat(fbdo, "/doam", humidity))
      Serial.printf("Độ ẩm: %s\n", String(humidity).c_str());
    else
      Serial.printf("Lỗi độ ẩm: %s\n", fbdo.errorReason().c_str());
  }
}
