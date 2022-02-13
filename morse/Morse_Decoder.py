

from typing import Callable, List
from .MorseCode_translator import convertToWords
import enum


class MORSE_ENCODING(enum.Enum):
    '''
    Encoding scheme used in the processing of morse codes(internally in the library)
    '''
    DOT = 0             # Represents a '.'
    DASH = 1            # Represents a '_'
    SYMBOL_PAUSE = 2    # Represents the pause between '.' or '_'
    # Represents the pause between letters (e.g. betwee P and Y)
    LETTER_PAUSE = 3
    WORD_PAUSE = 4      # Represents the pause between words


class TIMINGS(enum.Enum):
    '''
    Different time periods used in the morse code

    SHORT -> dots and inter symbol spaces (1 time units)
    MEDIUM -> dashes and inter letter spaces (3 time units)
    LONG -> inter word spaces (7 time units)

    Reference : https://morsecode.world/international/timing.html
    '''
    SHORT = 0
    MEDIUM = 1
    LONG = 2


class MinTimes:
    '''
    Used in determining whether a pulse is SHORT MEDIUM LONG
    handles differently for high pulses and low pulses
    '''
    SHORT = 0       # for DOT, SYMBOL_PAUSE
    MEDIMUM = 2     # for DASH,LETTER_PAUSE
    LONG = 5        # for WORD_PAUSE


class STATES(enum.Enum):
    '''
    States the morse decoder class can be in
    '''
    IDLE = 0        # not recording
    RECORDING = 1   # recording the time of a active signal
    PENDING = 2     # a possible signal change has been deteted awaiting to see if it is noise or a legitimate signal
    BLOCKED = 3     # blocks the decoder from decoding the decoder doesn't accept new incoming signals

TIME_UNIT = 1                   # time a dot a takes (or a letter pause)
SIGNAL_MAINTAIN_MIN_LIMIT = 0.1 # time a signal has to maintained for it to be considered a valid change of state
SIGNAL_TIMEOUT_LIMIT = 10       # maximum time the signal can be kept at a some state without changing before the deocder decides the signal has ended
MAX_WORD_COUNT = 100            # The maximum number of dots and dashes a message can have (not implemented as of yet)

def convert_to_english(encoding:str)->str:
    return convertToWords(encoding.replace('4','343'))


