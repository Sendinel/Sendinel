from django.conf.urls.defaults import patterns, url



urlpatterns = patterns("",
    url(r"^infoservice/register/(?P<id>\d+)/$",
        'sendinel.groups.views.register_infoservice', 
        name = 'web_infoservice_register'),     
    
    url(r"^infoservice/register/save/(?P<id>\d+)/$",
        'sendinel.groups.views.save_registration_infoservice', 
        name = 'web_infoservice_register_save'),
    # previous staff urls
   
    url(r"^logout/$", 'sendinel.groups.views.logout_staff', name = 'staff_logout'),
   
    url(r"^(?P<group_type>\w+)/$", 'sendinel.groups.views.index',
        name = 'groups_index'),
   
    url(r"^(?P<group_type>\w+)/create/$", 'sendinel.groups.views.create_group', 
        name = 'groups_create'),
   
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
