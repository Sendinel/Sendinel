from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.contrib import messages

from sendinel.backend.authhelper import check_and_delete_authentication_call, \
                                    delete_timed_out_authentication_calls, \
                                    format_phonenumber
from sendinel.backend.models import Patient, ScheduledEvent, Sendable, \
                                    InfoService
from sendinel.web.forms import HospitalAppointmentForm
from sendinel.settings import   AUTH_NUMBER, \
                                BLUETOOTH_SERVER_ADDRESS, \
                                AUTHENTICATION_CALL_TIMEOUT, \
                                COUNTRY_CODE_PHONE, START_MOBILE_PHONE, \
                                ADMIN_MEDIA_PREFIX
from sendinel.backend import bluetooth
from sendinel.logger import logger


def index(request):
    informationservices = InfoService.objects.all()
    return render_to_response('web/index.html',
                              locals(),  
                              context_instance=RequestContext(request))

def create_appointment(request):
    admin_media_prefix = ADMIN_MEDIA_PREFIX
    if request.method == "POST":
        form = HospitalAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient = Patient(name = form.cleaned_data['recipient_name'])
            request.session['appointment'] = appointment
            request.session['patient'] = patient            
            
            if appointment.way_of_communication == 'bluetooth':
                return HttpResponseRedirect(reverse("web_list_devices") + \
                                "?next=" + reverse("web_appointment_send"))
            elif appointment.way_of_communication in ('sms', 'voice' ):
                return HttpResponseRedirect( \
                    reverse("web_authenticate_phonenumber") + "?next=" + \
                    reverse("web_appointment_save"))
            else:
                raise Exception ("Unknown way of communication %s " \
                                   %appointment.way_of_communication) +\
                                "(this is neither bluetooth nor sms or voice)"
        else:
            return render_to_response('web/appointment_create.html',
                                locals(),
                                context_instance=RequestContext(request))
    else:
        #TODO: initiale Dateneintraege funktionieren noch nicht
        # try:
        #     initial_data = {'doctor': unicode(Doctor.objects.all().get())}
        # except Doctor.DoesNotExist:
        #     initial_data = {}
        initial_data = {'way_of_communication': \
                        Sendable.WAYS_OF_COMMUNICATION[0][1]}
        form = HospitalAppointmentForm(initial = initial_data)
        return render_to_response('web/appointment_create.html',
                                locals(),
                                context_instance=RequestContext(request))
  
def save_appointment(request):
    appointment = request.session.get('appointment', None)
    patient = request.session.get('patient', None)
    if not appointment or not patient:
        return HttpResponseRedirect(reverse(create_appointment))
    # TODO Rueckgabe testen, Fehlerbehandlung
    patient.phone_number = request.session['authenticate_phonenumber']['number']
    
    appointment.save_with_patient(patient)

    return render_to_response('web/appointment_saved.html',
                            locals(),
                            context_instance=RequestContext(request))

def send_appointment(request):
    appointment = request.session.get('appointment', None)
    mac_address = request.POST['device_mac'].strip()
    
    logger.info("started send_appointment to mac_address: " + mac_address)
    
    appointment.bluetooth_mac_address = mac_address
    output_data = appointment.get_data_for_sending()
    output_data.send()
    
    
def authenticate_phonenumber(request):
    next = ''
    if request.method == "POST":
        number = request.POST["number"].strip()

        number = format_phonenumber(number, COUNTRY_CODE_PHONE, START_MOBILE_PHONE)
        auth_number = AUTH_NUMBER
        request.session['authenticate_phonenumber'] = \
                                { 'number': number,
                                  'start_time': datetime.now() }
        next = request.GET.get('next','')
        return render_to_response('web/authenticate_phonenumber_call.html', 
                              locals(),
                              context_instance = RequestContext(request))
        # TODO implement form validation
        
    delete_timed_out_authentication_calls()
    
    patient = request.session.get('patient', None)
    if(patient):
        patient_name = patient.name
    
    locals().update({'next': next})
    return render_to_response('web/authenticate_phonenumber.html', 
                              locals(),
                              context_instance = RequestContext(request))

def check_call_received(request):
    response_dict = {}

    try:
        response_dict["status"] = "failed"

        number = request.session['authenticate_phonenumber']['number']
        start_time = request.session['authenticate_phonenumber']['start_time']
    
        if (start_time + AUTHENTICATION_CALL_TIMEOUT) >= datetime.now():
            if check_and_delete_authentication_call(number):
                response_dict["status"] = "received"
            else:
                response_dict["status"] = "waiting"
    except KeyError:
        pass

    return HttpResponse(content = simplejson.dumps(response_dict),
                        content_type = "application/json")

def list_bluetooth_devices(request):
    next = request.GET.get('next','')
    return render_to_response('web/list_devices.html',
                                locals(),
                                context_instance=RequestContext(request))

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
        
        return HttpResponse(content = simplejson.dumps(response_dict),
                            content_type = "application/json")
    except:
        # TODO write bluetooth error to log file
        return HttpResponse(status = 500)
        
def register_infoservice(request, id):
    request.session['infoservice_message'] = "In order to register for the " + \
                                "informationservice " + \
                                InfoService.objects.filter(pk = id)[0].name + \
                                "you have to authenticate your phone"
    return HttpResponseRedirect(reverse('web_authenticate_phonenumber'))
                             # "?next=" + 
                             # reverse('web_infoservice_register', \
                                     # kwargs={'id': id}))
    # return render_to_response('web/register_infoservice.html',
                              # locals(),
                              # context_instance=RequestContext(request))
        

