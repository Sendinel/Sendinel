from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^save/$', 
        'sendinel.notifications.views.save_notification',
        name = 'notifications_save'),
    url(r'^create/(?P<notification_type_name>[a-z]+)/$',
        'sendinel.notifications.views.create_notification',
        name = 'notifications_create'),
    url(r'^send$',
        'sendinel.notifications.views.send_notification_via_bluetooth',
        name = 'notifications_send'),
)
