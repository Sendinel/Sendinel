import re
from datetime import datetime

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from sendinel.backend.models import AuthenticationCall
from sendinel.settings import AUTHENTICATION_ENABLED, \
                              AUTHENTICATION_CALL_TIMEOUT, \
                              COUNTRY_CODE_PHONE, \
                              START_MOBILE_PHONE

def format_and_validate_phonenumber(number):
    """
    Replaces all number specific characters like
    "+", "-" and "/" and checks that there are no
    letters included. Checks also if the number is 
    the number of a mobile phone.
    
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

    # if the conversion to int does not fail then
    # there are only numbers included in the string
    try:
        int(number)
    except ValueError:
        raise ValidationError(_('Please enter numbers only.'))
    
    if number.startswith(START_MOBILE_PHONE):
        return number
    else:
        raise ValidationError(_('Please enter a cell phone number.'))

def check_and_delete_authentication_call(number):
    """
    Try to find an AuthenticationCall for the given phone numner.
    The last seven digits are compared to identify the call.
    """
    
    number = format_and_validate_phonenumber(number)
    
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
    
    timeout = datetime.now() - AUTHENTICATION_CALL_TIMEOUT
    AuthenticationCall.objects.filter(time__lt = timeout).delete()
    
def redirect_to_authentication_or(url):
    if AUTHENTICATION_ENABLED:
        return HttpResponseRedirect(
            reverse('web_authenticate_phonenumber') + "?next=" + url)
    return HttpResponseRedirect(url)