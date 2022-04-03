"""
Conatins functions for converting the read voltage values from the thermistor
into temperature value in degree Celcius
"""
#Temperature reader

import math

#Steinhart constants for 1kOhm Thermistor
c1 = 1.43291542079688e-3
c2 = 2.72319937659526e-4
c3 = -4.58846025754717e-7
c4 = 1.87721342921284e-7

def V_to_T(V:float,R:float):
    """
    Function for converting Voltage into Temperature using the steinhart equation
    $$ \\frac{1}{T} = c_1+c_2ln(R)+c_3{ln(R)}^2+c_4{ln(R)}^3 $$
    where T is in Kelvin

    Args:

        V (float)   : Voltage read (between 0 and 1)
        
        R (floar)   : Resistance in series with the Thermistor
    """
    R2 =R*(1/V-1)#: Resistance of the Thermistor
    #:Steinhart equation to give temeperature read from the Thermistor 
    T =  (1/(c1+c2*math.log(R2)+c3*math.log(R2)*math.log(R2)+c4*math.log(R2)*math.log(R2)*math.log(R2)))-273.15
    return T
    
