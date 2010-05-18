from datetime import datetime

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import get_enabled_wocs, \
                                    get_immediate_wocs
                          
def fill_authentication_session_variable(request):
    number = request.session["patient"].phone_number
    number = format_and_validate_phonenumber(number)
    request.session['authenticate_phonenumber'] = \
                            { 'number': number,
                              'start_time': datetime.now() }
    return number
    
def get_ways_of_communication(immediate = False):
    if immediate:
        return get_immediate_wocs()
    return get_enabled_wocs()