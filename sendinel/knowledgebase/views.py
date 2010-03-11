import os, glob

from django.shortcuts import render_to_response
from sendinel.settings import KNOWLEDGEBASE_DIRECTORY
from django.template import RequestContext


def index(request):

    files = os.listdir(KNOWLEDGEBASE_DIRECTORY)
    
    return render_to_response('knowledgebase/index.html',
                              locals(),
                              context_instance=RequestContext(request))
