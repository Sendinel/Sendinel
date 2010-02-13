from django.conf.urls.defaults import *
from sendinel.web.views import *

urlpatterns = patterns("",
    url(r"^$", 'sendinel.web.views.index', name = 'index'),
    url(r"^create_appointment/$", 'sendinel.web.views.create_appointment',
        name = 'create_appointment'),
    url(r'^inputText/$', 'sendinel.web.views.input_text', name = 'input_text'),
    url(r'^chooseCommunication/$', 'sendinel.web.views.choose_communication',
        name = 'choose_communication')
    )