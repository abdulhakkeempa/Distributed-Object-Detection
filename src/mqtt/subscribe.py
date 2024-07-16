# python 3.11

import random
import json
from paho.mqtt import client as mqtt_client
import sqlite3

DB_FILE = "db/database.db"
broker = 'broker.emqx.io'
port = 1883
topic = "python/dob-iot"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)

            # Connect to the SQLite database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Create the table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mqtt_data (
                    timestamp DATETIME,
                    location TEXT
                )
            """)

            # Insert data into the table
            cursor.execute("""
                INSERT INTO mqtt_data (timestamp, location)
                VALUES (?, ?)
            """, (data["timestamp"], data["location"]))

            conn.commit()
            conn.close()
            print(f"Data stored in SQLite: {data}")

        except Exception as e:
            print(f"Error storing data: {e}")

    client.subscribe(topic, 2)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()


