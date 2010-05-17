from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^groups/register/(?P<group_id>\d+)/$",
        'sendinel.groups.views.register', 
        name = 'groups_register'),
    url(r"^groups/register/save/(?P<group_id>\d+)/$",
        'sendinel.groups.views.save_registration_infoservice', 
        name = 'groups_register_save'),   
    url(r"^groups/send_message/(?P<id>\d+)/$", 
        'sendinel.groups.views.send_message', 
        name = 'groups_send_message')
)
