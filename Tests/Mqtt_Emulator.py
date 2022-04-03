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
from time import sleep
from typing import List
MQTT_NAME = "G9C_EM"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883

class Random_temp_generator():
    """
    Used to create changing temperature values for testing pruposes
    """
    def __init__(self,initial):
        self.temp = initial
    def get(self)->float:
        self.temp += (0.5 - random())
        return self.temp


class Random_morse_acess():
    """
    Used to send morse codes to the server for testing
    """
    def __init__(self,true_password:str,false_password:str):
        self.true_password = true_password
        self.false_password = false_password
        self.state = True
    def __call__(self)->str:
        p_state = self.state
        self.state = not(self.state)
        if(p_state):
            return self.true_password

        return self.false_password


class Random_CDR_acess():
    """
    Used to send CDR sequences for testing purposes
    """
    def __init__(self,passwords:List[List[int]]):
        self.passwords = passwords
        self.counter = 0
    def __call__(self)->str:
        ret = self.passwords[self.counter]
        self.counter  = (self.counter+1)%len(self.passwords)
        print(ret)
        return str(ret)

class Random_PO_acess():
    """
    Used to send CDR sequences for testing purposes
    """
    def __init__(self,passwords,tolerance):
        self.passwords = passwords
        self.counter = 0
        self.tolerance = tolerance
    def __call__(self)->str:
        print(self.counter,end=": ")
        try:
            ret = [i+(0.5-random())*self.tolerance for i in self.passwords[self.counter]]
            self.counter  = (self.counter+1)%len(self.passwords)
            print(ret)
            return str(ret)
        except Exception:
            self.counter  = (self.counter+1)%len(self.passwords)
            print(self.passwords[self.counter])
            return str(self.passwords[self.counter])

def main():
    timed_events = TimedEventManager()
    mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
    temp_CCC = Random_temp_generator(25)
    temp_PO = Random_temp_generator(35)
    temp_CDR = Random_temp_generator(60)
    random_morse = Random_morse_acess('hello','goodbye')

    cdr_acess = Random_CDR_acess(
        [
        [1, 1, 0, 2],
        [5,6,7,8,9,4,2],
        [],
        [4,3,2,1,5],
        [1, 1, 2, 2],
        [1, 2, 1, 2]
        ]
    )
    
    po_acess = Random_PO_acess(
        [
        [0.16655588150024414, 0.13585114479064941, 0.3684210777282715, 0.11480975151062012, 0.1613321304321289, 0.4034092426300049, 0.40139293670654297, 0.38600611686706543],
        [4,5,6,7],
        [0.2,0.1,0.7,0.1,0,0],
        [5,6,100,2],
        [1,2,3,4,5,6,7,8],
        'billy bob'
        ],
        0.2
    )

    def publish_temp():
        mqtt_handler.publish(tp.CCC.TEMPERATURE,f'{temp_CCC.get():.1f}')
        mqtt_handler.publish(tp.PO.TEMPERATURE,f'{temp_PO.get():.1f}')
        mqtt_handler.publish(tp.CDR.TEMPERATURE,f'{temp_CDR.get():.1f}')

    def print_message_and_payload(msg):
        def call_back(data):
            print(f"{msg}: {data}")
        return call_back

    timed_events.add_event(1,publish_temp)
    timed_events.add_event(2,lambda : mqtt_handler.publish(tp.CCC.MORSE_SEND,random_morse()))
    timed_events.add_event(3,lambda : mqtt_handler.publish(tp.CDR.SEQ_SEND,cdr_acess()))
    timed_events.add_event(1,lambda : mqtt_handler.publish(tp.PO.KNOCK_SEND,po_acess()))

    mqtt_handler.observe_event(tp.CCC.LOCKDOWN,print_message_and_payload('CCC'))
    mqtt_handler.observe_event(tp.PO.LOCKDOWN,print_message_and_payload('PO'))
    mqtt_handler.observe_event(tp.CDR.LOCKDOWN,print_message_and_payload('CDR'))

    #mqtt_handler.observe_event(tp.CCC.MORSE_ACCESS,print_message_and_payload('CCC'))
    #mqtt_handler.observe_event(tp.CDR.SEQ_ACCESS,print_message_and_payload('CDR'))
    mqtt_handler.observe_event(tp.PO.KNOCK_ACCESS,print_message_and_payload('PO'))
    while True:
        timed_events.run()
        sleep(0.1)


if __name__ == "__main__":
    main()