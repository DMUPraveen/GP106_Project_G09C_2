#Temperature reader

import math

#Steinhart constants for 1kOhm Thermistor
c1 = 1.43291542079688e-3
c2 = 2.72319937659526e-4
c3 = -4.58846025754717e-7
c4 = 1.87721342921284e-7

def V_to_T(V,R):
    R2 =R*(1/V-1) #Resistance of the Thermistor
    #Steinhart equation to give temeperature read from the Thermistor 
    T =  (1/(c1+c2*math.log(R2)+c3*math.log(R2)*math.log(R2)+c4*math.log(R2)*math.log(R2)*math.log(R2)))-273.15
    return T
    
