
#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <Wire.h>

const char* mqtt_server="192.168.0.163";

WiFiClient espClient;
PubSubClient mqtt_client(mqtt_server, 1883, espClient);

int piezo = A0;
int mq2 = A5;
int mq2Digi = 17;
int sensorVal = 0;
int sensorVal_gas = 0;
int mq2State = 0;

const char* ssid = "Paniemleda";
const char* password =  "pass123$";
 
const uint16_t port = 10000;
const char * host = "192.168.0.163";

void setup()
{
  Serial.begin(115200);
//  Serial.begin(9600);
  pinMode(piezo, INPUT);
  pinMode(mq2, INPUT);
  pinMode(mq2Digi, INPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
  
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

}


void reconnect() {
  // Loop until we're reconnected
  while (!mqtt_client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqtt_client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      mqtt_client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqtt_client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  sensorVal = analogRead(piezo);
  Serial.print("Piezo sensor Value: ");
  Serial.println(sensorVal);

  char sensorValString[8];
  dtostrf(sensorVal, 1, 2, sensorValString);
  String message = "Piezo_Data : "+String(sensorVal, DEC);
  sendToServer(message);

  char sensorVal_gasString[8];
  sensorVal_gas = analogRead(mq2);
  dtostrf(sensorVal_gas, 1, 2, sensorVal_gasString);
  Serial.print("Smoke Sensor Value: ");
  Serial.println(sensorVal_gas);
  
  String message_gas = "MQ2_Data : "+String(sensorVal_gas, DEC);
  sendToServer(message_gas);

  if (!mqtt_client.connected()) {
    reconnect();
  }
  mqtt_client.loop();

  mqtt_client.publish("sensors/health/piezo", sensorValString);
  mqtt_client.publish("sensors/health/gas", sensorVal_gasString);
  
  delay(500);
//  mq2State = digitalRead(mq2Digi);
//  Serial.print("Smoke Sensor state: ");
//  Serial.println(mq2State);
//  message = message +" MQ2_Data: "+sensorVal;
//  delay(1000);
}


void sendToServer(String message){
  WiFiClient client;
 
  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(500);
    return;
  }
 
  Serial.println("Connected to server successful!");
 
//  client.printf("Hello Python Server I am ESP32 !!!");
  client.print(message);
  while (client.connected() && !client.available());
  while (client.available()) {
    Serial.write(client.read());
  }
    Serial.println("Disconnecting...");
    client.stop();
}
