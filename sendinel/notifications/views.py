from copy import deepcopy
from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from sendinel.backend.models import Patient, Hospital
from sendinel.backend.authhelper import redirect_to_authentication_or
from sendinel.notifications.models import HospitalAppointment, AppointmentType
from sendinel.settings import DEFAULT_SEND_TIME
from sendinel.logger import logger, log_request
from sendinel.notifications.forms import NotificationValidationForm
                               

@log_request
def create_appointment(request, appointment_type_name = None):
    appointment_type = AppointmentType.objects. \
                              filter(name = appointment_type_name)[0]
    nexturl = ""
    backurl = reverse('web_index')
    if request.method == "POST":
        data = deepcopy(request.POST)
        if appointment_type.notify_immediately:
            data['date'] = date.today().strftime('%Y-%m-%d') + \
                            ' ' + DEFAULT_SEND_TIME
        else:
            data['date'] = data.get('date', '') + ' ' + DEFAULT_SEND_TIME
        form = NotificationValidationForm(data)
        if form.is_valid():
            appointment = HospitalAppointment()
            patient = Patient()
            patient.phone_number = form.cleaned_data['phone_number']
            appointment.date = form.cleaned_data['date']
            appointment.appointment_type = appointment_type
            appointment.hospital = Hospital.get_current_hospital()
            appointment.way_of_communication = \
                                    form.cleaned_data['way_of_communication']
            
            request.session['appointment'] = appointment
            request.session['patient'] = patient            
            
            logger.info("Create appointment via %s" %
                            appointment.way_of_communication)
            if appointment.way_of_communication == 'bluetooth':
                return HttpResponseRedirect(reverse("web_list_devices") + \
                                "?next=" + reverse("web_appointment_send"))
            elif appointment.way_of_communication in ('sms', 'voice' ):
                return redirect_to_authentication_or(
                                reverse("web_appointment_save"))

            else:
                logger.error("Unknown way of communication selected.")
                raise Exception ("Unknown way of communication %s " +
                                "(this is neither bluetooth nor sms or voice)"
                                   % appointment.way_of_communication)

        else:
            logger.info("create_appointment: Invalid form.")

    return render_to_response('notifications/create.html',
                            locals(),
                            context_instance=RequestContext(request))

@log_request
def save_appointment(request):
    appointment = request.session.get('appointment', None)
    patient = request.session.get('patient', None)
    
    nexturl = reverse("web_index")
    backurl = reverse("web_appointment_create", kwargs={'appointment_type_name':
                                            appointment.appointment_type.name })
    
    if not appointment or not patient:
        logger.warning("save_appointment: no appointment/patient in session")
        return HttpResponseRedirect(reverse(create_appointment))

    
    logger.info("Saving appointment: %s with patient: %s"
                    % (appointment, patient.phone_number))
    
    
    appointment.save_with_patient(patient)
        
    success = True
    title = _("The \"%s\" notification has been created.") \
                        % appointment.appointment_type.verbose_name
    if appointment.appointment_type.notify_immediately:
        message = _("The patient will be informed immediately.")
    else:
        message = _("Please tell the patient that he/she will be reminded"\
                            " one day before the appointment.")

    return render_to_response('web/status_message.html', 
                              locals(),
                              context_instance = RequestContext(request))

@log_request
def send_appointment(request):
    if (request.method == "POST"):
        appointment = request.session.get('appointment', None)
        mac_address = request.POST['device_mac'].strip()
        
        logger.info("sending appointment to mac_address: " + mac_address)
        logger.info("appointment data: " + unicode(appointment))
        
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
