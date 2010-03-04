from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from sendinel.backend.models import Usergroup

@login_required
def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))
  
@login_required
def create_infomessage(request):
    pass
    
@login_required
def list_infoservices(request):

    groups = Usergroup.objects.all()

    return render_to_response("list_infoservices.html",
                                locals(),
                                context_instance = RequestContext(request))