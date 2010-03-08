from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from sendinel.backend.models import Usergroup, ScheduledEvent, InfoMessage, \
                                    Subscription
from sendinel.staff.forms import InfoMessageForm

@login_required
def index(request):
    return render_to_response('staff/index.html',
                              context_instance=RequestContext(request))
  
@login_required
def create_infomessage(request, id):
       
    if(request.method == "GET"):
        form = InfoMessageForm()
    
        return render_to_response("staff/create_infomessage.html",
                                    locals(),
                                    context_instance = RequestContext(request))
    elif(request.method == "POST"):
        
        group = Usergroup.objects.filter(pk = id)[0]
        
        for patient in group.members.all():
        
            info_message = InfoMessage()
        
            info_message.text = request.POST["text"]
            
            subscription = Subscription.objects.filter(patient = patient,
                                                       usergroup = group)[0]
            
            info_message.recipient = patient
            info_message.way_of_communication = subscription.way_of_communication

            info_message.save()        
            info_message.create_scheduled_event(datetime.now())
        
        return HttpResponseRedirect(reverse("staff_list_infoservices"))

    
@login_required
def list_infoservices(request):

    all_groups = Usergroup.objects.all()

    groups = []
    
    for group in all_groups:
        groups.append({
            "id": group.id,
            "name": group.name, 
            "count_members": group.members.all().count()
        })
            
    return render_to_response("staff/list_infoservices.html",
                                locals(),
                                context_instance = RequestContext(request))