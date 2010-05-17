from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("",
    url(r"^medicines/register/$",
        'sendinel.medicine.views.register', 
        name = 'medicines_register'),     
    url(r'^/medicines/register/save/(?P<medicine_id>\d+)/$',
        'sendinel.medicine.views.register_save',
        name = 'medicines_register_save'),
    url(r'^medicines/send-message/$',
        'sendinel.medicine.views.send_message',
        name = 'medicines_send_message')
)