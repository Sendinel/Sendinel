from django.conf.urls.defaults import patterns, url



urlpatterns = patterns("",
    url(r"^(?P<infoservice_type>\w+)/$", 'sendinel.infoservices.views.index',
        name = 'infoservices_index'),
    url(r"^(?P<infoservice_type>\w+)/create/$", 
        'sendinel.infoservices.views.create_infoservice', 
        name = 'infoservices_create'),        
    url(r"^infoservices/delete/$", 
        'sendinel.infoservices.views.delete_infoservice', 
        name = 'infoservices_delete'),
    url(r"^infoservice/members/(?P<id>\d+)$", 
        'sendinel.infoservices.views.list_members_of_infoservice', 
        name = 'infoservices_members'),        
    url(r"^infoservice/members/delete/(?P<id>\d+)$", 
        'sendinel.infoservices.views.delete_members_of_infoservice', 
        name = 'infoservices_members_delete')        
)