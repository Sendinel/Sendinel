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
from sendinel.backend.models import Patient, ScheduledEvent, Sendable, Doctor
from sendinel.web.forms import HospitalAppointmentForm
from sendinel.settings import AUTH_NUMBER

def index(request):
    return render_to_response('start.html',
                              context_instance=RequestContext(request))

def create_appointment(request):
    
    
    if request.method == "POST":
        form = HospitalAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            patient = Patient(name = form.cleaned_data['recipient_name'])
            patient.save()
            
            appointment.recipient = patient
            appointment.save()
            
            if appointment.way_of_communication != 'bluetooth':
                appointment.create_scheduled_event()

            return HttpResponseRedirect(reverse('index'))
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
