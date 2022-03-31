import time
import paho.mqtt.client as mqtt
import getpass
import stdiomask
from tqdm import tqdm
from colorama import Fore, Back, Style

from pass_lib.pass_check import Password_Manager

users = {
    "Pentagon":b'(\x10\xad\xed\xa7\xc1\xf9\xc9\x1d\xe35e\xb0\xf5\xf8l'
}


def print_welcome_message():
    print(Fore.GREEN,'*'*40,'Welcome to Pentagonal Control Server','*'*40)
    print(Fore.GREEN,'''
                                    ░█▀▀█ █▀▀ █▀▀▄ ▀▀█▀▀ █▀▀█ █▀▀▀ █▀▀█ █▀▀▄ █▀▀█ █
                                    ░█▄▄█ █▀▀ █  █   █   █▄▄█ █ ▀█ █  █ █  █ █▄▄█ █
                                    ░█    ▀▀▀ ▀  ▀   ▀   ▀  ▀ ▀▀▀▀ ▀▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀
                                    
    ''')

def validate_user(pasword_manager : Password_Manager)->bool:
    '''
    Takes user name and password and validates
    '''
    User_get=input("User Name:- ")
    Password_get=stdiomask.getpass(prompt="Password:-",mask='*')
    exist,valid = pasword_manager.check_password_hash(User_get,Password_get)
    if(not exist):
        print(Fore.RED,'#'*50,"User ID is Wrong",'#'*50)
        print(Fore.RED,'#'*52,"Acess Denied",'#'*52)
        print(Fore.RED+"Press Enter to Exit")
        input()
        return False

    if(not valid):
        print(Fore.RED,'#'*50,"Password is Wrong",'#'*50)
        print(Fore.RED,'#'*52,"Acess Denied",'#'*52)
        print(Fore.RED+"Press Enter to Exit")
        input()
        return False
    print('*'*50,"Access Granted",'*'*50)
    return True





