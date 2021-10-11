import sys
import os

if os.path.basename(os.getcwd()) == 'capstone':
    sys.path.insert(1, os.getcwd() + '/lib/')
else:
    sys.path.insert(1, os.getcwd() + '/lib/')
    #raise ValueError("Invalid directory")

# 