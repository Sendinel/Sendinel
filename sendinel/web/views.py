from datetime import datetime
import time
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.i18n import javascript_catalog

from sendinel.backend.authhelper import check_and_delete_authentication_call, \
                                    delete_timed_out_authentication_calls, \
                                    format_phonenumber
from sendinel.backend.models import Patient, Sendable, \
                                    InfoService, Subscription, \
                                    HospitalAppointment, Hospital, \
                                    AppointmentType
from sendinel.web.forms import HospitalAppointmentForm
from sendinel.settings import   AUTH_NUMBER, \
                                BLUETOOTH_SERVER_ADDRESS, \
                                AUTHENTICATION_CALL_TIMEOUT, \
                                COUNTRY_CODE_PHONE, START_MOBILE_PHONE, \
                                ADMIN_MEDIA_PREFIX
from sendinel.backend import bluetooth
from sendinel.logger import logger, log_request

@log_request
def index(request):
    information_services = InfoService.objects.all()
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

def is_valid_appointment(post_vars):
    if not post_vars.has_key("date") or \
       not post_vars.has_key("way_of_communication") or \
       not post_vars.has_key("recipient"):
        return False
        
    if not post_vars["way_of_communication"]:
        return False
    
    try:
        appointment_date = datetime.strptime(post_vars["date"] , "%Y-%m-%d")
        format_phonenumber(post_vars["recipient"])
    except ValueError:
        return False
        
    return True

@log_request
def create_appointment(request, appointment_type = None):
    admin_media_prefix = ADMIN_MEDIA_PREFIX
    nexturl = ""
    backurl = reverse('web_index')
    if request.method == "POST":

        if is_valid_appointment(request.POST):
            
            appointment = HospitalAppointment()
            patient = Patient()
            patient.phone_number = request.POST['recipient']
            
            appointment.date = datetime.strptime(request.POST['date'] , "%Y-%m-%d")
            appointment.appointment_type = request.session['appointment_type']
            appointment.hospital = Hospital.get_current_hospital()
            appointment.way_of_communication = request.POST['way_of_communication']             
    
            
            
            request.session['appointment'] = appointment
            request.session['patient'] = patient            
            
            logger.info("Create appointment via %s" %
                            appointment.way_of_communication)
            if appointment.way_of_communication == 'bluetooth':
                return HttpResponseRedirect(reverse("web_list_devices") + \
                                "?next=" + reverse("web_appointment_send"))
            elif appointment.way_of_communication in ('sms', 'voice' ):

                return HttpResponseRedirect( \
                    reverse("web_authenticate_phonenumber") + "?next=" + \
                    reverse("web_appointment_save"))
            else:
                logger.error("Unknown way of communication selected.")
                raise Exception ("Unknown way of communication %s " \
                                   %appointment.way_of_communication) +\
                                "(this is neither bluetooth nor sms or voice)"
        else:
            logger.info("create_appointment: Invalid form.")
            return render_to_response('web/appointment_create.html',
                                locals(),
                                context_instance=RequestContext(request))
    else:
        #TODO: initiale Dateneintraege
        if appointment_type != None:
            request.session['appointment_type'] = AppointmentType.get_appointment_type(appointment_type)
            
        appointment_type = request.session['appointment_type']
        
        return render_to_response('web/appointment_create.html',
                                locals(),
                                context_instance=RequestContext(request))

@log_request
def save_appointment(request):
    nexturl = reverse("web_index")
    appointment = request.session.get('appointment', None)
    patient = request.session.get('patient', None)
    if not appointment or not patient:
        logger.warning("save_appointment: no appointment/patient in session")
        return HttpResponseRedirect(reverse(create_appointment))

    
    logger.info("Saving appointment: %s with patient: %s"
                    % (appointment, patient.phone_number))
    
    
    appointment.save_with_patient(patient)

    return render_to_response('web/appointment_saved.html',
                            locals(),
                            context_instance=RequestContext(request))

