from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^$", 'sendinel.knowledgebase.views.index', name = 'knowledgebase_index'),
    url(r"^show/(?P<file_id>\d+)/$", 'sendinel.knowledgebase.views.show', 
         name = 'knowledgebase_show')
    
    )