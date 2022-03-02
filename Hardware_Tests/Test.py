#imports
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #so that morse can be found

import time
from pyfirmata import Arduino,util
#Arduino Setup
board = Arduino('COM7')

#Define the pins
resistor_pin=board.get_pin('a:0:i')

it=util.Iterator(board)
it.start()
def resistor_1():
    resistor_Val=resistor_pin.read()
    return resistor_Val
def LED(Val):
    if Val=='false':
        board.digital[7].write(0)
    elif Val=='true':
        board.digital[7].write(1)