@log_request
def send_appointment(request):
    if (request.method == "POST"):
        appointment = request.session.get('appointment', None)
        mac_address = request.POST['device_mac'].strip()
        
        logger.info("sending appointment to mac_address: " + mac_address)
        logger.info("appointment data: " + str(appointment))
        
        appointment.bluetooth_mac_address = mac_address
        output_data = appointment.get_data_for_sending()
        result = output_data.send()
        if(result):
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 500)
           
    backurl = reverse("web_list_devices")
    url = reverse("web_appointment_send")
    next = reverse("web_index")
    mac_address = request.GET['device_mac'].strip()

    return render_to_response('web/send_bluetooth_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))

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
        next = request.GET.get('next', reverse('web_appointment_save'))
        return render_to_response('web/authenticate_phonenumber_call.html', 
                          locals(),
                          context_instance = RequestContext(request))
    except ValueError as e:
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
    backurl = reverse("web_appointment_create")
    return render_to_response('web/list_devices.html',
                                locals(),
                                context_instance=RequestContext(request))

@log_request
def get_bluetooth_devices(request):
    response_dict = {}
    devices_list = []
    
    try:
        devices = bluetooth.get_discovered_devices(BLUETOOTH_SERVER_ADDRESS)
        for device in devices.items():
            device_dict = {}
            device_dict["name"] = device[1]
            device_dict["mac"] = device[0]
            devices_list.append(device_dict)
        response_dict["devices"] = devices_list
        
        logger.debug("Got Bluetooth Devices: %s"% str(devices_list))
        
        return HttpResponse(content = simplejson.dumps(response_dict),
                            content_type = "application/json")
    except Exception as e:
        logger.error("get_bluetooth_devices from %s failed: %s" %
                        (BLUETOOTH_SERVER_ADDRESS, str(e)))
        # TODO write bluetooth error to log file
        return HttpResponse(status = 500)

@log_request
def register_infoservice(request, id):
    ajax_url= reverse('web_check_call_received')
    
    if request.method == "POST":
        request.session['way_of_communication'] = \
                                        request.POST['way_of_communication']
        patient = Patient()
        patient.phone_number = request.POST['number']
        request.session['patient'] = patient
        try:                                
            number = fill_authentication_session_variable(request) 
            auth_number = AUTH_NUMBER
            backurl = reverse('web_infoservice_register',  kwargs = {'id': id})        
            next = reverse('web_infoservice_register_save', kwargs = {'id': id})
            url = reverse('web_check_call_received')
            
            return render_to_response('web/authenticate_phonenumber_call.html', 
                locals(),
                context_instance = RequestContext(request))
        except ValueError as e:
            error = e
       
    infoservice = InfoService.objects.filter(pk = id)[0].name
    backurl = reverse("web_index")
    
    return render_to_response('web/infoservice_register.html', 
                              locals(),
                              context_instance = RequestContext(request))

@log_request
def save_registration_infoservice(request, id):
    patient = request.session['patient']
    patient.save()
    way_of_communication = request.session['way_of_communication']
    infoservice = InfoService.objects.filter(pk = id)[0]
    subscription = Subscription(patient = patient,
                                way_of_communication = way_of_communication,
                                infoservice = infoservice)
    subscription.save()
    logger.info("Saved subscription %s.", str(subscription))
    
    return HttpResponseRedirect(reverse('web_index'))


@log_request
def fill_authentication_session_variable(request):
    number = request.session["patient"].phone_number
    number = format_phonenumber(number)
    request.session['authenticate_phonenumber'] = \
                            { 'number': number,
                              'start_time': datetime.now() }
    return number

@log_request
def not_implemented(request):
    backurl = reverse("web_index")
    return render_to_response('web/not_implemented.html', 
                              locals(),
                              context_instance = RequestContext(request))

@log_request
def list_infoservices(request):
    backurl = reverse("web_index")
    informationservices = InfoService.objects.all()
    return render_to_response('web/list_infoservices.html', 
                              locals(),
                              context_instance = RequestContext(request))

