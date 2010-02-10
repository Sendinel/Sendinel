from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from sendinel.backend.models import Patient
from sendinel.web.forms import *

def index(request):
    return render_to_response('start.html',
                              context_instance=RequestContext(request))

def create_appointment(request):
    if request.method == "POST":
        form = HospitalAppointmentForm(request.POST)
        appointment = form.save(commit=False)
        patient = Patient(name = form.cleaned_data['recipient_name'])
        patient.save()
        appointment.recipient = patient
        appointment.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        form = HospitalAppointmentForm()
        return render_to_response('create_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))

        

def input_text(request):
    return render_to_response('input_text.html',
                              context_instance=RequestContext(request))

def choose_communication(request):
    return render_to_response('choose_communication.html',
                              context_instance=RequestContext(request))