from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.backend.models import InfoService, InfoMessage, \
                                    Subscription, Patient

from sendinel.staff.forms import InfoMessageForm
from sendinel.logger import logger, log_request


@log_request
def index(request):
    return render_to_response('staff/index.html',
                              context_instance=RequestContext(request))

@log_request                              
def logout_staff(request):
    logout(request)
    
    logger.info("logged out staff member")
    
    return HttpResponseRedirect(reverse("web_index"))

@log_request
def create_infomessage(request, id):
    infoservice = InfoService.objects.filter(pk = id)[0]
    
    if(request.method == "GET"):
          
        return render_to_response("staff/create_infomessage.html",
                                    locals(),
                                    context_instance = RequestContext(request))
    elif(request.method == "POST"):
        
        for patient in infoservice.members.all():
        
            info_message = InfoMessage()
        
            info_message.text = request.POST["text"]
            
            subscription = Subscription.objects.filter(patient = patient,
                                                infoservice = infoservice)[0]
            
            info_message.recipient = patient
            info_message.send_time = datetime.now()
            info_message.way_of_communication = \
                            subscription.way_of_communication

            info_message.save()        
            info_message.create_scheduled_event(datetime.now())
            
            logger.info("Created %s", str(info_message))
        
        nexturl = reverse('web_index')
        
        success = True
        title = _("Message created")
        message = _("All members of the %s service will get your message.") \
                            % infoservice.name
    
        return render_to_response('web/status_message.html', 
                                  locals(),
                                  context_instance = RequestContext(request))

@log_request
def list_infoservices(request):

    all_infoservices = InfoService.objects.all()

    infoservices = []
    
    for infoservice in all_infoservices:
        infoservices.append({
            "id": infoservice.id,
            "name": infoservice.name, 
            "count_members": infoservice.members.all().count()
        })
            
    return render_to_response("staff/list_infoservices.html",
                                locals(),
                                context_instance = RequestContext(request))

@log_request
def create_infoservice(request):
    if request.method == "POST":
        infoservice = InfoService(name = request.POST["name"])
        infoservice.save()
        
        logger.info("Created InfoService: %s", str(infoservice))
        
        nexturl = reverse('staff_list_infoservices')
        
        success = True
        title = _("Creation successful")
        message = _("The %s service has been created.") % infoservice.name
    
        return render_to_response('web/status_message.html', 
                                  locals(),
                                  context_instance = RequestContext(request))
        
    return render_to_response("staff/infoservice_create.html",
                                locals(),
                                context_instance = RequestContext(request))
                                
@log_request
def delete_infoservice(request):
    if request.method == 'POST' and request.POST.has_key('infoservice_id'):
        infoservice = InfoService.objects.get(id = request.POST['infoservice_id'])
        infoservice.delete()
    return HttpResponseRedirect(reverse("staff_list_infoservices"))   
        

@log_request
def list_members_of_infoservice(request, id):   
    infoservice = InfoService.objects.filter(pk = id)[0]
    subscriptions = Subscription.objects.filter(infoservice = id)
    return render_to_response("staff/infoservice_members.html",
                                locals(),
                                context_instance = RequestContext(request))

@log_request
def delete_members_of_infoservice(request, id):
    
    if request.method == "POST" and request.POST.has_key('subscription_id'):
        
        subscription = Subscription.objects.get(id = request.POST["subscription_id"])        
        subscription.delete()
        
    return HttpResponseRedirect(reverse("staff_infoservice_members", 
                                   kwargs={"id": id}))  
