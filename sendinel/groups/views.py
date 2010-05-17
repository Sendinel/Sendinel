from copy import deepcopy

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.backend.models import Patient
from sendinel.backend.authhelper import redirect_to_authentication_or
from sendinel.groups.models import InfoService, InfoMessage, Subscription
from sendinel.groups.forms import InfoMessageValidationForm, \
                                  NotificationValidationForm2
from sendinel.logger import logger, log_request
from sendinel.settings import AUTH_NUMBER
from sendinel.web.views import fill_authentication_session_variable, \
                               render_status_success

@log_request
def send_message(request, id):
    group = get_object_or_404(InfoService, pk = id)
    if(request.method == "POST"):
        form = InfoMessageValidationForm(request.POST)
        
        if form.is_valid():
            create_messages_for_group(group, form.cleaned_data['text'])
            
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All members of the \"%s\" service" + \
                        " will get your message.") \
                                % group.name
            
            render_status_success(request, title, message, nexturl = nexturl)

        
    return render_to_response("groups/message_create.html",
                              locals(),
                              context_instance = RequestContext(request))          

def create_messages_for_group(group, text):
    '''
        Put together all information for an infomessage and
        calls InfoService.create_scheduled_event
    '''
    
    for patient in group.members.all():
        info_message = InfoMessage()
        info_message.text = text
        subscription = Subscription.objects.filter(patient = patient,
                                            infoservice = group)[0]
        info_message.recipient = patient
        info_message.send_time = datetime.now()
        info_message.way_of_communication = \
                        subscription.way_of_communication
        info_message.save()        
        info_message.create_scheduled_event(datetime.now())
        logger.info("Created %s", str(info_message))                            
                              
def set_session_variables_for_register(request):
    request.session['way_of_communication'] = \
                                    request.POST['way_of_communication']
    patient = Patient()
    patient.phone_number = request.POST['phone_number']
    request.session['patient'] = patient                                   
                                   
@log_request
def register(request, group_id):
    ajax_url= reverse('web_check_call_received')
    
    if request.method == "POST":
        set_session_variables_for_register(request)
            
        data = deepcopy(request.POST)
        form = NotificationValidationForm2(data)
        if form.is_valid():
            number = fill_authentication_session_variable(request) 
            auth_number = AUTH_NUMBER
            backurl = reverse('web_index')        

            return redirect_to_authentication_or(reverse \
                    ('groups_register_save', 
                     kwargs = {'group_id': group_id}))
        else:
            logger.info("register: Invalid form.")
       
    group = get_object_or_404(InfoService,pk = group_id)
    backurl = reverse("web_index")
    
    return render_to_response('groups/register.html', 
                              locals(),
                              context_instance = RequestContext(request))
                             
@log_request
def save_registration_infoservice(request, group_id):
    backurl = reverse('groups_register', 
                      kwargs = {'group_id': group_id})        
    nexturl = reverse('web_index')
    
    subscription = subscription_save(request, group_id)
    
    success = True
    title = _("Registration successful")
    message = _("The patient will now receive all messages from the "
                        " \"%s\" service.") % subscription.infoservice.name
    
    return render_status_success(request, title, message, 
                                 backurl = backurl, nexturl = nexturl)                                
                              
@log_request                              
def subscription_save(request, id):
    patient = request.session['patient']
    patient.save()
    way_of_communication = request.session['way_of_communication']
    infoservice = InfoService.objects.filter(pk = id)[0]
    subscription = Subscription(patient = patient,
                                way_of_communication = way_of_communication,
                                infoservice = infoservice)
    subscription.save()
    logger.info("Saved subscription %s of type %s.", 
                (unicode(subscription), 
                 unicode(subscription.infoservice.type)))
    return subscription                                                       
    