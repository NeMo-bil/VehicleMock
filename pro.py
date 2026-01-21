import utils
import vehicle
from paho.mqtt.client import Client
import json

class Pro(vehicle.Vehicle):

    id=""
    commandTopic=""    
    telemetryTopic=""
    lfTelemetryTopic=""
    
    proTelemetryData = {
        "timestamp": 1717414982000,
        "position_latitude": 52.520008,
        "position_longitude": 13.404954,
        "position_heading": 135.0,
        "velocity": 5.5,
        "state_of_charge": 78.2,
        "ad_status": 3,
        "ad_nemo_status": 1
    }

    proLowFrequencyTelemetryData = {
        "timestamp": 1717414982000,
        "K_TCU_H2TRail": 298,
        "MPa_TCU_H2PRail": 35,
        "K_TCU_H2TRegulator": 295,
        "MPa_TCU_H2PRegulatorIn": 34,
        "MPa_TCU_H2PRegulatorOut": 34,
        "MPa_TCU_H2PTank3": 33,
        "K_TCU_H2TGas4": 296,
        "MPa_TCU_H2PTank4": 34,
        "K_TCU_H2TGas5": 297,
        "MPa_TCU_H2PTank5": 33,
        "K_TCU_H2TGas1": 295,
        "MPa_TCU_H2PTank1": 34,
        "K_TCU_H2TGas2": 294,
        "MPa_TCU_H2PTank2": 34,
        "K_TCU_H2TGas3": 296,
        "ms2_IMU_VertAccel": 0,
        "kWh_VCU_VerbrauchKumulativ": 123,
        "kWh_VCU_LadungKumulativ": 56,
        "km_VCU_Kilometerstand": 12056,
        "Dummy_64Bit": 0,
        "pct_TCU_Tankstand": 85,
        "gs_FCU_Wasserstoffmassenstrom": 0,
        "K_TCUH2TEndplug": 292,
        "Pro_Temperature0": 29,
        "Pro_Temperature1": 29,
        "Pro_Temperature2": 29,
        "Pro_Temperature3": 29,
        "Pro_Temperature4": 29,
        "Pro_Temperature5": 29,
        "Pro_Temperature6": 29,
        "Pro_Temperature7": 29
    }

    proCommandData = {}
    
    def __init__(self,id):
        self.id=id
        self.commandTopic = "v1/nemo.pro/{vehicle_id}/command".format(vehicle_id=id)
        self.telemetryTopic = "v1/nemo.pro/{vehicle_id}/hf/telemetry".format(vehicle_id=id)
        self.lfTelemetryTopic = "v1/nemo.pro/{vehicle_id}/lf/telemetry".format(vehicle_id=id)

    def handleCommand(self, data: dict):
        self.cabCommandData = data
        print("Received new cab command data:", self.cabCommandData)
        
    def getCommandTopic(self) -> str:
        return self.commandTopic
    
    def getTelemetry(self):
        return self.proTelemetryData

    def getLowFrequencyTelemetry(self):
        return self.proLowFrequencyTelemetryData
        
    def refreshAndSend(self, client: Client):
        print("Currently nothing to simulate. Current telemetry:", self.proTelemetryData, self.proLowFrequencyTelemetryData)
        client.publish(self.telemetryTopic, json.dumps(self.proTelemetryData))
        client.publish(self.lfTelemetryTopic, json.dumps(self.proLowFrequencyTelemetryData))
       