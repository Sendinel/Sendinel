from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("",
    url(r"^register/$",
        'sendinel.medicine.views.register', 
        name = 'medicine_register'),     
    url(r'^register/save/(?P<medicine_id>\d+)/$',
        'sendinel.medicine.views.register_save',
        name = 'medicine_register_save'),
    url(r'^send-message/$',
        'sendinel.medicine.views.send_message',
        name = 'medicine_send_message')
)