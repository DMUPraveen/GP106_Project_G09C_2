'''
Conatains configurations for the hardware setup
These include the pins different compenets are connected to
Values of resistors etc.

The pins are given in the following format
pin = {X}:{Y}:{Z}

X = a,d where a= analog,d=digital

Y = pin number

Z = i,o where i= input, o=output
'''


LDR_PIN = "a:1:i"
LED_RED = "d:10:o"
LED_GREEN = "d:11:o"
BUZZER_PIN = "d:9:p"
THERMISTOR_PIN = "a:0:i"
BUTTON_PIN = 'd:12:i'
THERMISTOR_RESISTOR = 1000 #: resistor in series with the thermistor