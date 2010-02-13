from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.backend.models import Patient, ScheduledEvent
from sendinel.backend.authhelper import AuthHelper
from sendinel.web.forms import *

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
        authHelper = AuthHelper()
        
        number = request.REQUEST["phonenumber"]
        number = authHelper.authenticate(number)
        if number:
            return render_to_response('authenticate_phonenumber_call.html', 
                                      locals(),
                                      context_instance = RequestContext(request))
        else:
            # there should happen something if the number was not valid
            pass
    
    return render_to_response('authenticate_phonenumber.html', 
                              locals(),
                              context_instance = RequestContext(request))

def input_text(request):
    return render_to_response('input_text.html',
                              context_instance=RequestContext(request))

def choose_communication(request):
    return render_to_response('choose_communication.html',
                              context_instance=RequestContext(request))