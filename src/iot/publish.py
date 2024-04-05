import random
import json
import time
from paho.mqtt import client as mqtt_client
import datetime

class MqttClient:
    def __init__(self, broker, port, topic, client_id):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.client = self.connect_mqtt()

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}")

        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(self.topic, 2)
        self.client.on_message = on_message

    def publish(self, payload):
        self.client.publish(self.topic, payload)

    def run(self):
        self.subscribe()
        self.client.loop_forever()

    def generate_data(self, location):
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "location": location,
        }
        return json.dumps(data)


    def send_data(self, location):
        data = self.generate_data(location)
        print(f"Sending data: {data}")
        self.publish(data)

if __name__ == '__main__':
    broker = 'broker.emqx.io'
    port = 1883
    topic = "python/dob-iot"
    client_id = f'publish-{random.randint(0, 100)}'

    mqtt_client = MqttClient(broker, port, topic, client_id)

    while True:
        mqtt_client.publish("Location")
        print(f"Published payload")
        time.sleep(5)  # Send data every 5 seconds
