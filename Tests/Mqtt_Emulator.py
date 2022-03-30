'''
This script is used to inject mqtt messages and to test other componenets of the system
without having to setup the circuit every time
Used especially to test the dashboard
'''

import test_config
from Utility.Event import TimedEventManager
from Network.mqtt import MQTT_Handler
from random import random
import Topics as tp
MQTT_NAME = "G9C_EM"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883

class Random_temp_generator():
    def __init__(self,initial):
        self.temp = initial
    def get(self)->float:
        self.temp += (0.5 - random())
        return self.temp
def main():
    timed_events = TimedEventManager()
    mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
    temp_CCC = Random_temp_generator(25)
    temp_PO = Random_temp_generator(35)
    temp_CDR = Random_temp_generator(60)
    
    def publish_temp():
        mqtt_handler.publish(tp.CCC.TEMPERATURE,f'{temp_CCC.get():.1f}')
        mqtt_handler.publish(tp.PO.TEMPERATURE,f'{temp_PO.get():.1f}')
        mqtt_handler.publish(tp.CDR.TEMPERATURE,f'{temp_CDR.get():.1f}')

    def print_message_and_payload(msg):
        def call_back(data):
            print(f"{msg}: {data}")
        return call_back
    timed_events.add_event(1,publish_temp)
    mqtt_handler.observe_event(tp.CCC.LOCKDOWN,print_message_and_payload('CCC'))
    mqtt_handler.observe_event(tp.PO.LOCKDOWN,print_message_and_payload('PO'))
    mqtt_handler.observe_event(tp.CDR.LOCKDOWN,print_message_and_payload('CDR'))
    while True:
        timed_events.run()


if __name__ == "__main__":
    main()