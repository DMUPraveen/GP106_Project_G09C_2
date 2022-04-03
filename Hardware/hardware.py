"""
This module contains the class for handling the hardware configuration and functions related to comunicating with
the hardware and etc.
"""

from pyfirmata import Arduino
from . import Thermistor_Lib
from typing import Optional
from .hardware_config import *

# As of now the threshold must be manually adjusted via the potentiometer
# We are working on methods to calibrate this automatically depending on the lighting condition
##############################################


class Hardware:
    '''
    Wrapper around the pyfirmata Arduino Class to ease readability of the code
    '''

    def __init__(self, com_port: str):
        '''
        Args:

            com_port (str) : The comport which the arduino is connected to
            
            The systme is locked on startup
        '''
        self.board = Arduino(com_port)
        self.ldr_pin = self.board.get_pin(LDR_PIN)
        self.red_pin = self.board.get_pin(LED_RED)
        self.gree_pin = self.board.get_pin(LED_GREEN)
        self.thermistor = self.board.get_pin(THERMISTOR_PIN)
        self.buzzer = self.board.get_pin(BUZZER_PIN)
        self.button = self.board.get_pin(BUTTON_PIN)
        self.locked = True
        self.lock()

    def wait_while_input_stable(self):
        '''
        In most cases the input from the arduino is not stable for a while
        This function when called waits in a blocking loop until it is
        '''
        while True:
            for pin in [self.ldr_pin, self.thermistor]:
                if(pin.read() is None):
                    continue
            break

    def update(self):
        '''
        Updating the board (calling board.itierate())
        '''
        self.board.iterate()

    def green_on(self):
        '''
        Turns the green led on
        '''
        self.gree_pin.write(1)

    def green_off(self):
        '''
        Turns the green led off
        '''
        self.gree_pin.write(0)

    def red_on(self):
        '''
        Turns the red led on
        '''
        self.red_pin.write(1)

    def red_off(self):
        '''
        Turns the red led off
        '''
        self.red_pin.write(0)

    def get_ldr(self) -> float:
        '''
        Reads the ldr value and returns a float between 0 and 1
        '''
        return self.ldr_pin.read()

    def buzzer_on(self):
        '''
        Turns the connected buzzer on
        '''
        self.buzzer.write(1.0)

    def buzzer_off(self):
        '''
        Turns the buzzer off
        '''
        self.buzzer.write(0)

    def button_pressed(self)->bool:
        '''
        Returns true if the button is pressed
        else it returns falls
        '''
        return self.button.read()

    def get_temp(self) -> Optional[float]:
        '''
        Returns the temperature in Celcius (may return None if the input is not stable)
        '''
        try:
            return Thermistor_Lib.V_to_T(self.thermistor.read(), THERMISTOR_RESISTOR)
        except:
            return None

    def lock(self):
        '''
        Sets the system into lockdown mode
        '''
        self.locked = True
        self.red_on()
        self.green_off()

    def unlock(self):
        '''
        Sets the system into unlock mode
        '''
        self.locked = True
        self.green_on()
        self.red_off()
