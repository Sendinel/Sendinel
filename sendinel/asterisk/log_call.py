#!/usr/bin/python
import sys
# adapt paths for call from asterisk
from os.path import abspath, dirname

PROJECT_PATH = dirname(abspath(__file__)) + "/../../"
sys.path.insert(0, PROJECT_PATH)

from django.core.management import setup_environ
from sendinel import settings
setup_environ(settings)

from sendinel.backend.models import AuthenticationCall

def log_call():
    """
    Save calls from asterisk in the database.
    This function reads data from stdin and should be called by asterisk
    using the Asterisk Gateway Interface (AGI)
    """
    # TODO evaluate wether this should be called via XMLRPC to avoid 
    #      permission problems
    
    # read all data from stdin - should be less than 25 lines
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        (key, value) = line.split(":", 1)
        if key == "agi_callerid":
            number = value.strip()
            AuthenticationCall(number = number).save()
            break


if __name__ == "__main__":
    log_call()
