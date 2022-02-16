# Importing libraries
from pyfirmata import Arduino, util
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
R1 = 1100 #fixed resistor value

#Steinhart constants for 1kOhm Thermistor
c1 = 1.43291542079688e-3
c2 = 2.72319937659526e-4
c3 = -4.58846025754717e-7
c4 = 1.87721342921284e-7


while True:
    time.sleep(0.1)
    v = (V.read())
    R2 =R1*(1/(v)-1) #Resistance of the Thermistor
    #Steinhart equation to give temeperature read from the Thermistor 
    T =  (1/(c1+c2*math.log(R2)+c3*math.log(R2)*math.log(R2)+c4*math.log(R2)*math.log(R2)*math.log(R2)))-273.15
    print(T,'celcius')

#conditioning whether to generate sound from the buzzer
    if T > 10000:
        B.write(0.2)
        board.pass_time(0.5)
        B.write(0.6)
        board.pass_time(0.5)
        B.write(0.8)
        board.pass_time(0.5)
        B.write(0)
        
        



