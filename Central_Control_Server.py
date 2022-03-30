from Central_Control_Center import CENTRAL_CONTROL_SERVER_NAME
from Network.mqtt import MQTT_Handler

MQTT_NAME = "G9C_CCS"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883

GROUP_NAME = "G9C"
PO_TOPIC = "PO"
CCS_TOPIC = "CCS"
CCC_TOPIC = "CCC"



def main():
    mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
