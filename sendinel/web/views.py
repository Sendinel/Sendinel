from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.i18n import javascript_catalog
from django.utils.translation import ugettext as _

from sendinel.backend import bluetooth
from sendinel.backend.authhelper import check_and_delete_authentication_call, \
                                    delete_timed_out_authentication_calls
from sendinel.infoservices.models import InfoService
from sendinel.notifications.models import AppointmentType
from sendinel.logger import logger, log_request
from sendinel.settings import   AUTH_NUMBER, \
                                AUTHENTICATION_CALL_TIMEOUT
from sendinel.web.utils import fill_authentication_session_variable


@log_request
def index(request):
    groups = InfoService.objects.all().filter(type="information")
    medicine_count = InfoService.objects.all().filter(type="medicine").count()
    appointment_types = AppointmentType.objects.all()
    return render_to_response('web/index.html',
                              locals(),  
                              context_instance = RequestContext(request))

@log_request
def choose_language(request):
    return render_to_response('web/language_choose.html',
                              locals(),
                              context_instance = RequestContext(request))

def jsi18n(request):
    js_info_web = {
        'packages': ('sendinel')
    }
    return javascript_catalog(request, packages = js_info_web)


@log_request
def authenticate_phonenumber(request):
    nexturl = ''
    next = ''
    ajax_url= reverse('web_check_call_received')
    backurl = reverse('web_index')
    
   
    logger.info("Deleting timed out authentication calls.")
    delete_timed_out_authentication_calls()
    
    try:    
        number = fill_authentication_session_variable(request)
        logger.info("Starting authentication with %s" % AUTH_NUMBER)
        auth_number = AUTH_NUMBER
        next = request.GET.get('next', reverse('notifications_save'))
        return render_to_response('web/authenticate_phonenumber_call.html', 
                          locals(),
                          context_instance = RequestContext(request))
    except ValueError, e:
        error = e

@log_request
def check_call_received(request):
    response_dict = {}

    try:
        response_dict["status"] = "failed"

        number = request.session['authenticate_phonenumber']['number']
        start_time = request.session['authenticate_phonenumber']['start_time']

        if (start_time + AUTHENTICATION_CALL_TIMEOUT) >= datetime.now():
            if check_and_delete_authentication_call(number):
                response_dict["status"] = "received"
                logger.info("check_call_received: call received.")
            else:
                response_dict["status"] = "waiting"
    except KeyError:
        pass

    return HttpResponse(content = simplejson.dumps(response_dict),
                        content_type = "application/json")

@log_request
def list_bluetooth_devices(request):
    next = request.GET.get('next', '')
    backurl = reverse("notifications_create", kwargs=
                       {"appointment_type_name":
                           request.session["appointment"].appointment_type.name})
    return render_to_response('web/list_devices.html',
                                locals(),
                                context_instance=RequestContext(request))

@log_request
def get_bluetooth_devices(request):
    response_dict = {}
    devices_list = []    
    
    try:
        devices = bluetooth.get_discovered_devices(request.META["REMOTE_ADDR"])
        for device in devices.items():
            device_dict = {}
            device_dict["name"] = device[1]
            device_dict["mac"] = device[0]
            devices_list.append(device_dict)
        response_dict["devices"] = devices_list
        
        logger.debug("Got Bluetooth Devices: %s"% str(devices_list))
        
        return HttpResponse(content = simplejson.dumps(response_dict),
                            content_type = "application/json")
    except Exception, e:
        logger.error("get_bluetooth_devices from %s failed: %s" %
                        (request.META["REMOTE_ADDR"], str(e)))
        return HttpResponse(status = 500)

@log_request
def imprint(request):
    backurl = reverse("web_index")
    return render_to_response('web/imprint.html',
                              locals(),
                              context_instance = RequestContext(request))

