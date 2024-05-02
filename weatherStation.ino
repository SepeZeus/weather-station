#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>
//#include <LinkedList.h>

// int next;
// LinkedList<float> *temps = new LinkedList<float>();


#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

//WiFi credentials
const char* ssid = "";
const char* password = "";

WiFiClient espClient;

//set MQTT
PubSubClient client(espClient);

const char *mqtt_server = ""; //ip address
const char *mqtt_username = "";
const char *mqtt_password = "";

//Prinout message sent to MQTT
/*void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}
*/

//Prinout weatherdata
/*void weatherPrints(float h, float t, float m){ //h = humidity, t= temperature, m = mean temperature

  Serial.print(F("Humidity (%): "));
  Serial.print(h);
  Serial.print(F(" Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(F("Mean Temperature: "));
  Serial.print(m);
  Serial.print(F("°C "));

}
*/

//Get mean temperature
/*
float meanTemperature(LinkedList<float>* temps){
    float mean = 0.00;
    while(temps->get(next)){
      mean += temps->get(next);
      next += 1;
  }
  float meanTemp = mean/temps->size();
  return meanTemp;
}
*/


//Connect to MQTT server and WiFi
void mqtt_and_wifi_setup(){
  //connect to WiFi
  Serial.print("Connecting to WiFi");
  // Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  //Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //setup MQTT
  client.setServer(mqtt_server, 1883);
  //client.setCallback(mqttCallback);
}

//reconnect MQTT server if connection is lost, is also used to initialize the connection
void reconnect() {
  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (client.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
      client.subscribe("esp32/weather/temperature");
      client.subscribe("esp32/weather/humidity");

    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Trying again in 5 seconds");
      delay(5000);
    }
  }
}

//forward message to MQTT server
void sendToMqtt(float temp, float humid){
  char dataStr[6]; //take up to three decimal precision (ex. 27.158), values above xx.xxx aren't expected nor needed
  if(temp){
    dtostrf(temp,1,3, dataStr);//change temp (a float) to a string type and fit it into the allotted 6 bytes 
    client.publish("esp32/weather/temperature", dataStr);
  }
  if(humid){
    dtostrf(humid,1,3, dataStr);//change humidity (a float) to a string type and fit it into the allotted 6 bytes
    client.publish("esp32/weather/humidity", dataStr);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT11 test!"));
  dht.begin();

  //next = 0;

  mqtt_and_wifi_setup();
  reconnect();
}

void loop() {
  if(!client.connected()){
    reconnect();
  }
  client.loop();
  // Wait 5 seconds between readings
  delay(5000);
  // Reading temperature or humidity takes about 250 milliseconds!
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  sendToMqtt(t, h); 

  // temps->add(t);
  // float m = meanTemperature(temps);
  // weatherPrints(h, t, m);
  //next = 0;
}




