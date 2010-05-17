from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import WayOfCommunication

def render_status_success(request, title, message, \
                          backurl = None, nexturl = None):
    success = True
    return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))
                          
def fill_authentication_session_variable(request):
    number = request.session["patient"].phone_number
    number = format_and_validate_phonenumber(number)
    request.session['authenticate_phonenumber'] = \
                            { 'number': number,
                              'start_time': datetime.now() }
    return number
    
def get_ways_of_communication(immediate = False):
    if immediate:
        return WayOfCommunication.get_immediate_wocs()

    return WayOfCommunication.get_enabled_wocs()