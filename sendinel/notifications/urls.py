from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^save/$', 
        'sendinel.notifications.views.save_appointment',
        name = 'notifications_save'),
    url(r'^create/(?P<appointment_type_name>[a-z]+)/$',
        'sendinel.notifications.views.create_appointment',
        name = 'notifications_create'),
    url(r'^send$',
        'sendinel.notifications.views.send_appointment_via_bluetooth',
        name = 'notifications_send'),
)
