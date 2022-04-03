'''
Conatins functions for processing and validating passwords from many sub teams
'''
from pass_lib.pass_check import Password_Manager
import Topics as tp
from typing import Callable,Optional
import json



class CCC_pass_checker:
    '''
    Code for validating the password from CCC (Morse Code)
    '''
    MORSE_CODE_USER = "MORSE_CODE"
    def __init__(self,
                pass_man:Password_Manager,
                on_fail:Optional[Callable[[],None]]=None,
                on_password_err:Optional[Callable[[],None]]=None,
        ):
        '''
        Used to handle checking passcodes sent from the CCC.
        Args:

            pass_man        : password manager containing the passwords
            
            on_password_err : This function will be called when there is an invalid password
                                Default is None. If None nothing will be done
            
            on_fail         : This function will be called when there is some other error such
                                as a missing user etc.
        '''
        self.on_fail:Callable[[],None] = lambda : None
        self.on_password_err:Callable[[],None] = lambda : None
        self.pass_man = pass_man
        if(on_password_err is not None):
            self.on_password_err = on_password_err
        if(on_fail is not None):
            self.on_fail = on_fail
        
    def check(self,password:str)->str:
        '''
        Checks the password decoded by the CCC (morse code from flash to plaintext)
        and sends the appropriate response if so
        
        Args:

            password (str) : the password to be checked
        '''
        exists,valid = self.pass_man.check_password_hash(self.MORSE_CODE_USER,password)
        if(not exists):
            self.on_fail()
            return tp.CCC.ACESS_DENIED
        if(valid):
            return tp.CCC.ACESS_GRANTED
        else:
            self.on_password_err()
            return tp.CCC.ACESS_DENIED




class CDR_sequence_checker:
    '''
    Code for validating the sequences sent by the CDR (Provided by team A)
    '''
    TOP_SECRECT = "TOP_SECRET"
    SECRET = "SECRET"
    CONFIDENTIAL = "CONFIDENTIAL"
    def __init__(self,
                on_password_err:Optional[Callable[[],None]]=None,
                on_fail:Optional[Callable[[],None]]=None
        ):
        '''
        Used to handle checking passcodes sent from the CDR.
        Args:

            on_password_err : This function will be called when there is an invalid password
                                Default is None. If None nothing will be done
            on_fail         : This function will be called when there is some other error such
                                as a missing user etc.
        '''
        self.on_fail:Callable[[],None] = lambda : None
        self.on_password_err:Callable[[],None] = lambda : None

        if(on_password_err is not None):
            self.on_password_err = on_password_err
        if(on_fail is not None):
            self.on_fail = on_fail

    def check(self,password:str)->str:

        '''
        Args:

            password : the sequence sent by the CDR

        this function will check the signal and return the appropiate response
        '''
        CorSeq_conf = '[1, 1, 0, 2]'  # correct sequence - confidential
        CorSeq_secret = '[1, 1, 2, 2]'  # correct sequence - secret
        CorSeq_top = '[1, 2, 1, 2]'  # correct sequence - top secret
        if(password == CorSeq_conf):
            return tp.CDR.GRANTED_CONFIDENTIAL
        elif(password == CorSeq_secret):
            return tp.CDR.GRANTED_SECRET
        elif(password == CorSeq_top):
            return tp.CDR.GRANTED_TOPSECRET
        
        self.on_fail()
        return tp.CDR.ACCESS_DENIED
        

class PO_knock_checker:
    '''
    Code for validating the knocks sent by the PO (Provided by team B)
    '''
    PASS_KNOCK = [0.16655588150024414, 0.13585114479064941, 0.3684210777282715, 0.11480975151062012, 0.1613321304321289, 0.4034092426300049, 0.40139293670654297, 0.38600611686706543]
    TOLERANCE = 0.2 #time variation to avoid human errors
    def __init__(self,
                on_password_err:Optional[Callable[[],None]]=None,
                on_fail:Optional[Callable[[],None]]=None
        ):
        '''
        Used to handle checking passcodes sent from the CDR.

        Args:

            on_password_err : This function will be called when there is an invalid password
                                Default is None. If None nothing will be done
            on_fail         : This function will be called when there is some other error such
                                as a missing user etc.
        '''
        self.on_fail:Callable[[],None] = lambda : None
        self.on_password_err:Callable[[],None] = lambda : None

        if(on_password_err is not None):
            self.on_password_err = on_password_err
        if(on_fail is not None):
            self.on_fail = on_fail


    @classmethod
    def compare_knocks(cls,pass_knocks):
        if len(pass_knocks) != len(cls.PASS_KNOCK):
            return False

        for pass_k,rec_k in zip(pass_knocks,cls.PASS_KNOCK):
            diff = abs(pass_k-rec_k)
            if(diff > cls.TOLERANCE):
                return False

        return True
    def check(self,str_array:str)->str:
        '''
        Checks whether sent knock is correct and returns the appropraite response
        
        Args:

            array(str) : A python list containing converted to a string e.g. ['1.0,2.0,3.0,4.5,5.2']
        
        As the array is in string format it needs to be decoded to work with we will exploit the
        fact that in the json format lists are implemented in the same way to convert the string to a list
        using json.loads
        '''
        try:
            float_array = json.loads(str_array)
        
        except json.JSONDecodeError:
            return tp.PO.ACESS_DENIED

        try:
            if(self.compare_knocks(float_array)):
                return tp.PO.ACESS_GRANTED

            return tp.PO.ACESS_DENIED
        except Exception:
            return tp.PO.ACESS_DENIED

        


