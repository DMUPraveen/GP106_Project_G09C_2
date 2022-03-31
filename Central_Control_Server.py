
from Network.mqtt import MQTT_Handler
from Serverlogin_utilities import validate_user,print_welcome_message
import Topics as tp
from pass_lib.pass_check import Password_Manager
from Utility.Event import Event_Manager
from time import sleep

MQTT_NAME = "G9C_CCS"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883

MORSE_CODE_USER = "MORSE_CODE"

SECURITY_BREACH_EVENT = "SECURITY_BREACH"
passwords = {
    "Pentagon":b'(\x10\xad\xed\xa7\xc1\xf9\xc9\x1d\xe35e\xb0\xf5\xf8l',
    MORSE_CODE_USER:b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'

}


class Central_Control_Server:
    
    def __init__(self):
        self.pas_man = Password_Manager(passwords)
        print_welcome_message()
        if(not validate_user(self.pas_man)):
            return
        self.mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
        self.event_manager = Event_Manager()

        self.initialize_event_manager()
        self.initialize_mqtt_handler()
    
    def validate_and_send_morse(self,morse_message:str):
        exists,valid = self.pas_man.check_password_hash(MORSE_CODE_USER,morse_message)
        if(not exists):
            self.event_manager.publish_event(SECURITY_BREACH_EVENT)
            return
        if(valid):
            self.mqtt_handler.publish(tp.CCC.MORSE_ACCESS,tp.CCC.ACESS_GRANTED)
        else:
            self.mqtt_handler.publish(tp.CCC.MORSE_ACCESS,tp.CCC.ACESS_DENIED)
    
    def initialize_event_manager(self):
        self.event_manager.on_event(SECURITY_BREACH_EVENT,lambda : print("Security Breach"))
    
    def initialize_mqtt_handler(self):
        self.mqtt_handler.observe_event(tp.CCC.MORSE_SEND,self.validate_and_send_morse)

    def loop(self):
        while True:
            sleep(0.1)

if __name__ == "__main__":
    CCS_system = Central_Control_Server()
    CCS_system.loop()