from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to


urlpatterns = patterns("",
    url(r"^infoservice/register/(?P<id>\d+)/$",
        'sendinel.groups.views.register_infoservice', 
        name = 'web_infoservice_register'),     
    url(r"^infoservice/register/save/(?P<id>\d+)/$",
        'sendinel.groups.views.save_registration_infoservice', 
        name = 'web_infoservice_register_save'),
    # previous staff urls
    url(r"^$", redirect_to, {'url': 'list_groups/'}),
    url(r"^logout/$", 'sendinel.groups.views.logout_staff', name = 'staff_logout'),
    url(r"^list_groups/$", 'sendinel.groups.views.list_groups', 
        name = 'staff_list_groups'),
    url(r"^infoservice/create/$", 'sendinel.groups.views.create_group', 
        name = 'staff_infoservice_create'),
    url(r"^infoservice/delete/$", 'sendinel.groups.views.delete_infoservice', 
        name = 'staff_infoservice_delete'),
    url(r"^infoservice/members/(?P<id>\d+)$", 
        'sendinel.groups.views.list_members_of_infoservice', 
        name = 'staff_infoservice_members'),
    url(r"^infoservice/members/delete/(?P<id>\d+)$", 'sendinel.groups.views.delete_members_of_infoservice', 
        name = 'staff_infoservice_members_delete'),
    url(r"^create_infomessage/(?P<id>\d+)/$", 
        'sendinel.groups.views.create_infomessage', 
        name = 'staff_create_infomessage')
)
