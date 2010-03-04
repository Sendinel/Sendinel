from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from sendinel.backend.models import Usergroup, ScheduledEvent, InfoMessage
from sendinel.staff.forms import InfoMessageForm

@login_required
def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))
  
@login_required
def create_infomessage(request, id):
       
    if(request.method == "GET"):
        form = InfoMessageForm()
    
        return render_to_response("create_infomessage.html",
                                    locals(),
                                    context_instance = RequestContext(request))
    elif(request.method == "POST"):
        
        info_message = InfoMessage()
        
        info_message.text = request.REQUEST["text"]
        info_message.recipient = Usergroup.objects.filter(pk = id)[0]
        info_message.way_of_communication = "voicecall"

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
            
    return render_to_response("list_infoservices.html",
                                locals(),
                                context_instance = RequestContext(request))