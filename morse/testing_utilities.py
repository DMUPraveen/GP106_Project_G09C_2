
from typing import List, Literal
from random import random
import sys
from morse.Morse_Decoder import TIMINGS,MinTimes,configs,MORSE_ENCODING
import itertools


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
                ts.append(self.random_time(configs.SIGNAL_MAINTAIN_MIN_LIMIT*3,MinTimes.MEDIMUM-3*configs.SIGNAL_MAINTAIN_MIN_LIMIT))
            elif(t == TIMINGS.MEDIUM):
                ts.append(self.random_time(MinTimes.MEDIMUM+configs.SIGNAL_MAINTAIN_MIN_LIMIT*3,MinTimes.LONG-3*configs.SIGNAL_MAINTAIN_MIN_LIMIT))
            else:
                ts.append(self.random_time(MinTimes.LONG+5*configs.SIGNAL_MAINTAIN_MIN_LIMIT,configs.SIGNAL_TIMEOUT_LIMIT-3*configs.SIGNAL_MAINTAIN_MIN_LIMIT))
        ts.append(self.random_time(configs.SIGNAL_TIMEOUT_LIMIT,self.MAXTIME))
        return list(itertools.accumulate(ts,initial=self.start_time))

    def no_noise_signal_get(self,current_time:float):
        if(current_time > self.times[self.index]):
            self.signal_state = not self.signal_state
            self.index +=1
            if(self.index >= len(self.times)):
                return False

        return self.signal_state

        



                



