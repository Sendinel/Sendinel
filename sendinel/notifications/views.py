from copy import deepcopy
from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from sendinel.backend.models import Patient, \
                                    Hospital, \
                                    get_woc, \
                                    get_woc_by_id
from sendinel.backend.authhelper import redirect_to_authentication_or
from sendinel.notifications.models import Notification, NotificationType
from sendinel.notifications.forms import NotificationValidationForm, \
										NotificationValidationFormBluetooth
from sendinel.settings import DEFAULT_SEND_TIME
from sendinel.logger import logger, log_request
from sendinel.web.utils import get_ways_of_communication
                               
@log_request
def create_notification(request, notification_type_name = None):
    '''
        Display the form and creates a new notification, but does not
        save it yet. Redirect to authentication if switched on
    '''
    notification_type = NotificationType.objects. \
                              filter(name = notification_type_name)[0]
    nexturl = ""
    backurl = reverse('web_index')
    
    ways_of_communication = get_ways_of_communication(
                                    notification_type.notify_immediately)
    
    if request.method == "POST":
        data = deepcopy(request.POST)
        if notification_type.notify_immediately:
            data['date'] = date.today().strftime('%Y-%m-%d') + \
                            ' ' + DEFAULT_SEND_TIME
        else:
            data['date'] = data.get('date', '') + ' ' + DEFAULT_SEND_TIME
			
        form = NotificationValidationForm(data)

        woc = get_woc_by_id( request.POST['way_of_communication'] )
        if not woc.can_send_immediately:
		    form = NotificationValidationFormBluetooth(data)
		
        if form.is_valid():
            notification = Notification()
            patient = Patient()
            if woc.can_send_immediately:
                patient.phone_number = form.cleaned_data['phone_number']
            notification.date = form.cleaned_data['date']
            notification.notification_type = notification_type
            notification.hospital = Hospital.get_current_hospital()
            notification.way_of_communication = \
                                    form.cleaned_data['way_of_communication']
                                    
            request.session['notification'] = notification
            request.session['patient'] = patient            
            
            logger.info("Create notification via %s" %
                            notification.way_of_communication.verbose_name)
            if notification.way_of_communication == get_woc('bluetooth'):
                return HttpResponseRedirect(reverse("web_list_devices") + \
                                "?next=" + reverse("notifications_send"))
            elif notification.way_of_communication.name in ('sms', 'voice' ):
                return redirect_to_authentication_or(
                                reverse("notifications_save"))

            else:
                logger.error("Unknown way of communication selected.")
                raise Exception ("Unknown way of communication %s " \
                                 %notification.way_of_communication.\
                                 verbose_name + "(this is neither " + \
                                 "bluetooth nor sms or voice)") 
                                
        else:
        
            logger.info("create_notification: Invalid form.")
        
    return render_to_response('notifications/create.html',
                            locals(),
                            context_instance=RequestContext(request))

@log_request
def save_notification(request):
    notification = request.session.get('notification', None)
    patient = request.session.get('patient', None)
    
    nexturl = reverse("web_index")
    backurl = reverse("notifications_create", 
                      kwargs={'notification_type_name':
                               notification.notification_type.name })
    
    if not notification or not patient:
        logger.warning("save_notification: no notification/patient in session")
        return HttpResponseRedirect(reverse(create_notification))

    
    logger.info("Saving notification: %s with patient: %s"
                    % (notification, patient.phone_number))
    
    
    notification.save_with_patient(patient)
        
    title = _("The \"%s\" notification has been created.") \
                        % notification.notification_type.verbose_name
    new_button_label = _("New notification")
    
    if notification.notification_type.notify_immediately:
        message = _("The patient will be informed immediately.")
    else:
        message = _("Please tell the patient that he/she will be reminded"\
                            " one day before the notification.")
    success = True
    
    return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))  

@log_request
def send_notification_via_bluetooth(request):
    if (request.method == "POST"):
        notification = request.session.get('notification', None)
        mac_address = request.POST['device_mac'].strip()
        
        logger.info("sending notification to mac_address: " + mac_address)
        logger.info("notification data: " + unicode(notification))
        
        notification.bluetooth_mac_address = mac_address
        notification.bluetooth_server_address = \
                                        request.META['REMOTE_ADDR'].strip()
        output_data = notification.get_data_for_sending()
        result = output_data.send()
        if(result):
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 500) 
           
    backurl = reverse("web_list_devices")
    url = reverse("notifications_send")
    next = reverse("web_index")
    mac_address = request.GET['device_mac'].strip()
    
    return render_to_response('web/send_bluetooth_notification.html',
                                locals(),
                                context_instance=RequestContext(request))
