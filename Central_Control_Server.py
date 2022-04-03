
from Network.mqtt import MQTT_Handler
from Serverlogin_utilities import validate_user,print_welcome_message
import Topics as tp
from pass_lib.pass_check import Password_Manager
from Utility.Event import Event_Manager
from time import sleep
from teams_password_checkers import CDR_sequence_checker,CCC_pass_checker,PO_knock_checker
from typing import Callable
import sys
import json

MQTT_NAME = "G9C_CCS"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883
PASSWORD_FILE = "Passwords.json"
SECURITY_BREACH_EVENT = "SECURITY_BREACH"


class Central_Control_Server:
    
    def __init__(self):
        self.pas_man = Password_Manager.password_manager_from_file(PASSWORD_FILE)
        print_welcome_message()
        if(not validate_user(self.pas_man)):
            sys.exit()
        self.mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
        self.event_manager = Event_Manager()

        #Intializing password checkers
        self.cdr_sequence_checker = CDR_sequence_checker()
        self.ccc_pass_checker = CCC_pass_checker(self.pas_man,self.event_manager.publish_event(SECURITY_BREACH_EVENT))
        self.po_knock_checker = PO_knock_checker()
        ########################################
        
        self.initialize_event_manager()
        self.initialize_mqtt_handler()
    

    def initialize_event_manager(self):
        '''
        Intializers the even manager system
        '''
        self.event_manager.on_event(SECURITY_BREACH_EVENT,lambda : print("Security Breach"))
    
    def send_to_mqtt_decorator(self,topic:str,function:Callable[[str],str])->Callable[[str],None]:
        '''
        This is a utility function that takes in a function that takes in a
        string and returns a new function that instead of returning the said string
        publishes to the mqtt_server under the topic topic 

        This is used to convert password checker functions provided by other teams
        which take in a str as the pass code and returns the correct access code (denied,accepted etc),
        into functions that does the same but publishes the result instead

        topic: The topic to which the returning function will publish to
        function: function to be decorated
        '''
        def publishing_function(payload):
            print(payload)
            self.mqtt_handler.publish(topic,function(payload))
        
        return publishing_function

    def initialize_mqtt_handler(self):
        '''
        Intializes the mqtt handler

        Mainly used to define what should happen on recieving messages under a given topic
        '''
        self.mqtt_handler.observe_event(
            tp.CCC.MORSE_SEND,
            self.send_to_mqtt_decorator(tp.CCC.MORSE_ACCESS,self.ccc_pass_checker.check)
        )
        self.mqtt_handler.observe_event(
            tp.CDR.SEQ_SEND,
            self.send_to_mqtt_decorator(tp.CDR.SEQ_ACCESS,self.cdr_sequence_checker.check)
            )
        self.mqtt_handler.observe_event(
            tp.PO.KNOCK_SEND,
            self.send_to_mqtt_decorator(tp.PO.KNOCK_ACCESS,self.po_knock_checker.check)
            )
    def loop(self):
        while True:
            sleep(0.1)

if __name__ == "__main__":
    CCS_system = Central_Control_Server()
    CCS_system.loop()