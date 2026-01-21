from paho.mqtt.client import Client

class Vehicle:
    def handleCommand(self, data: dict):
        pass

    def refreshAndSend(self, client: Client):
        pass
    
    def getCommandTopic(self) -> str:
        return "changeMeTopic"
