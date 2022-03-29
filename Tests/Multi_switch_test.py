import test_config
from Utility.Resource import Multi_Or_Switch
import unittest

class test_multi_switch(unittest.TestCase):

    def test_simple_case(self):
        switch_variable = 0
        def on_on():
            nonlocal switch_variable
            switch_variable +=1
        def on_off():
            nonlocal switch_variable
            switch_variable -=1
        switch = Multi_Or_Switch(on_on,on_off)
        h1 = switch.get_handle()
        h1.request_on()
        self.assertEqual(switch_variable,1)
        h1.request_on()
        h1.request_on()
        h1.request_on()
        h1.request_on()
        h1.request_on()
        h1.request_on()
        self.assertEqual(switch._on_counter,1)
        self.assertEqual(switch_variable,1)
        h1.request_off()
        self.assertEqual(switch_variable,0)
        h1.request_off()
        h1.request_off()
        h1.request_off()
        h1.request_off()
        h1.request_off()
        h1.request_off()
        self.assertEqual(switch._on_counter,0)
        self.assertEqual(switch_variable,0)

    def test_multiple_handles(self):
        switch_variable = 0
        def on_on():
            nonlocal switch_variable
            switch_variable +=1
        def on_off():
            nonlocal switch_variable
            switch_variable -=1
        switch = Multi_Or_Switch(on_on,on_off)
        h1 = switch.get_handle()
        h2 = switch.get_handle()
        self.assertEqual(len(switch._handlers),2)
        h1.request_on()
        h1.request_on()
        self.assertEqual(switch_variable,1)
        h2.request_off()
        h2.request_off()
        self.assertEqual(switch_variable,1)
        h2.request_on()
        h2.request_on()
        self.assertEqual(switch_variable,1)
        self.assertEqual(switch._on_counter,2)
        h1.request_off()
        h1.request_off()
        self.assertEqual(switch_variable,1)
        self.assertEqual(switch._on_counter,1)
        h2.request_off()
        self.assertEqual(switch_variable,0)
        self.assertEqual(switch._on_counter,0)
        h2.request_off()
        self.assertEqual(switch_variable,0)
        h3 = switch.get_handle()
        h3.request_on()
        self.assertEqual(switch_variable,1)
        h1.request_off()
        self.assertEqual(switch_variable,1)
        h1.request_on()
        h2.request_on()
        self.assertEqual(switch_variable,1)
        self.assertEqual(switch._on_counter,3)
        h1.request_off()
        self.assertEqual(switch_variable,1)
        h2.request_off()
        self.assertEqual(switch_variable,1)
        h3.request_off()
        h3.request_off()
        self.assertEqual(switch_variable,0)
        self.assertEqual(switch._on_counter,0)
    def test_master_off(self):
        switch_variable = 0
        def on_on():
            nonlocal switch_variable
            switch_variable +=1
        def on_off():
            nonlocal switch_variable
            switch_variable -=1
        switch = Multi_Or_Switch(on_on,on_off)
        h1 = switch.get_handle()
        h2 = switch.get_handle()
        h1.request_on()
        h2.request_on()
        self.assertEqual(switch_variable,1)
        self.assertEqual(switch._on_counter,2)
        switch.master_off()
        self.assertEqual(switch._on_counter,0)
        self.assertEqual(switch_variable,0)
        self.assertEqual(h1.on,False)
        self.assertEqual(h2.on,False)
        h1.request_on()
        self.assertEqual(h1.on,True)
        self.assertEqual(switch_variable,1)
        switch.master_off()
        self.assertEqual(switch_variable,0)
        self.assertEqual(h1.on,False)
        self.assertEqual(h2.on,False)
        





if __name__ == "__main__":
    unittest.main(verbosity=2)