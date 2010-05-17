from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^notifications/save/$", 'sendinel.notifications.views.save_appointment',
        name = 'notifications_save'),
    url(r"^notifications/create/(?P<appointment_type_name>[a-z]+)/$",
        'sendinel.notifications.views.create_appointment',
        name = 'notifications_create'),
    url(r"^notifications/send$", 'sendinel.notifications.views.send_appointment',
        name = 'notifications_send'),
)
