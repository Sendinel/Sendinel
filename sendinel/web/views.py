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
from sendinel.backend.models import Patient, ScheduledEvent
from sendinel.web.forms import HospitalAppointmentForm
from sendinel.settings import AUTH_NUMBER, BLUETOOTH_SERVER_ADDRESS
from sendinel.backend import bluetooth

def index(request):
    return render_to_response('start.html',
                              context_instance=RequestContext(request))

def create_appointment(request):
    form = HospitalAppointmentForm(request.POST)
    
    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        
        patient = Patient(name = form.cleaned_data['recipient_name'])
        patient.save()
        
        appointment.recipient = patient
        appointment.save()
        
        if appointment.way_of_communication != 'bluetooth':
            appointment.create_scheduled_event()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render_to_response('create_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))

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
        
    
    
    
    
    
    
