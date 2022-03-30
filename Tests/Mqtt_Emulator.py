'''
This script is used to inject mqtt messages and to test other componenets of the system
without having to setup the circuit every time
Used especially to test the dashboard
'''
from scipy import rand
from sympy import topological_sort
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
    temp = Random_temp_generator(25)
    
    def publish_temp():
        mqtt_handler.publish(tp.CCC.TEMPERATURE,f'{temp.get():.1f}')
        
    timed_events.add_event(1,publish_temp)

    while True:
        timed_events.run()


if __name__ == "__main__":
    main()