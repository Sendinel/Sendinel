from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from sendinel.backend.authhelper import calculate_call_timeout, \
                                    check_and_delete_authentication_call, \
                                    delete_timed_out_authentication_calls, \
                                    format_phonenumber
from sendinel.backend.models import Patient, ScheduledEvent, Sendable, Doctor, Hospital
from sendinel.web.forms import HospitalAppointmentForm
from sendinel.settings import AUTH_NUMBER, DEFAULT_HOSPITAL_NAME, BLUETOOTH_SERVER_ADDRESS
from sendinel.backend import bluetooth

def index(request):
    return render_to_response('start.html',
                              context_instance=RequestContext(request))

def create_appointment(request):
    if request.method == "POST":
        form = HospitalAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient = Patient(name = form.cleaned_data['recipient_name'])
            request.session['appointment'] = appointment
            request.session['patient'] = patient
            
            if appointment.way_of_communication == 'bluetooth':
                return HttpResponseRedirect(reverse("list_devices") + \
                                "?next=" + reverse(send_appointment))
            elif appointment.way_of_communication in ('sms', 'voice' ):
                return HttpResponseRedirect( \
                    reverse("authenticate_phonenumber") + "?next=" + \
                    reverse(save_appointment))
            else:
                raise Exception ("Unknown way of communication %s " \
                                   %appointment.way_of_communication) +\
                                "(this is neither bluetooth nor sms or voice)"
        else: 
            return render_to_response('create_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))
    else:
        #TODO: initiale Dateneintraege funktionieren noch nicht
        try:
            initial_data = {'doctor': unicode(Doctor.objects.all()[0])}
        except Doctor.DoesNotExist:
            initial_data = {}
        initial_data.update({'way_of_communication': Sendable.WAYS_OF_COMMUNICATION[0][1]})
        form = HospitalAppointmentForm(initial = initial_data)
        return render_to_response('create_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))
  
def save_appointment(request):
    appointment = request.session.get('appointment', None)
    patient = request.session.get('patient',None)
    if not appointment or not patient:
        return HTTPResponseRedirect(reverse(create_appointment))
    # TODO Rueckgabe testen, Fehlerbehandlung
    appointment.save_with_patient(patient)

def authenticate_phonenumber(request):
    if request.method == "POST":
        number = request.REQUEST["number"].strip()
        number = format_phonenumber(number)
        name = request.REQUEST["name"].strip()
        auth_number = AUTH_NUMBER

        
        request.session['authenticate_phonenumber'] = \
                                { 'name': name,
                                  'number': number,
                                  'start_time': datetime.now() }
        
        return render_to_response('authenticate_phonenumber_call.html', 
                              locals(),
                              context_instance = RequestContext(request))
        # TODO implement form validation


    delete_timed_out_authentication_calls()

    return render_to_response('authenticate_phonenumber.html', 
                              locals(),
                              context_instance = RequestContext(request))

def check_call_received(request):
    response_dict = {}

    try:
        response_dict["status"] = "failed"

        number = request.session['authenticate_phonenumber']['number']
        start_time = request.session['authenticate_phonenumber']['start_time']
    
        if start_time >= calculate_call_timeout():
            if check_and_delete_authentication_call(number):
                response_dict["status"] = "received"
            else:
                response_dict["status"] = "waiting"
    except KeyError:
        pass

    return HttpResponse(content = simplejson.dumps(response_dict),
                        content_type = "application/json")

def input_text(request):
    return render_to_response('input_text.html',
                              context_instance=RequestContext(request))

def choose_communication(request):
    return render_to_response('choose_communication.html',
                              context_instance=RequestContext(request))

def list_bluetooth_devices(request):
    return render_to_response('list_devices.html',
                                locals(),
                                context_instance=RequestContext(request))

def get_bluetooth_devices(request):
    response_dict = {}
    devices_list = []
    
    devices = bluetooth.get_discovered_devices(BLUETOOTH_SERVER_ADDRESS)
    for device in devices.items():
        device_dict = {}
        device_dict["name"] = device[1]
        device_dict["mac"] = device[0]
        devices_list.append(device_dict)
    response_dict["devices"] = devices_list
    
    return HttpResponse(content = simplejson.dumps(response_dict),
                        content_type = "application/json")
        
    
    
    
    
    
    
