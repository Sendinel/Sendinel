from copy import deepcopy

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.backend.models import Patient
from sendinel.groups.models import InfoService, InfoMessage, Subscription
from sendinel.groups.forms import InfoserviceValidationForm, \
                                  InfoMessageValidationForm, \
                                  NotificationValidationForm2
from sendinel.logger import logger, log_request
from sendinel.settings import AUTH, AUTH_NUMBER
from sendinel.web.views import fill_authentication_session_variable, \
                               render_status_success


@log_request                              
def logout_staff(request):
    logout(request)
    
    logger.info("logged out staff member")
    
    return HttpResponseRedirect(reverse("web_index"))

@log_request
def create_infomessage(request, id):
    if(request.method == "POST"):
        form = InfoMessageValidationForm(request.POST)
        
        if form.is_valid():
            infoservice = get_object_or_404(InfoService, pk = id)
            create_messages_for_group(infoservice, form.cleaned_data['text'])
            
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All members of the \"%s\" service" + \
                        " will get your message.") \
                                % infoservice.name
            
            render_status_success(request, title, message, nexturl = nexturl)

        
    return render_to_response("groups/message_create.html",
                              locals(),
                              context_instance = RequestContext(request))

@log_request
def index(request, group_type):
    groups = InfoService.objects.all().filter(type = group_type)
    group_textblocks = InfoService.TYPE_TEXTS[group_type]

    backurl = reverse("web_index")
    
    return render_to_response("groups/index.html",
                                locals(),
                                context_instance = RequestContext(request))

@log_request
def create_group(request, group_type):

    group_textblocks = InfoService.TYPE_TEXTS[group_type]

    if request.method == "POST":
    
        data = deepcopy(request.POST)        
        form = InfoserviceValidationForm(data)
    
        if form.is_valid():
    
            infoservice = InfoService(name = request.POST["name"],
                                      type = group_type)
            infoservice.save()
            
            logger.info("Created InfoService: %s", str(infoservice))
            
            nexturl = reverse('groups_index', kwargs={'group_type': group_type})
            backurl = reverse('groups_create', kwargs={'group_type': group_type})
                        
            success = True
            title = _("Creation successful")
            message = _("The \"%(group_name)s\" %(group_type)s has been created.") \
                        % {'group_name': infoservice.name,
                           'group_type': group_textblocks["name"]}
    
            return render_to_response('web/status_message.html', 
                                      locals(),
                                      context_instance = RequestContext(request))
        
    return render_to_response("groups/create.html",
                                locals(),
                                context_instance = RequestContext(request))
                                
@log_request
def delete_infoservice(request):
    if request.method == 'POST' and request.POST.has_key('infoservice_id'):
        infoservice = get_object_or_404(InfoService, 
                                        pk = request.POST['infoservice_id'])
                                        
        group_type = infoservice.type
        infoservice.delete()
        
        return HttpResponseRedirect(reverse("groups_index", 
                                    kwargs={'group_type': group_type}))
                                    
    return HttpResponseRedirect(reverse("web_index"))   
        

@log_request
def list_members_of_infoservice(request, id):   
    group = get_object_or_404(InfoService, pk = id)
    
    group_textblocks = InfoService.TYPE_TEXTS[group.type]
    
    subscriptions = Subscription.objects.filter(infoservice = id)
    return render_to_response("groups/subscriptions.html",
                                locals(),
                                context_instance = RequestContext(request))

@log_request
def delete_members_of_infoservice(request, id):
    
    if request.method == "POST" and request.POST.has_key('subscription_id'):
        
        subscription = Subscription.objects.get(
                                        id = request.POST["subscription_id"])        
        subscription.delete()
        
    return HttpResponseRedirect(reverse("staff_infoservice_members", 
                                   kwargs={"id": id}))  

def set_session_variables_for_register(request):
    request.session['way_of_communication'] = \
                                    request.POST['way_of_communication']
    patient = Patient()
    patient.phone_number = request.POST['phone_number']
    request.session['patient'] = patient                                   
                                   
@log_request
def register_infoservice(request, id):
    ajax_url= reverse('web_check_call_received')
    
    if request.method == "POST":
        set_session_variables_for_register(request)
            
        data = deepcopy(request.POST)
        form = NotificationValidationForm2(data)
        if form.is_valid():
            number = fill_authentication_session_variable(request) 
            auth_number = AUTH_NUMBER
            backurl = reverse('web_index')        

            if AUTH:
                return HttpResponseRedirect(
                        reverse('web_authenticate_phonenumber') \
                        + "?next=" + reverse('web_infoservice_register_save', \
                        kwargs = {'id': id}))
                
            return HttpResponseRedirect(
                reverse('web_infoservice_register_save', kwargs = {'id': id}))
        else:
            logger.info("register_infoservice: Invalid form.")
       
    infoservice = InfoService.objects.filter(pk = id)[0].name
    backurl = reverse("web_index")
    
    return render_to_response('groups/register.html', 
                              locals(),
                              context_instance = RequestContext(request))

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
                              
@log_request
def save_registration_infoservice(request, id):
    backurl = reverse('web_infoservice_register',  kwargs = {'id': id})        
    nexturl = reverse('web_index')
    
    subscription = subscription_save(request, id)
    
    success = True
    title = _("Registration successful")
    message = _("The patient will now receive all messages from the "
                        " \"%s\" service.") % subscription.infoservice.name
    
    return render_to_response('web/status_message.html', 
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
    