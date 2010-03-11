import os
from copy import copy

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.settings import KNOWLEDGEBASE_DIRECTORY, \
                              MEDIA_URL
from sendinel.logger import logger



def index(request):
    files = os.listdir(KNOWLEDGEBASE_DIRECTORY)
    for file in copy(files):
        if file.startswith('.'): files.remove(file)
        
    files = dict(zip(range(0,(len(files))), files))
    request.session['numbered_files'] = files
    
    return render_to_response('knowledgebase/index.html',
                              locals(),
                              context_instance=RequestContext(request))

def show(request, file_id):

    file_name = request.session['numbered_files'][int(file_id)]
    
    
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
        path_name = MEDIA_URL + "knowledgebase/" + file_name
        return render_to_response('knowledgebase/show_jpg.html',
                              locals(),
                              context_instance=RequestContext(request))
    elif file_name.endswith('.flv'):
        return render_to_response('knowledgebase/show_video.html',
                              locals(),
                              context_instance=RequestContext(request))
    elif file_name.endswith('.txt'):
        path_name = KNOWLEDGEBASE_DIRECTORY + '/' + file_name
        
        try:
            text = open(path_name).read()
        except:
            logger.error('Could not open file' + file_name)
        
        return render_to_response('knowledgebase/show_txt.html',
                              locals(),
                              context_instance=RequestContext(request))    
    