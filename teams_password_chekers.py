'''
Conatins functions for processing and validating passwords from many sub teams
'''
from pass_lib.pass_check import Password_Manager
import Topics as tp
class CDR_sequence_checker:
    TOP_SECRECT = "TOP_SECRET"
    SECRET = "SECRET"
    CONFIDENTIAL = "CONFIDENTIAL"
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
        
        return tp.CDR.ACCESS_DENIED
        