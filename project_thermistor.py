# Importing libraries
from pyfirmata import Arduino, util
import Thermistor_Lib
import time
import math

#connecting to the arduino
board = Arduino('COM5')

#Iterator
iterator = util.Iterator(board)
iterator.start()

#Assigning variables for the connected pins
V = board.get_pin('a:0:i')
B = board.get_pin('d:9:p')
R1 = 980 #fixed resistor value

#Steinhart constants for 1kOhm Thermistor
c1 = 1.43291542079688e-3
c2 = 2.72319937659526e-4
c3 = -4.58846025754717e-7
c4 = 1.87721342921284e-7



while True:
    time.sleep(0.1)
    v = (V.read())
    print(v)
    T = Thermistor_Lib.V_to_T(v,R1)
    print(T,'celcius')

#conditioning whether to generate sound from the buzzer
    if T > 30:
        B.write(1.0)
    else:
        B.write(0)
    
        
        



