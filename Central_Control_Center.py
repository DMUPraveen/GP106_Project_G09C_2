

from morse.Morse_Decoder import Morse_Decoder
from Network.mqtt import MQTT_Handler
from Hardware.hardware import Hardware
import time
from Utility.Event import Event_Manager, TimedEventManager
from Utility.Resource import Multi_Or_Switch
import Topics as tp



CENTRAL_CONTROL_SERVER_NAME = "CCS"

############### Server Config  ###############
MQTT_NAME = "G9C_CCC"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883



COM_PORT = "COM4"
MAX_TEMP = 36
LDR_THRESHOLD = 0.5
####################################################
TEMP_REPORT_DELAY = 1  # The temperature is sent to the server every second so as not to
# overload traffic



class System:
    def __init__(self,name,server_port,server_address,com_port):
        self.mqtt_handler = MQTT_Handler(name,server_address, server_port)
        self.hardware = Hardware(com_port,time.time())
        self.timed_events = TimedEventManager()
        self.event_manager = Event_Manager()
        self.buzzer_switch = Multi_Or_Switch(
                self.hardware.buzzer_on,
                self.hardware.buzzer_off
        )
        self.fire_alarm = self.buzzer_switch.get_handle()
        self.network_alarm = self.buzzer_switch.get_handle()




        self.initialize_mqtt_handler()
        self.initialize_mqtt_handler()

    def initialize_mqtt_handler(self):
        ############ MQTT Call Backs ###################
        def parse_acess_message(data):
            if(data == tp.CCC.ACESS_GRANTED):
                print("Acess granted")
                self.hardware.unlock()
            else:
                print("Acess denied")
                self.hardware.lock()
        def raise_alarm(data):
            self.network_alarm.request_on()
        ###############################################
       
        self.mqtt_handler.observe_event(tp.CCC.MORSE_ACCESS, parse_acess_message)
        self.mqtt_handler.observe_event(tp.CCC.RAISE_ALARM, raise_alarm)

    def intialize_event_managers(self):
        ############ Event Call Backs ###################
        def publish_temperature_data():
            self.mqtt_handler.publish(
                tp.CCC.TEMPERATURE, 
                f'{self.hardware.get_temp():.1f}')
                #print("publishsing")
        ###############################################
        self.timed_events.add_event(TEMP_REPORT_DELAY,publish_temperature_data)

    def initialize_hardware(self):
        def morse_call_back(code: str):
            print(code)
            self.mqtt_handler.publish(tp.CCC.MORSE_SEND, code)
        self.morse_decoder = Morse_Decoder(morse_call_back,time.time())
        self.hardware.wait_while_input_stable()
        print("Hardware Up and Running")

        
def main():
    # Instantiating main objects that handle hardware,network,resources and events
    mqtt_handler = MQTT_Handler(MQTT_NAME, MQTT_SERVER, MQTT_PORT)
    hardware = Hardware(COM_PORT, time.time())
    timed_events = TimedEventManager()
    event_manager = Event_Manager()
    buzzer_switch = Multi_Or_Switch(
        hardware.buzzer_on,
        hardware.buzzer_off
    )
    
    fire_alarm = buzzer_switch.get_handle()
    network_alarm =  buzzer_switch.get_handle()
    ############## Defining Call backs used by various porcesses in the code #####################
    def morse_call_back(code: str):
        print(code)
        mqtt_handler.publish(tp.CCC.MORSE_SEND, code)

    def parse_acess_message(data):
        if(data == tp.CCC.ACESS_GRANTED):
            print("Acess granted")
            hardware.unlock()
        else:
            print("Acess denied")
            hardware.lock()
    def raise_alarm(data):
        network_alarm.request_on()

    def publish_temperature_data():
        mqtt_handler.publish(tp.CCC.TEMPERATURE, f'{hardware.get_temp():.1f}')
        #print("publishsing")
    ############### Managing Events###############
    #Mqtt event
    mqtt_handler.observe_event(tp.CCC.MORSE_ACCESS, parse_acess_message)
    mqtt_handler.observe_event(tp.CCC.RAISE_ALARM, raise_alarm)

    #other events
    timed_events.add_event(TEMP_REPORT_DELAY,publish_temperature_data)
    #################################################################################################
    
    md = Morse_Decoder(morse_call_back, time.time())
    hardware.wait_while_input_stable()
    print("Systme up and running")
    hardware.unlock()
    while True:
        # hardware.buzzer_on()
        temp = hardware.get_temp()
        timed_events.run()
        #################################Checking for the temperature value###################
        if(temp is None):
            pass
        elif(temp > MAX_TEMP):
            fire_alarm.request_on()
        else:
            fire_alarm.request_off()
        ######################################################################################

        if(hardware.button_pressed()):
            #print("pressed")  # If the lock button is pressed lock the system
            hardware.lock()
        ldr = hardware.get_ldr()
        if(ldr is None):
            pass
        else:
            # Capturing signal from morse code
            md.get_signal(ldr > LDR_THRESHOLD, time.time())
            # print(md.state)
        # updating the hardware important functions are called in this function
        hardware.update(time.time())
        # Functions that need to be run every loop


if __name__ == "__main__":
    main()
