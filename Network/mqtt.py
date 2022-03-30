'''
wrappers around the paho mqtt library
'''

import paho.mqtt.client as mqtt
from typing import Dict,List,Callable

class MQTT_Handler(mqtt.Client):
    def __init__(self,id:str,server:str,port:int):
        super().__init__(id)
        try:
            super().connect(server,port)
        except:
            print("server error")
            exit()
        self.events:Dict[str,List[Callable[[str],None]]] = {}
        self.loop_start()

    def observe_event(self,topic:str,func:Callable[[str],None]):
        print(topic)
        if(topic not in self.events):
            self.subscribe(topic)
            self.events[topic] = []
        self.events[topic].append(func)

    def on_connect(self,client,userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self,client,userdata,msg):
        topic = msg.topic
        message = str(msg.payload.decode("utf-8"))
        print(topic,message)
        if(topic in self.events):
            for func in self.events[topic]:
                func(message)
    def on_disconnect(self, userdata, flags, rc):
        print("Disconnected with result code "+str(rc))
    
