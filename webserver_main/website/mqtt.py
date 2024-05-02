
import paho.mqtt.client as mqtt
from website.service.databaseService import addTemperature,addHumidity

def mqttInitializer(app):
    
    def on_message(client, userdata, message):
        data = float(message.payload.decode("utf-8"))
        if message.topic == "esp32/weather/temperature":
            with app.app_context():
                addTemperature(data)
        elif message.topic == "esp32/weather/humidity":
            with app.app_context():
                addHumidity(data)
        print(type(data), message)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe("esp32/weather/temperature")
            client.subscribe("esp32/weather/humidity")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client("esp32")
    client.on_message = on_message
    client.on_connect = on_connect
    print("Connecting to MQTT broker")
    client.connect("<insert IP address>", port=1883)
    print("Connected Successfully")
    client.loop_start()