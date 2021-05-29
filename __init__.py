server = input("server location")
import sys
import os
if server =="aws":
    sys.path.insert(1, os.getcwd() + '/lib/')
    print("running from AWS SageMaker")
else:
    print("running from: Local")
    if os.path.getatime(os.getcwd()) == 'capstone':
        sys.path.insert(1, os.getcwd() + '/lib/')
    else:
        sys.path.insert(1, "/Users/boula/Documents/GitHub/Public/capstone/lib/")
