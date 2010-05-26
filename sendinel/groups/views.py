from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.backend.models import Patient, \
                                    Hospital, \
                                    WayOfCommunication
from sendinel.backend.authhelper import redirect_to_authentication_or
from sendinel.infoservices.models import InfoService, Subscription
from sendinel.groups.forms import InfoMessageValidationForm, \
                                  NotificationValidationForm2
from sendinel.infoservices.utils import create_messages_for_infoservice, \
                                        set_session_variables_for_register, \
                                        subscription_save
from sendinel.logger import logger, log_request
from sendinel.settings import AUTH_NUMBER
from sendinel.web.utils import fill_authentication_session_variable, \
                               get_ways_of_communication

@log_request
def send_message(request, group_id):
    '''
        Display the form and send a message to all 
        patients who subscribed to the information group. 
    '''
    group = get_object_or_404(InfoService, pk = group_id)
    member_count = str(group.members.count())
    if(request.method == "POST"):
        form = InfoMessageValidationForm(request.POST)
        if form.is_valid():
            create_messages_for_infoservice(group, form.cleaned_data['text'])
            
            backurl = reverse('groups_send_message',
                              kwargs= {'group_id': group_id})
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All members of the \"%s\" service" + \
                        " will get your message.") \
                                % group.name
            new_button_label = _("Send another message")
            success = True
            
            return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))

        
    return render_to_response("groups/message_create.html",
                              locals(),
                              context_instance = RequestContext(request))                                           
                                   
@log_request
def register(request, group_id):
    '''
    Register a patient to an information group, i.e.
    a new subscription of the infoservice is created.
    '''
    ajax_url= reverse('web_check_call_received')
    
    # ways_of_communication = get_ways_of_communication(immediate = True)
    ways_of_communication = WayOfCommunication.objects.filter(
                                                enabled = True,
                                                can_send_immediately = True)
    
    if request.method == "POST":
        set_session_variables_for_register(request)
        
        form = NotificationValidationForm2(request.POST)
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
def register_save(request, group_id):
    '''
        Save the subscription of the patient to the information group.
        Display the success message.
    '''
    backurl = reverse('groups_register', 
                      kwargs = {'group_id': group_id})        
    nexturl = reverse('web_index')
    
    subscription = subscription_save(request, group_id)
    
    title = _("Registration successful")
    message = _("The patient will now receive all messages from the "
                        " \"%s\" service.") % subscription.infoservice.name
    new_button_label = _("Register another patient")
    success = True
    
    return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))                               
                                           
    
