from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.infoservices.models import InfoService, Subscription
from sendinel.groups.forms import InfoserviceValidationForm
from sendinel.logger import logger, log_request

@log_request
def index(request, infoservice_type):
    infoservices = InfoService.objects.all().filter(type = infoservice_type)
    infoservice_textblocks = InfoService.TYPE_TEXTS[infoservice_type]

    backurl = reverse("web_index")
    
    return render_to_response("infoservices/index.html",
                                locals(),
                                context_instance = RequestContext(request))
                                
@log_request
def create_infoservice(request, infoservice_type):

    infoservice_textblocks = InfoService.TYPE_TEXTS[infoservice_type]

    if request.method == "POST":
        form = InfoserviceValidationForm(request.POST)
    
        if form.is_valid():
    
            infoservice = InfoService(name = request.POST["name"],
                                      type = infoservice_type)
            infoservice.save()
            
            logger.info("Created InfoService: %s", str(infoservice))
            
            nexturl = reverse('infoservices_index', 
                              kwargs={'infoservice_type': infoservice_type})
            backurl = reverse('infoservices_create', 
                              kwargs={'infoservice_type': infoservice_type})
            title = _("Creation successful")
            message = _("The \"%(infoservice_name)s\" " + \
                        "%(infoservice_type)s has been created.") \
                        % {'infoservice_name': infoservice.name,
                           'infoservice_type': infoservice_textblocks["name"]}
            new_button_label = _("Create another %(infoservice_type)s") \
                            % {'infoservice_type': infoservice_textblocks['name']}
            success = True
            
            return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))    
        
    return render_to_response("infoservices/create.html",
                                locals(),
                                context_instance = RequestContext(request))
                                
@log_request
def delete_infoservice(request):
    if request.method == 'POST' and request.POST.has_key('group_id'):
        infoservice = get_object_or_404(InfoService, 
                                        pk = request.POST['group_id'])
                                        
        infoservice_type = infoservice.type
        infoservice.delete()
        
        return HttpResponseRedirect(reverse("infoservices_index", 
                                    kwargs={'infoservice_type': infoservice_type}))
                                    
    return HttpResponseRedirect(reverse("web_index"))   
    

@log_request
def list_members_of_infoservice(request, id):   
    infoservice = get_object_or_404(InfoService, pk = id)
    
    infoservice_textblocks = InfoService.TYPE_TEXTS[infoservice.type]
    
    subscriptions = Subscription.objects.filter(infoservice = id)
    return render_to_response("infoservices/subscriptions.html",
                                locals(),
                                context_instance = RequestContext(request))
                                
@log_request
def delete_members_of_infoservice(request, id):
    if request.method == "POST" and request.POST.has_key('subscription_id'):
        subscription = Subscription.objects.get(
                                        id = request.POST["subscription_id"])        
        subscription.delete()
        
    return HttpResponseRedirect(reverse("infoservices_members", 
                                   kwargs={"id": id}))                                