import re
from datetime import datetime

from sendinel.backend.models import AuthenticationCall
from sendinel.settings import AUTHENTICATION_CALL_TIMEOUT, \
                              COUNTRY_CODE_PHONE, \
                              START_MOBILE_PHONE

def format_phonenumber(number):
    """
    Replaces all number specific characters like
    "+", "-" and "/" and checks that there are no
    letters included. Checks also if the number is the number of a 
    mobile phone.
    TODO update docstring for mobile number
    
    @param  number:     The phone number that will be checked
    @type   number:     string
    
    @raise  ValueError
    """
   
    if number.startswith('+'):
        number = number.replace('+', '00', 1)
    
    regex = re.compile('(\/|\+|-| )')
    number = regex.sub('', number)
    
    if number.startswith(COUNTRY_CODE_PHONE):
        number = number.replace(COUNTRY_CODE_PHONE, '0', 1)

    # if the conversion to int does not fail
    # then there are only numbers included
    # in the string
    try:
        int(number)
    except ValueError:
        raise ValueError('Please enter a valid phonenumber.')
    
    if number.startswith(START_MOBILE_PHONE):
        return number
    else:
        raise ValueError('Please enter a valid phonenumber.')    

def check_and_delete_authentication_call(number):
    """
    Try to find an AuthenticationCall for the given phone numner.
    The last seven digits are compared to identify the call.
    """
    number = format_phonenumber(number)
    return True # This disables the authentication TODO make this right!
    last_seven_digits = number[-7:]
    calls = AuthenticationCall.objects.filter( \
                                    number__endswith = last_seven_digits)
    
    return True
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
