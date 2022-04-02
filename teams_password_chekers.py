'''
Conatins functions for processing and validating passwords from many sub teams
'''
from pass_lib.pass_check import Password_Manager
import Topics as tp
from typing import Callable,Optional




class CCC_pass_checker:
    MORSE_CODE_USER = "MORSE_CODE"
    def __init__(self,
                pass_man:Password_Manager,
                on_fail:Optional[Callable[[],None]]=None,
                on_password_err:Optional[Callable[[],None]]=None,
        ):
        '''
        Used to handle checking passcodes sent from the CCC.
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
    TOP_SECRECT = "TOP_SECRET"
    SECRET = "SECRET"
    CONFIDENTIAL = "CONFIDENTIAL"
    def __init__(self,
                on_password_err:Optional[Callable[[],None]]=None,
                on_fail:Optional[Callable[[],None]]=None
        ):
        '''
        Used to handle checking passcodes sent from the CCC.
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
        