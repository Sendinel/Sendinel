import re
from datetime import datetime

from sendinel.backend.models import AuthenticationCall
from sendinel.backend.helper import NotObservedNumberException
from settings import AUTHENTICATION_CALL_TIMEOUT

def format_phonenumber(number):
    """
    Replaces all number specific characters like
    "+", "-" and "/" and checks that there are no
    letters included.
    
    @param  number:     The phone number that will be checked
    @type   number:     string
    
    @raise  ValueError
    """
    regex = re.compile('(\/|\+|-| )')
    new_number = regex.sub('', number)
    
    # if the conversion to int does not fail
    # then there are only numbers included
    # in the string
    if int(new_number) and new_number[0] == '0':
        return new_number
    else:
        raise ValueError('please give national number without country prefix')    

def check_and_delete_authentication_call(number):
    """
    Try to find an AuthenticationCall for the given phone numner.
    The last seven digits are compared to identify the call.
    """
    number = format_phonenumber(number)
    last_seven_digits = number[-7:]
    calls = AuthenticationCall.objects.filter( \
                                    number__endswith = last_seven_digits)
    if calls.count() == 1:
        calls.delete()
        return True
    
    return False
    
def delete_timed_out_authentication_calls():
    """
    Find and delete all timed out authentication calls.
    This can be configured through settings.
    """
    AuthenticationCall.objects.filter(time__lt = calculate_call_timeout()). \
                                                                    delete()
    
def calculate_call_timeout():
    """
    Calculate the time when all calls received before are timed out.
    Can be configured via AUTHENTICATION_CALL_TIMEOUT.
    """
    return (datetime.now() - AUTHENTICATION_CALL_TIMEOUT)