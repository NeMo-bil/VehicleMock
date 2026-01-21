import utils
import vehicle
from paho.mqtt.client import Client
import json


class Cab(vehicle.Vehicle):
    
    id=""
    commandTopic=""    
    telemetryTopic=""
    

    cabTelemetryData = {
        "position_latitude": 52.520008,
        "position_longitude": 13.404954,
        "position_heading": 90.0,
        "velocity": 45.6,
        "state_of_charge": 76.3,
        "ad_status": 3,
        "ad_nemo_status": 1
        }

    cabCommandData = {}
    
    def __init__(self,id):
        self.id=id
        self.commandTopic = "v1/nemo.cab/{vehicle_id}/command".format(vehicle_id=id)
        self.telemetryTopic = "v1/nemo.cab/{vehicle_id}/telemetry".format(vehicle_id=id)

    def handleCommand(self, data: dict):
        self.cabCommandData = data
        print("Received new cab command data:", self.cabCommandData)

    def getCommandTopic(self) -> str:
        return self.commandTopic
        
    def getTelemetry(self):
        return self.cabTelemetryData
        
    def refreshAndSend(self, client: Client):
        if self.is_valid_next_stop_location(self.cabCommandData):
            self.cabTelemetryData["position_latitude"] = utils.calculate_new_position(self.cabTelemetryData["position_latitude"],self.cabCommandData["ad_pickup_dropoff_position_latitude"])
            self.cabTelemetryData["position_longitude"] = utils.calculate_new_position(self.cabTelemetryData["position_longitude"],self.cabCommandData["ad_pickup_dropoff_position_longitude"])
            print("New vehicle data:", self.cabTelemetryData)
        else:
            print("Currently no valid target location. Current commandData:", self.cabCommandData, "Current telemetry:", self.cabTelemetryData)
        client.publish(self.telemetryTopic, json.dumps(self.cabTelemetryData))
                
                
    def is_valid_next_stop_location(self, payload):
        value = [payload.get("ad_pickup_dropoff_position_longitude"),payload.get("ad_pickup_dropoff_position_latitude")]

        # Must be a list of exactly 2 elements
        if not isinstance(value, list) or len(value) != 2:
            return False

        # Each element must be a float (or int, optionally)
        return all(isinstance(x, (float, int)) for x in value)