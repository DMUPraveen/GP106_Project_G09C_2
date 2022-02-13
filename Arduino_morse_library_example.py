
from pyfirmata import Arduino,util,OUTPUT,INPUT
from morse.Morse_Decoder import Morse_Decoder,MORSE_ENCODING
from time import time
from typing import List

#This is a new comment

COM_PORT = 'COM3'





def main():
    dec = Morse_Decoder(print,time())
    board = Arduino(COM_PORT)
    ldr_pin = board.get_pin('a:0:i')
    
    while(ldr_pin.read() is None):
        board.iterate()
        pass
    print("Ready")
    pre_val = ldr_pin.read()
    while True:
        
        val = ldr_pin.read()
        #buttone reads
        #thermistor reads etc.
        if(val is not None):
            #print(val,dec.state)
            if(dec.get_signal(val > 0.5,time())):
                break #if uncommented breaks when a valid message has been translated
                print("Finsihed decoding ready for next")
            

        board.iterate()







if __name__ == "__main__":
    main()


