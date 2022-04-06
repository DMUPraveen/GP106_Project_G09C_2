

from tkinter.tix import MAX
from morse.Morse_Decoder import Morse_Decoder
from Network.mqtt import MQTT_Handler
from Hardware.hardware import Hardware
import time
from Utility.Event import Event_Manager, TimedEventManager
from Utility.Resource import Multi_Or_Switch
import logging
import Topics as tp


CENTRAL_CONTROL_SERVER_NAME = "CCS"

############### Server Config  ###############
MQTT_NAME = "G9C_CCC"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883


COM_PORT = "COM4"
MAX_TEMP = 36
LDR_THRESHOLD = 0.3
####################################################
TEMP_REPORT_DELAY = 1  # The temperature is sent to the server every second so as not to
# overload traffic


############System Specific Events#########
FIRE = "FIRE"
NOFIRE = "NOFIRE"
LOCK = "LOCK"
UNLOCK = "UNLOCK"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
class System:
    def __init__(self, name:str, server_port:int, server_address:str, com_port:str):
        """
        Args:

            name (str)              : mqtt client name

            server_port (int)       : mqtt server port

            server_adress (str)     : mqtt broker adress
            
            com_port (str)          : arduino comport
        """
        
        
        self.mqtt_handler = MQTT_Handler(name, server_address, server_port)
        self.hardware = Hardware(com_port)
        self.timed_events = TimedEventManager()
        self.event_manager = Event_Manager()
        self.buzzer_switch = Multi_Or_Switch(
            self.hardware.buzzer_on,
            self.hardware.buzzer_off
        )
        self.fire_alarm = self.buzzer_switch.get_handle()
        self.network_alarm = self.buzzer_switch.get_handle()

        self.security = True  # Indicates whether the system is secure and running
        self.locked = True  # Indicates whether the systme is locked or not

        self.initialize_mqtt_handler()
        self.initialize_hardware()
        self.intialize_event_managers()

        self.system_lock()
        self.mqtt_handler.publish(tp.CCC.STATUS,tp.CCC.SECURE)

    def initialize_mqtt_handler(self):
        '''
        Intializing the mqtt handler
        '''
        ############ MQTT Call Backs ###################
        def parse_acess_message(data):
            if(data == tp.CCC.ACESS_GRANTED):
                print("Acess granted")
                self.system_unlock()
            else:
                print("Acess denied")
                self.system_lock()

        def raise_alarm(data):
            self.network_alarm.request_on()
        
        def system_lockdown(data):
            print(data)
            self.system_lock()
            self.network_alarm.request_on()
        ###############################################

        self.mqtt_handler.observe_event(tp.CCC.MORSE_ACCESS, parse_acess_message)
        self.mqtt_handler.observe_event(tp.CCC.RAISE_ALARM, raise_alarm)
        self.mqtt_handler.observe_event(tp.CCC.LOCKDOWN,system_lockdown)

    def intialize_event_managers(self):
        """
        Initializing the event manager
        """
        ############ Event Call Backs ###################
        def publish_temperature_data():
            self.mqtt_handler.publish(
                tp.CCC.TEMPERATURE,
                f'{self.hardware.get_temp():.1f}')
            # print("publishsing")
        ###############################################

        # Timed events
        self.timed_events.add_event(
            TEMP_REPORT_DELAY, publish_temperature_data)

        # Event Managers
        self.event_manager.on_event(FIRE, self.fire_alarm.request_on)
        self.event_manager.on_event(LOCK, self.system_lock)
        self.event_manager.on_event(NOFIRE,self.fire_alarm.request_off)

    def initialize_hardware(self):
        '''
        Intializing the hardware (also wating while input is stable)
        '''
        def morse_call_back(code: str):
            print(code)
            self.mqtt_handler.publish(tp.CCC.MORSE_SEND, code)
        self.morse_decoder = Morse_Decoder(morse_call_back, time.time())
        self.hardware.wait_while_input_stable()
        print("Hardware Up and Running")

    def system_lock(self):
        '''
        Lock the system
        '''
        if(self.locked):
            return

        self.locked = True
        self.hardware.lock()
        self.mqtt_handler.publish(tp.CCC.STATUS, tp.CCC.LOCKED)

    def system_unlock(self):
        '''
        Unlock the system
        '''
        if(not self.locked):
            return

        self.locked = False
        self.hardware.unlock()
        self.mqtt_handler.publish(tp.CCC.STATUS, tp.CCC.UNLOCKED)

    def is_fire(self, temp):
        '''
        Check if the temperature is too high
        '''
        return (temp is not None and temp > MAX_TEMP)

    def main_loop(self):
        '''
        The main loop of the Central Control Center
        '''
        while True:
            self.timed_events.run()
            temp = self.hardware.get_temp()
            if(self.is_fire(temp)):
                logger.debug("Fire")
                self.event_manager.publish_event(FIRE)
            else:
                self.event_manager.publish_event(NOFIRE)
            ldr = self.hardware.get_ldr()
            if(ldr is not None):
                #print(ldr,LDR_THRESHOLD)
                self.morse_decoder.get_signal(ldr > LDR_THRESHOLD, time.time())

            if(self.hardware.button_pressed()):
                self.system_unlock()
                self.buzzer_switch.master_off()
            self.hardware.update()



if __name__ == "__main__":
    system = System(MQTT_NAME,MQTT_PORT,MQTT_SERVER,COM_PORT)
    system.main_loop()
