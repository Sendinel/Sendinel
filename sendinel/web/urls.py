from django.conf.urls.defaults import * # patterns, url

urlpatterns = patterns("",
    url(r"^$", 'sendinel.web.views.index', name = 'web_index'),
    url(r'^authenticate_phonenumber/$', 'sendinel.web.views.authenticate_phonenumber',
        name = 'web_authenticate_phonenumber'),
    url(r'^check_call_received/$', 'sendinel.web.views.check_call_received', 
        name = 'web_check_call_received'),
    url(r'^list_devices/$', 'sendinel.web.views.list_bluetooth_devices', 
        name = 'web_list_devices'),
    url(r'^get_devices/$', 'sendinel.web.views.get_bluetooth_devices', 
        name = 'web_get_devices'),
    url(r"^language_choose/$", 'sendinel.web.views.choose_language',
        name = 'choose_language'),
    url(r"^imprint/$", 'sendinel.web.views.imprint', name = 'imprint')
    )
