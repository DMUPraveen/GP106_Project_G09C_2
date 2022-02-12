try:
    from pyfirmata import Arduino,util
except:
    import pip
    pip.main(['install','pyfirmata','paho-mqtt'])
    from pyfirmata import Arduino,util

#imports
import time
import pyfirmata

#Arduino Setup
board = Arduino('COM7')

#Define the pins
resistor_pin=board.get_pin('a:0:i')

it=pyfirmata.util.Iterator(board)
it.start()
def resistor_1():
    resistor_Val=resistor_pin.read()
    return resistor_Val
def LED(Val):
    if Val=='false':
        board.digital[7].write(0)
    elif Val=='true':
        board.digital[7].write(1)
