
from typing import List, Literal
from random import random

from Morse_Decoder import Morse_Decoder,TIMINGS,MinTimes,SIGNAL_MAINTAIN_MIN_LIMIT,SIGNAL_TIMEOUT_LIMIT
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
    MAXTIME = 100 #maximum pulse duration generated
    def __init__(self,current_time:float,start_time:float,start_state:bool = False):
        self.signal_state:bool = start_state
        self.start_time:float = start_time
        self.times:List[float] = self.generate_times([TIMINGS.SHORT,TIMINGS.MEDIUM,TIMINGS.LONG,TIMINGS.SHORT,TIMINGS.LONG,TIMINGS.SHORT,TIMINGS.LONG,TIMINGS.MEDIUM])
        self.finished = False
        self.index = 0
    @staticmethod
    def random_time(t1:float,t2:float):
        '''
        returns a random time duration between t1 and t2
        '''
        return random()*(t2-t1)+t1

    def generate_times(self,times:List[Literal[TIMINGS.LONG,TIMINGS.MEDIUM,TIMINGS.SHORT]])->List[float]:
        ts : List[float] = []
        for t in times:
            if(t == TIMINGS.SHORT):
                ts.append(self.random_time(SIGNAL_MAINTAIN_MIN_LIMIT,MinTimes.MEDIMUM-SIGNAL_MAINTAIN_MIN_LIMIT))
            elif(t == TIMINGS.MEDIUM):
                ts.append(self.random_time(MinTimes.MEDIMUM+SIGNAL_MAINTAIN_MIN_LIMIT,MinTimes.LONG-SIGNAL_MAINTAIN_MIN_LIMIT))
            else:
                ts.append(self.random_time(MinTimes.LONG+SIGNAL_MAINTAIN_MIN_LIMIT,SIGNAL_TIMEOUT_LIMIT-SIGNAL_MAINTAIN_MIN_LIMIT))
        ts.append(self.random_time(SIGNAL_TIMEOUT_LIMIT,self.MAXTIME))
        return list(itertools.accumulate(ts,initial=self.start_time))

    def no_noise_signal_get(self,current_time:float):
        if(current_time > self.times[self.index]):
            self.signal_state = not self.signal_state
            self.index +=1
            if(self.index >= len(self.times)):
                return False

        return self.signal_state

        

                




def test_function1(times:List[float]):
    '''
    Functions for testing Morse_Decoder
    >>> test_function1([0.01, 1, 0.01, 1, 0.01, 0.01, 1, 100])
    [<MORSE_ENCODING.DASH: 1>, <MORSE_ENCODING.SYMBOL_PAUSE: 2>, <MORSE_ENCODING.DASH: 1>]
    '''
    ldr = False
    timer = Debug_Timer()
    md = Morse_Decoder(print,timer.time())
    now = timer()
    index = 0
    while (index < len(times)):

        if(timer() - now >= times[index]):
            ldr = not ldr
            index += 1
            now = timer()
        timer.tick(0.01)
        md.get_signal(ldr,timer.time())

def test_function2():
    timer = Debug_Timer()

    a = Automatic_Morse(timer.time(),100)
    md = Morse_Decoder(print,timer.time())
    while True:
        if(md.get_signal(a.no_noise_signal_get(timer.time()),timer.time())):
            break
        timer.tick(0.05)



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    a = Automatic_Morse(0,100)
    print(a.times)
    test_function2()
