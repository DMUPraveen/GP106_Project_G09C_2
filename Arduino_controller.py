
from pyfirmata import Arduino,util,OUTPUT,INPUT
from morse.Morse_Decoder import Morse_Decoder,MORSE_ENCODING
from time import time
from typing import List

#This is a new comment

COM_PORT = 'COM3'

def call_back(code: str):
    s = ''
    for c in code:
        if(c == MORSE_ENCODING.DOT):
            s += '.'
        elif(c == MORSE_ENCODING.DASH):
            s += '_'
        elif(c == MORSE_ENCODING.LETTER_PAUSE):
            s += ' '
            pass
        elif(c == MORSE_ENCODING.SYMBOL_PAUSE):
            pass
        elif(c == MORSE_ENCODING.WORD_PAUSE):
            s += '       '
    print(s)





def main():
    board = Arduino(COM_PORT)
    it = util.Iterator(board)
    ldr_pin = board.get_pin('a:0:i')
    it.start()
    dec = Morse_Decoder(call_back,time())
    while True:
        
        val = ldr_pin.read()
        #buttone reads
        #thermistor reads etc.
        if(val is not None):
            print(val,dec.state)
            if(dec.get_signal(val > 0.5,time())):
                break
            









if __name__ == "__main__":
    main()


