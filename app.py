import json
import os
import yaml
import time
import threading
from paho.mqtt.client import Client, CallbackAPIVersion
import uuid
import utils, cab, pro, vehicle

# --- Load configuration from file ---
def load_config(path=os.getenv("CONFIG_FILE","config.yaml")):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

config = load_config()


def isCab():
    return VEHICLE_TYPE == "cab"

VEHICLE_ID = config.get("id", f"urn:ngsi-ld:vehicle:{uuid.uuid4()}")
VEHICLE_TYPE = config.get("type", "cab")
VEHICLE_INSTANCE = vehicle.Vehicle

print("Initialized as type ", VEHICLE_TYPE, " with id ", VEHICLE_ID)

if isCab(): 
    VEHICLE_INSTANCE = cab.Cab(VEHICLE_ID)
else:
    VEHICLE_INSTANCE = pro.Pro(VEHICLE_ID)


mqtt_config = config.get("mqtt", {})
MQTT_BROKER = mqtt_config.get("broker", "localhost")
MQTT_PORT = mqtt_config.get("port", 1883)
MQTT_USERNAME = mqtt_config.get("user",os.getenv("MQTT_USERNAME"))
MQTT_PASSWORD = mqtt_config.get("password",os.getenv("MQTT_PASSWORD"))
PERIODIC_INTERVAL = mqtt_config.get("periodic_interval", 5)

vehicleData = {
  "location": [1.0,1.0],
  "bearing": 1.0,
    "batteryLevel": 50.0,
    "consumption": 100.0,
    "speed":15.0,
    "chainedPosition": 0
}


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code", reason_code)
    commandTopic = VEHICLE_INSTANCE.getCommandTopic()
    print("Subscribing to command topic:", commandTopic)
    client.subscribe(commandTopic)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received payload:", payload)
        VEHICLE_INSTANCE.handleCommand(payload)

    except Exception as e:
        print("Error handling message:", e)

def periodic_publisher(client):
    while True:
        VEHICLE_INSTANCE.refreshAndSend(client)
        time.sleep(PERIODIC_INTERVAL)

client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
# Set the username and password for authentication
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message


if __name__ == "__main__":
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start background thread for periodic publishing
    thread = threading.Thread(target=periodic_publisher, args=(client,), daemon=True)
    thread.start()

    client.loop_forever()
