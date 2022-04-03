
import hashlib
import json
from typing import Dict,Any,NamedTuple, Optional,Callable

STRING_ENCODING = 'utf-8'




def hash_string(string:str):
    return hashlib.md5(bytes(string,'utf-8')).hexdigest()

class Password_Respones(NamedTuple):
    exists : bool
    valid : Optional[bool] = None

class Password_Manager:
    def __init__(self,password_dictionary:Dict[str,str],on_update:Optional[Callable[[Dict[str,str]],None]]=None):
        self.passwords:Dict[str,str] = password_dictionary
        self.on_update:Callable[[Dict[str,str]],None] = lambda _ : None
        if(on_update is not None):
            self.on_update = on_update


    def check_password(self,user,password):
        if(user not in self.passwords):
            return Password_Respones(False)
        else:
            return Password_Respones(True,password==self.passwords[user])  
                    
    def check_password_hash(self,user:str,password:str)->Password_Respones:
        if(user not in self.passwords):
            return Password_Respones(False)

        true_hash = self.passwords[user]
        pass_hash = hash_string(password)
        if(pass_hash == true_hash):
            return Password_Respones(True,True)
    
        return Password_Respones(True,False)
            
    @classmethod
    def password_manager_from_file(cls,file_name:str):
        '''
        Used to create a passwrod manager from a json file
        automatically adds an appropriate on_update function
        '''
        password_dictionary = json.load(open(file_name,"r"))
        def on_update(dictionary:Dict[str,str]):
            with open(file_name,"w") as f:
                json.dump(password_dictionary,f)


        return cls(password_dictionary,on_update)

    def update_passwords(self):
        self.on_update(self.passwords)


        






