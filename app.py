import json
import yaml
import time
import threading
from paho.mqtt.client import Client, CallbackAPIVersion
import uuid

# --- Load configuration from file ---
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

config = load_config()

VEHICLE_ID = config.get("id", f"urn:ngsi-ld:vehicle:{uuid.uuid4()}")

mqtt_config = config.get("mqtt", {})
MQTT_BROKER = mqtt_config.get("broker", "localhost")
MQTT_PORT = mqtt_config.get("port", 1883)
MQTT_USERNAME = mqtt_config.get("user")
MQTT_PASSWORD = mqtt_config.get("password")
PERIODIC_INTERVAL = mqtt_config.get("periodic_interval", 5)

topics = mqtt_config.get("topics", {})
INPUT_TOPIC = topics.get("commands", "v1/vehicle/{vehicle_id}/command").format(vehicle_id=VEHICLE_ID)
OUTPUT_TOPIC = topics.get("telemetry", "v1/vehicle/{vehicle_id}/telemetry").format(vehicle_id=VEHICLE_ID)

vehicleData = {
  "location": [1.0,1.0],
  "bearing": 1.0,
    "batteryLevel": 50.0,
    "consumption": 100.0,
    "speed":15.0,
    "chainedPosition": 0
}

def calculate_new_position(current: float, target: float) -> float:
    difference = target - current
    step = difference * 0.1
    if abs(step) < 0.01:
        step = min(0.01, difference) if difference > 0 else max(-0.01, difference)
    return current + step

def is_valid_next_stop_location(payload):
    value = payload.get("nextStopLocation")

    # Must be a list of exactly 2 elements
    if not isinstance(value, list) or len(value) != 2:
        return False

    # Each element must be a float (or int, optionally)
    return all(isinstance(x, (float, int)) for x in value)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code", reason_code)
    client.subscribe(INPUT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received payload:", payload)

        if is_valid_next_stop_location(payload):
            vehicleData["location"][0] = calculate_new_position(vehicleData["location"][0],payload["nextStopLocation"][0])
            vehicleData["location"][1] = calculate_new_position(vehicleData["location"][1],payload["nextStopLocation"][1])
            print("New vehicle data:", vehicleData)
        else:
            print("Missformed payload:", payload)

    except Exception as e:
        print("Error handling message:", e)

def periodic_publisher(client):
    while True:
        client.publish(OUTPUT_TOPIC, json.dumps(vehicleData))
        print(f"[Periodic] Published telemetry to {OUTPUT_TOPIC}: {vehicleData}")
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
