from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^appointment/save/$", 'sendinel.notifications.views.save_appointment',
        name = 'web_appointment_save'),
    url(r"^appointment/create/(?P<appointment_type_name>[a-z]+)/$",
        'sendinel.notifications.views.create_appointment',
        name = 'web_appointment_create'),
    url(r"^appointment/send$", 'sendinel.notifications.views.send_appointment',
        name = 'web_appointment_send'),
)
