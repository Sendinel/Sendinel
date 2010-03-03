#!/usr/bin/python
import sys

from django.core.management import setup_environ
from sendinel import settings
from sendinel.backend.models import AuthenticationCall


setup_environ(settings)


def log_call():
    """
    Save calls from asterisk in the database.
    This function reads data from stdin and should be called by asterisk
    using the Asterisk Gateway Interface (AGI)
    """
    # read all data from stdin - should be less than 25 lines
    data = sys.stdin.readlines()
    
    number = None
    
    for line in data:
        (key, value) = line.split(":", 1)
        if key == "agi_callerid":
            number = value
            break
    
    if not number:
        raise ValueError("agi_callerid not found in stdin data.")
    
    number = number.strip()
    AuthenticationCall(number = number).save()
    

if __name__ == "__main__":
    log_call()
