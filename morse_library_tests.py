
from typing import List, Literal
from random import random
from morse.MorseCode_translator import convertToMorse
import sys
from morse.Morse_Decoder import Morse_Decoder,TIMINGS,MinTimes,SIGNAL_MAINTAIN_MIN_LIMIT,SIGNAL_TIMEOUT_LIMIT,MORSE_ENCODING
import itertools


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# def convert_to_morse(message:str)->str:
#     return convertToMorse(message).replace('343','4')


class Debug_Timer:
    def __init__(self):
        self.t:float = 0

    def __call__(self):
        return self.time()
    def time(self)->float:
        return self.t

    def tick(self, delta:float):
        self.t += delta




class Automatic_Morse:
    '''
    Simulates an arduino signal 
    does not support empty strings
    '''
    MAXTIME = 100 #maximum pulse duration generated
    def __init__(self,current_time:float,start_time:float,message_encoding:List[MORSE_ENCODING],start_state:bool = False):
        self.signal_state:bool = start_state
        self.start_time:float = start_time
        self.times:List[float] = self.generate_times(self.encoding_to_time(message_encoding))
        self.finished = False
        self.index = 0
    @staticmethod
    def random_time(t1:float,t2:float):
        '''
        returns a random time duration between t1 and t2
        '''
        return random()*(t2-t1)+t1

    def encoding_to_time(self,message:List[MORSE_ENCODING]):
        times = []
        for encoding in message:
            if(encoding == MORSE_ENCODING.DOT or encoding == MORSE_ENCODING.SYMBOL_PAUSE):
                times.append(TIMINGS.SHORT)
            elif(encoding == MORSE_ENCODING.DASH or encoding == MORSE_ENCODING.LETTER_PAUSE):
                times.append(TIMINGS.MEDIUM)
            else:
                times.append(TIMINGS.LONG)
        return times


    def generate_times(self,times:List[Literal[TIMINGS.LONG,TIMINGS.MEDIUM,TIMINGS.SHORT]])->List[float]:
        ts : List[float] = []
        for t in times:
            if(t == TIMINGS.SHORT):
                ts.append(self.random_time(SIGNAL_MAINTAIN_MIN_LIMIT*3,MinTimes.MEDIMUM-3*SIGNAL_MAINTAIN_MIN_LIMIT))
            elif(t == TIMINGS.MEDIUM):
                ts.append(self.random_time(MinTimes.MEDIMUM+SIGNAL_MAINTAIN_MIN_LIMIT*3,MinTimes.LONG-3*SIGNAL_MAINTAIN_MIN_LIMIT))
            else:
                ts.append(self.random_time(MinTimes.LONG+5*SIGNAL_MAINTAIN_MIN_LIMIT,SIGNAL_TIMEOUT_LIMIT-3*SIGNAL_MAINTAIN_MIN_LIMIT))
        ts.append(self.random_time(SIGNAL_TIMEOUT_LIMIT,self.MAXTIME))
        return list(itertools.accumulate(ts,initial=self.start_time))

    def no_noise_signal_get(self,current_time:float):
        if(current_time > self.times[self.index]):
            self.signal_state = not self.signal_state
            self.index +=1
            if(self.index >= len(self.times)):
                return False

        return self.signal_state

        

                






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
