
import hashlib
import json
from typing import Dict,Any,NamedTuple, Optional,Callable

STRING_ENCODING = 'utf-8'




def hash_string(string:str):
    """
    converts supplied string into a md5 hash in hexformat
    """
    return hashlib.md5(bytes(string,'utf-8')).hexdigest()

class Password_Respones(NamedTuple):
    """
    Response structure for a password query
    """
    exists : bool #: whether user name exists or not
    valid : Optional[bool] = None #: whether the password is correct or not

class Password_Manager:
    """
    Class for querying and managing passwords and passcodes used in the project
    """
    def __init__(self,password_dictionary:Dict[str,str],on_update:Optional[Callable[[Dict[str,str]],None]]=None):
        """
        Args:
            password_dictionary : dictionary conatining users and passwords
            on_update           : function to be called when the dictionary is updated (such as sacing to a database or file) 
        """
        self.passwords:Dict[str,str] = password_dictionary
        self.on_update:Callable[[Dict[str,str]],None] = lambda _ : None
        if(on_update is not None):
            self.on_update = on_update


    def check_password(self,user:str,password:str)->Password_Respones:
        """
        Checks the password of stored with the user against the provided password

        Args:

            user (str)      : username for the password
            password(str)   : password to be checked
        """
        if(user not in self.passwords):
            return Password_Respones(False)
        else:
            return Password_Respones(True,password==self.passwords[user])  
                    
    def check_password_hash(self,user:str,password:str)->Password_Respones:
        """
        Similar to password check but checks the hash of the password against the stored hash
        """
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

    def update_passwords(self,user:str,password:str,master_user:str,master_password:str,store_hash=False,master_check_hash=True):
        '''
        Used to update passwords
        '''
        if(master_check_hash):
            res = self.check_password_hash(master_user,master_password)
        else:
            res = self.check_password(master_user,master_password)
        if(res.exists and res.valid):
            if(store_hash):
                self.passwords[user] = hash_string(password)
            else:
                self.passwords[user] = password
            self.on_update(self.passwords)


        






