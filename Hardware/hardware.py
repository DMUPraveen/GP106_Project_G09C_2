from pyfirmata import Arduino
from . import Thermistor_Lib
from typing import Optional
from .hardware_config import *
'''
Class for handling the hardware configuration
'''

# As of now the threshold must be manually adjusted via the potentiometer
# We are working on methods to calibrate this automatically depending on the lighting condition
##############################################


class Hardware:
    '''
    Wrapper around the pyfirmata Arduino Class to ease readability of the code
    '''

    def __init__(self, com_port: str, time: float, report_delay: float):
        self.board = Arduino(com_port)
        self.ldr_pin = self.board.get_pin(LDR_PIN)
        self.red_pin = self.board.get_pin(LED_RED)
        self.gree_pin = self.board.get_pin(LED_GREEN)
        self.thermistor = self.board.get_pin(THERMISTOR_PIN)
        self.buzzer = self.board.get_pin(BUZZER_PIN)
        self.button = self.board.get_pin(BUTTON_PIN)
        self.time = time
        self.locked = True
        self.lock()

    def wait_while_input_stable(self):
        '''
        Wait while the inputs stabilize
        '''
        while True:
            for pin in [self.ldr_pin, self.thermistor]:
                if(pin.read() is None):
                    continue
            break

    def update(self, time):
        '''
        Updating the board (calling board.itierate())
        And doing the reporting if the correct time has elapsed
        '''
        self.board.iterate()

    def green_on(self):
        self.gree_pin.write(1)

    def green_off(self):
        self.gree_pin.write(0)

    def red_on(self):
        self.red_pin.write(1)

    def red_off(self):
        self.red_pin.write(0)

    def get_ldr(self) -> float:
        return self.ldr_pin.read()

    def buzzer_on(self):
        #print("hello")
        self.buzzer.write(1.0)

    def buzzer_off(self):
        self.buzzer.write(0)

    def button_pressed(self):
        return self.button.read()

    def get_temp(self) -> Optional[float]:
        try:
            return Thermistor_Lib.V_to_T(self.thermistor.read(), THERMISTOR_RESISTOR)
        except:
            return None

    def lock(self):
        self.locked = True
        self.red_on()
        self.green_off

    def unlock(self):
        self.locked = True
        self.green_on()
        self.red_off()
