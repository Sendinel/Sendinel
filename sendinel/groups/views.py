

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

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
                               render_status_success

@log_request
def send_message(request, id):
    group = get_object_or_404(InfoService, pk = id)
    if(request.method == "POST"):
        form = InfoMessageValidationForm(request.POST)
        if form.is_valid():
            create_messages_for_infoservice(group, form.cleaned_data['text'])
            
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All members of the \"%s\" service" + \
                        " will get your message.") \
                                % group.name
            return render_status_success(request, title, message, nexturl = nexturl)

        
    return render_to_response("groups/message_create.html",
                              locals(),
                              context_instance = RequestContext(request))                                           
                                   
@log_request
def register(request, group_id):
    ajax_url= reverse('web_check_call_received')
    
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
def save_registration_infoservice(request, group_id):
    backurl = reverse('groups_register', 
                      kwargs = {'group_id': group_id})        
    nexturl = reverse('web_index')
    
    subscription = subscription_save(request, group_id)
    
    title = _("Registration successful")
    message = _("The patient will now receive all messages from the "
                        " \"%s\" service.") % subscription.infoservice.name
    
    return render_status_success(request, title, message, 
                                 backurl = backurl, nexturl = nexturl)                                
                                           
    