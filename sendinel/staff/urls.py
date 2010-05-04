from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^$", 'sendinel.staff.views.index', name = 'staff_index'),
    url(r"^logout/$", 'sendinel.staff.views.logout_staff', name = 'staff_logout'),
    url(r"^list_infoservices/$", 'sendinel.staff.views.list_infoservices', 
        name = 'staff_list_infoservices'),
    url(r"^infoservice/create/$", 'sendinel.staff.views.create_infoservice', 
        name = 'staff_infoservice_create'),
    url(r"^infoservice/members/(?P<id>\d+)$", 
        'sendinel.staff.views.list_members_of_infoservice', 
        name = 'staff_infoservice_members'),
    url(r"^infoservice/members/delete/(?P<id>\d+)$", 'sendinel.staff.views.delete_members_of_infoservice', 
        name = 'staff_infoservice_members_delete'),
    url(r"^create_infomessage/(?P<id>\d+)/$", 
        'sendinel.staff.views.create_infomessage', 
        name = 'staff_create_infomessage')
    )