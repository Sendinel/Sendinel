from django.conf.urls.defaults import *
from sendinel.web.views import *

urlpatterns = patterns("",
    url(r"^$", 'sendinel.web.views.index', name = 'web_index'),
    url(r"^appointment/save/$", 'sendinel.web.views.save_appointment',
        name = 'web_appointment_save'),
    url(r"^appointment/create/$", 'sendinel.web.views.create_appointment',
        name = 'web_appointment_create'),        
    url(r'^inputText/$', 'sendinel.web.views.input_text', name = 'input_text'),
    url(r'^chooseCommunication/$', 'sendinel.web.views.choose_communication',
        name = 'web_choose_communication'),
    url(r'^authenticate_phonenumber/$', 'sendinel.web.views.authenticate_phonenumber',
        name = 'web_authenticate_phonenumber'),
    url(r'^check_call_received/$', 'sendinel.web.views.check_call_received', 
        name = 'web_check_call_received'),
    url(r'^list_devices/$', 'sendinel.web.views.list_bluetooth_devices', 
        name = 'web_list_devices'),
    url(r"^appointment/send$", 'sendinel.web.views.send_appointment',
        name = 'web_appointment_send'),        
    url(r'^get_devices/$', 'sendinel.web.views.get_bluetooth_devices', 
        name = 'web_get_devices')
        
    )