class Morse_Decoder:
    '''
    Morse_Decoder class is used to decode the morse code recieved via the input signal
    The class operates as a state machine.
    Method get_signal(signal_state:bool,current_time)
    
    When this is executed depending on previous states that is stored in the class it will determine what the morse signal is doing.
    When decoder detects that the morse signal is over it will decode it and call the callback function provided upon construction with
    the decoded morse signal passed as an argument.

    Since morse code is time dependant (length of the pulses change its meaning) a timer is required for the operation of the class
    in order to calculate the duration of individual (low or high) signals. The timer can be provided in the contructor.

    Note:   there are no checks to see whether the current time is greater than all previously provided times or whether the elapsed time is correct
            providing time that is less than previouly provided times will have undocumented behaviout
            it is responisbility of the caller to ensure the provided time is correct (you can use time.time from the time library for example)
             
    '''
    def __init__(
        self,
        call_back: Callable[[str], None],
        current_time: float 
        ):
        '''
        call_back -> function to be called when a morse code has been decoded
        time -> time the decoder starts at (time of creation all times are )
        '''
        ##to be called when a Morse code is captured 

        self.last_signal_state: bool = False                # the state of the signal when get_signal was called previously
        self.state: STATES = STATES.IDLE                    # the state of the deocder used for deciding on the routine to be taken when a signal change is detected
        self.call_back: Callable[[str], None] = call_back   # call back function to be called when the morse code is decoded to plain text of format (decode_plaintext_message:str)->None
        self.last_time: float = current_time                # the time at which the signal whose duration is current being mointored, started
        self.pending_start: float = current_time            # When there is a change in the signal the time of change is intially stored here if the signal is legtimate it is moved to last_time
        self.state_before_pending: STATES = STATES.IDLE     # state of decoder
        self.duratons: List[float] = []                     # the durations of the pulses recieved
        # Not necessary to store whether they are high or low since the starting pulse is always high and high low pulses occur alternatively

    def start_pending_state(self, now:float) -> None:
        #print("start pending")
        '''
        utility function to,
        starts the pending state -- when a state change happens
        now -> time point the change occured
        '''
        self.state_before_pending = self.state
        self.state = STATES.PENDING
        self.pending_start = now

    def reject_pending_state(self) -> None:
        #print("reject pending")
        '''
        utility function to,
        reject the state change as noise
        '''
        assert(self.state == STATES.PENDING)

        self.state = self.state_before_pending

    def block(self)->None:
        self.state = STATES.BLOCKED

    def if_blocked_unblock_and_reset(self,current_time:float)->None:
        if(self.state == STATES.BLOCKED):
            self.state = STATES.IDLE                      
            self.last_time = current_time                
            self.pending_start = current_time           
            self.state_before_pending = STATES.IDLE     
            self.duratons.clear()    


    def accept_pending_state(self, new_state: STATES) -> None:
        #print(new_state)
        '''
        new_state -> the new_state of the decoder to be set could be recording or idle (current has to pending)
        Utility function for accepting the change of state of the ldr as not noise and legitimate
        this function handles all the logic required for this process such as,
            change of state -- setting self.state =  new_state 
            changing the last_time to the beginning of the new signal
            if there was a signal previous being recoreded save its duration in self.duratons
        '''
        assert (self.state == STATES.PENDING)

        tim = self.pending_start - self.last_time
        self.last_time = self.pending_start
        self.state = new_state
        if(self.state_before_pending == STATES.IDLE): #this is the first signal
            return
        else:
            self.duratons.append(tim)

    def get_signal(self, new_signal_state: bool,current_time: float)->bool:
        '''
        Must be called within the event loop.
        If a coherent morse code was recieved it will forward the data for conversion
        and to be finally sent without blocking the main event loop
        '''
        # record the time of recieving new data
        # no state change
        if(self.state == STATES.BLOCKED):
            pass
        elif(new_signal_state == self.last_signal_state):
            # the state hasn't changed for an adequate amount of time -> accept the change of state as valid
            if(self.state == STATES.PENDING and current_time - self.pending_start > SIGNAL_MAINTAIN_MIN_LIMIT):
                self.accept_pending_state(STATES.RECORDING)

            # end of message revert to IDLE and process the message
            elif(self.state == STATES.RECORDING and current_time - self.last_time > SIGNAL_TIMEOUT_LIMIT):
                self.state = STATES.IDLE
                if(self.last_signal_state):#ending with a dash (that is too long but what ever ...) dash should be added
                    self.duratons.append(current_time-self.last_time)
                else:#ending with long low signal correct ending of a message the signal need not be added
                    pass
                self.process_code(self.duratons)
                self.duratons.clear()
                return True # no issue in returning since the

        # state change
        else:
            if(self.state == STATES.IDLE):
                # off after unusually proloned on signal, this is ignored considerd as return to normal idle state
                if(self.last_signal_state):
                    pass
                else:  # signal is on after prologned off signal, possible start of a signal
                    self.start_pending_state(current_time)
            elif(self.state == STATES.PENDING):
                # the change that happened previously was just noise return to state before pending state
                self.reject_pending_state()

            elif(self.state == STATES.RECORDING):
                # the change happened may be the start of a new legitimate change in signal or noise change state to pending
                self.start_pending_state(current_time)

        # set the last_ldr state the current value of it
        self.last_signal_state = new_signal_state
        return False


    def process_code(self, timing_data: List[float]) -> None:
        '''
        Called when a morse code has been captured by get_signal
        '''
        #print(timing_data)
        encoding = self.convert_timing_to_code(timing_data)
        #print(encoding)
        encoded_string = "".join(str(code.value) for code in encoding)
        try:
            message = convert_to_english(encoded_string)
        except KeyError:
            message = ''
        self.call_back(message)

        

    def convert_timing_to_code(self, timing_data: List[float]) -> List[MORSE_ENCODING]:
        '''
        utililty function for converting a list of timing information into a format detailed in MORSE_ENCODING enum
        to represent the morse code information
        '''
        encoding_list: List[MORSE_ENCODING] = []
        # Intial signal is high by default ( a dot or a dash), False is LOW(a pause letter word or symbol)
        signal = True
        for time in timing_data:
            timing = self.time_to_timeunit(time)
            if(signal):  # a dot or a dash
                if(timing == TIMINGS.SHORT):
                    encoding_list.append(MORSE_ENCODING.DOT)
                else:  # if it is medium or long pause (a design decision)
                    encoding_list.append(MORSE_ENCODING.DASH)
            else:  # a pause
                if(timing == TIMINGS.SHORT):
                    encoding_list.append(MORSE_ENCODING.SYMBOL_PAUSE)
                elif(timing == TIMINGS.MEDIUM):
                    encoding_list.append(MORSE_ENCODING.LETTER_PAUSE)
                elif(timing == TIMINGS.LONG):
                    encoding_list.append(MORSE_ENCODING.WORD_PAUSE)
            signal = not signal
        return encoding_list

    @staticmethod
    def time_to_timeunit(time: float) -> TIMINGS:
        '''
        utility funtion for converting a single time duration to the corresponding timeunit
        this function handles the natural variability of the signal and determines the most appropriate number
        of time units for a given time duration
        '''
        t = time/TIME_UNIT
        if(t > MinTimes.LONG):
            return TIMINGS.LONG  # 7 second
        elif(t > MinTimes.MEDIMUM):
            return TIMINGS.MEDIUM  # 3 seconds
        else:
            return TIMINGS.SHORT  # 1 second
