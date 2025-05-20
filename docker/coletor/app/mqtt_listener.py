import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
TOPICS = ["robot/status", "robot/uv"]

INFLUXDB_HOST = "influxdb"
INFLUXDB_PORT = 8086
INFLUXDB_DB = "uvscout"

client_db = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
client_db.switch_database(INFLUXDB_DB)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        json_body = [
            {
                "measurement": msg.topic,
                "tags": {
                    "robot_id": data.get("id", "unknown")
                },
                "fields": {k: float(v) if isinstance(v, (int, float)) else str(v) for k, v in data.items()},
                "time": data.get("timestamp")
            }
        ]
        client_db.write_points(json_body)
        print(f"Stored message from {msg.topic}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
