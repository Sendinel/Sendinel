from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("",
    url(r"^medicines/register/$",
        'sendinel.medicines.views.register', 
        name = 'medicines_register'),     
    url(r'^/medicines/register/save/(?P<medicine_id>\d+)/$',
        'sendinel.medicines.views.register_save',
        name = 'medicines_register_save'),
    url(r'^medicines/send-message/$',
        'sendinel.medicines.views.send_message',
        name = 'medicines_send_message')
)