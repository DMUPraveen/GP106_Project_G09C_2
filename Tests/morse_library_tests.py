import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #so that morse can be found

from morse.Morse_Decoder import Morse_Decoder
from morse.MorseCode_translator import convertToMorse
from morse.testing_utilities import Debug_Timer,Automatic_Morse,MORSE_ENCODING





# def convert_to_morse(message:str)->str:
#     return convertToMorse(message).replace('343','4')





def test_function(message:str):
    '''
    When using this test function please note that only simple letter are supported
    multiple spaces between words will lead to an error since this simulates a real ldr signal 
    to consecutive off signals does not make sence

    So use,

    lower case words (all supported character are in mores_lib.py)
    do not use more than one space between words

    do not use sentences beginning with a space it must begin with a character (as in morse code the beginning of the message
    is always a dot or a dash)


    >>> test_function('hello world')
    hello world
    >>> test_function('h')
    h
    >>> test_function('university of peradeniya')
    university of peradeniya

    >>> test_function('0123456')
    0123456

    >>> test_function('.')
    .
    >>> test_function('bye bye')
    bye bye
    >>> test_function('1+2=3')
    1+2=3
    >>> test_function('lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
    lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    '''

    timer = Debug_Timer()
    morse = convertToMorse(message)
    #print(morse)
    encoding = [MORSE_ENCODING(int(i)) for i in morse]
    #print(encoding)
    a = Automatic_Morse(timer.time(),100,encoding)
    md = Morse_Decoder(print,timer.time())
    while True:
        if(md.get_signal(a.no_noise_signal_get(timer.time()),timer.time())):
            break
        timer.tick(0.05)

def test_function_with_noise(message:str):
    '''
    When using this test function please note that only simple letter are supported
    multiple spaces between words will lead to an error since this simulates a real ldr signal 
    to consecutive off signals does not make sence

    So use,

    lower case words (all supported character are in mores_lib.py)
    do not use more than one space between words

    do not use sentences beginning with a space it must begin with a character (as in morse code the beginning of the message
    is always a dot or a dash)


    >>> test_function_with_noise('hello world')
    hello world
    >>> test_function_with_noise('h')
    h
    >>> test_function_with_noise('university of peradeniya')
    university of peradeniya

    >>> test_function_with_noise('0123456')
    0123456

    >>> test_function_with_noise('.')
    .
    >>> test_function_with_noise('bye bye')
    bye bye
    >>> test_function_with_noise('1+2=3')
    1+2=3
    >>> test_function_with_noise('lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
    lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    '''

    timer = Debug_Timer()
    morse = convertToMorse(message)
    #print(morse)
    encoding = [MORSE_ENCODING(int(i)) for i in morse]
    #print(encoding)
    a = Automatic_Morse(timer.time(),100,encoding)
    md = Morse_Decoder(print,timer.time())
    while True:
        if(md.get_signal(a.no_noise_signal_get(timer.time()),timer.time())):
            break
        timer.tick(0.05)



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
