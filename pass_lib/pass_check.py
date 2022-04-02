
import hashlib
import json
import logging
from tarfile import ENCODING
from typing import Dict,Any,NamedTuple, Optional

STRING_ENCODING = 'utf-8'




def hash_string(string:str):
    return hashlib.md5(bytes(string,'utf-8')).digest()

class Password_Respones(NamedTuple):
    exists : bool
    valid : Optional[bool] = None

class Password_Manager:
    def __init__(self,dict:Dict[str,Any]):
        self.passwords = dict

    def get_password(self,user):
        if(user not in self.passwords):
            return Password_Respones(False)
        else:
            return Password_Respones(True,self.passwords[user])  
                    
    def check_password_hash(self,user:str,password:str)->Password_Respones:
        if(user not in self.passwords):
            return Password_Respones(False)

        true_hash = self.passwords[user]
        pass_hash = hash_string(password)
        if(pass_hash == true_hash):
            return Password_Respones(True,True)
    
        return Password_Respones(True,False)
            



        






