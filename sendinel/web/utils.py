from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.backend.authhelper import format_and_validate_phonenumber

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