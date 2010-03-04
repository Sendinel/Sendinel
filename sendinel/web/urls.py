from django.conf.urls.defaults import *
from sendinel.web.views import *

urlpatterns = patterns("",
    url(r"^$", 'sendinel.web.views.index', name = 'index'),
    url(r"^create_appointment/$", 'sendinel.web.views.create_appointment',
        name = 'create_appointment'),
    url(r'^inputText/$', 'sendinel.web.views.input_text', name = 'input_text'),
    url(r'^chooseCommunication/$', 'sendinel.web.views.choose_communication',
        name = 'choose_communication'),
    url(r'^authenticate_phonenumber/$', 'sendinel.web.views.authenticate_phonenumber',
        name = 'authenticate_phonenumber'),
    url(r'^check_call_received/$', 'sendinel.web.views.check_call_received', 
        name = 'check_call_received'),
    url(r'^list_devices/$', 'sendinel.web.views.list_bluetooth_devices', 
        name = 'list_devices'),
    url(r'^get_devices/$', 'sendinel.web.views.get_bluetooth_devices', 
        name = 'get_devices')
        
    )