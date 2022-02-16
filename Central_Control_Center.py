import json
from pydoc import cli
import paho.mqtt.client as mqtt
from pyfirmata import Arduino
from morse.Morse_Decoder import Morse_Decoder
from typing import Dict,Callable,List, Optional
import Thermistor_Lib
import time
GROUP_NAME = "G9C"
UNIT_NAME = "CCC"
CENTRAL_CONTROL_SERVER_NAME = "CCS"
################ Arduino Config ##############
LDR_PIN = "a:1:i"
LED_RED = "d:10:o"
LED_GREEN = "d:11:o"
BUZZER_PIN ="d:9:p"
THERMISTOR_PIN ="a:0:i"
THERMISTOR_RESISTOR = 1000
COM_PORT = "COM4"
MAX_TEMP = 30
##############################################


############### Server Config  ###############
MQTT_NAME = "G9C_CCC"
MQTT_SERVER = "vpn.ce.pdn.ac.lk" 
MQTT_PORT = 8883
def topic_wrapper(topic):
    ret =  f"{GROUP_NAME}/{UNIT_NAME}/{topic}"
    print(ret)
    return ret
def topic_server_wraps(topic):
    ret = f"{GROUP_NAME}/{CENTRAL_CONTROL_SERVER_NAME}/{topic}"
    print(ret)
    return ret
THERMISTOR_TOPIC = topic_wrapper("Temperature")
SYS_ERR = topic_wrapper("SYS_ERR")
MORSE_SEND = topic_wrapper("MOs Code")
MORSE_GET_GRANTED = topic_server_wraps("MOs Code/Granted")
MORSE_GET_DENIED = topic_server_wraps("MOs Code/Denied")
ALARM = topic_server_wraps("Alarm")
##############################################



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
        print("Connected with result code "+str(rc))
    


class Hardware:
    def __init__(self,com_port:str,time:float,report_delay:float,mqtt_handler:MQTT_Handler):
        self.board = Arduino(com_port)
        self.ldr_pin = self.board.get_pin(LDR_PIN)
        self.red_pin = self.board.get_pin(LED_RED)
        self.gree_pin = self.board.get_pin(LED_GREEN)
        self.thermistor = self.board.get_pin(THERMISTOR_PIN)
        self.buzzer = self.board.get_pin(BUZZER_PIN)
        self.time = time
        self.report_delay = report_delay
        self.mqtt_handler:MQTT_Handler = mqtt_handler
    def wait_while_input_stable(self):
        while True:
            for pin in [self.ldr_pin,self.thermistor]:
                if(pin.read() is None):
                    continue
            break
    def update(self,time):
        self.board.iterate()
        if((time - self.time) > self.report_delay):
            self.time = time
            self.report()
    def green_on(self):
        self.gree_pin.write(1)
    def green_off(self):
        self.gree_pin.write(0)
    def red_on(self):
        self.red_pin.write(1)
    def red_off(self):
        self.red_pin.write(0)
    def get_ldr(self)->float:
        return self.ldr_pin.read()
    def buzzer_on(self):
        print("hello")
        self.buzzer.write(1.0)
    def buzzer_off(self):
        self.buzzer.write(0) 
    def get_temp(self)->Optional[float]:
        try:
            return Thermistor_Lib.V_to_T(self.thermistor.read(),THERMISTOR_RESISTOR)
        except:
            return None
    def report(self):
        temp = self.get_temp()
        #print("reporting")
        if(temp is not None):
            self.mqtt_handler.publish(THERMISTOR_TOPIC,temp)
        else:
            self.mqtt_handler.publish(SYS_ERR)



def main():
    mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
    hardware = Hardware(COM_PORT,time.time(),1,mqtt_handler)
    hardware.wait_while_input_stable()
    print("done")
    def call_back(code:str):
        print(code)
        mqtt_handler.publish(MORSE_SEND,code)
    def access_granted(data):
        print("Acess granted")
    def access_denied(data):
        print("Acess denied")
    
    mqtt_handler.observe_event(MORSE_GET_GRANTED,access_granted)
    mqtt_handler.observe_event(MORSE_GET_DENIED,access_denied)
    mqtt_handler.observe_event(ALARM,lambda temp : hardware.buzzer_on())
    md = Morse_Decoder(call_back,time.time())
    while True:
        #hardware.buzzer_on()
        temp = hardware.get_temp()
        #print(temp)
        if(temp is None):
            pass
        elif(temp > MAX_TEMP):
            hardware.buzzer_on()
        else:
            hardware.buzzer_off()
        ldr = hardware.get_ldr()
        if(ldr is None):
            pass
        else:
            md.get_signal(ldr>0.3,time.time())
            #print(md.state)
        hardware.update(time.time())


        

if __name__ == "__main__":
    main()


    