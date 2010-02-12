from sendinel import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.backend.models import Patient, ScheduledEvent
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
            send_time = appointment.date - settings.REMINDER_DAYS_BEFORE_EVENT
            scheduled_event= ScheduledEvent()
            scheduled_event.sendable = appointment
            scheduled_event.send_time = send_time
            scheduled_event.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render_to_response('create_appointment.html',
                                locals(),
                                context_instance=RequestContext(request))



def input_text(request):
    return render_to_response('input_text.html',
                              context_instance=RequestContext(request))

def choose_communication(request):
    return render_to_response('choose_communication.html',
                              context_instance=RequestContext(request))