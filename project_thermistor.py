# Importing libraries
from pyfirmata import Arduino, util
import time
import math

#connecting to the arduino
board = Arduino('COM5')

#Iterator
iterator = util.Iterator(board)
iterator.start()

#Assigning variables for the conncted pins
V = board.get_pin('a:1:i')
B = board.get_pin('d:9:p')
R1 = 1100 #fixed resistor value

while True:
    time.sleep(0.1)
    v = (V.read())*1023
    R2 =R1*(1023/(v)-1) #Resistance of the thermistor
    #Steinhart equation to give temeperature read from the thermistor 
    T =  (1/(c1+c2*math.log(R2*10)+c3*math.log(R2*10)*math.log(R2*10)*math.log(R2*10)))-273
    print(T,'celcius')

#conditioning whether to generate sound from the buzzer
    if T > 30:
        B.write(0.2)
        board.pass_time(0.5)
        B.write(0.6)
        board.pass_time(0.5)
        B.write(0.8)
        board.pass_time(0.5)
        B.write(0)
        
        



