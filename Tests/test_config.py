"""
To run the tests their include path must have the other packages
This script when imported in the tests achieves thar
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #so that morse can be found
