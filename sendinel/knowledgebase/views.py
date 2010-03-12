import os
from copy import copy

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from sendinel.settings import KNOWLEDGEBASE_DIRECTORY, \
                              MEDIA_URL
from sendinel.logger import logger



def index(request):
    files = os.listdir(KNOWLEDGEBASE_DIRECTORY)
    for file in copy(files):
        if file.startswith('.') or file.endswith('.db'): files.remove(file)
        
    files = dict(zip(range(0,(len(files))), files))
    request.session['numbered_files'] = files
    
    return render_to_response('knowledgebase/index.html',
                              locals(),
                              context_instance=RequestContext(request))

def show(request, file_id):

    file_id = int(file_id)
    numbered_files = request.session['numbered_files']
    file_name = numbered_files[file_id].lower()
    
    if (len(numbered_files)-1 > file_id):
        nexturl = reverse('knowledgebase_show', kwargs={'file_id':(file_id+1)})
        
    backurl = reverse('knowledgebase_index')
    if (file_id > 0):
        backurl = reverse('knowledgebase_show', kwargs={'file_id':(file_id-1)})
    
    
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
        path_name = MEDIA_URL + "knowledgebase/" + file_name
        return render_to_response('knowledgebase/show_jpg.html',
                              locals(),
                              context_instance=RequestContext(request))
                              
    elif file_name.endswith('.flv'):
        path_name = MEDIA_URL + "knowledgebase/" + file_name
        return render_to_response('knowledgebase/show_video.html',
                              locals(),
                              context_instance=RequestContext(request))
                              
    elif file_name.endswith('.txt'):
        path_name = KNOWLEDGEBASE_DIRECTORY + '/' + file_name
        
        try:
            text = open(path_name).read()
            text = text.encode('latin-1')
        except:
            logger.error('Could not open file' + file_name)
        
        return render_to_response('knowledgebase/show_txt.html',
                              locals(),
                              context_instance=RequestContext(request))    
    