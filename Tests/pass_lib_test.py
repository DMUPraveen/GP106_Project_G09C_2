"""
Code for testing certaing functionalities of the password manager
"""
import test_config
from pass_lib.pass_check import Password_Manager,hash_string
import unittest

class password_manager_tester(unittest.TestCase):

    def setUp(self):
        self.pass_dic = {
            "user1" : hash_string("hello world"),
            "user2" : hash_string("GP106"),
            "user3" : hash_string("")
        }
        self.pm = Password_Manager(self.pass_dic)
    def test_password_exists_and_valid(self):

        re1 = self.pm.check_password_hash("user1","hello world")
        self.assertTrue(re1.exists)
        self.assertTrue(re1.valid)
        re2 = self.pm.check_password_hash("user2","GP106")
        self.assertTrue(re2.exists)
        self.assertTrue(re2.valid)
        re3 = self.pm.check_password_hash("user3","")
        self.assertTrue(re3.exists)
        self.assertTrue(re3.valid)
    def test_password_exists_and_invalid(self):

        re1 = self.pm.check_password_hash("user1","hello world ") # off by one spaec
        self.assertTrue(re1.exists)
        self.assertFalse(re1.valid)
        re2 = self.pm.check_password_hash("user2","106GP")
        self.assertTrue(re2.exists)
        self.assertFalse(re2.valid)
        re3 = self.pm.check_password_hash("user3","asd")
        self.assertTrue(re3.exists)
        self.assertFalse(re3.valid)
    
    def test_password_not_exist(self):
        re1 = self.pm.check_password_hash("user","adadasd")
        self.assertFalse(re1.exists)
        self.assertIsNone(re1.valid)




if __name__ == "__main__":
    unittest.main(verbosity=2)
