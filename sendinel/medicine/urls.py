from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("",
    url(r"^medicine/register/$",
        'sendinel.medicine.views.register_patient', 
        name = 'medicine_register_patient'),     
   
    url(r'^medicine/register/save/(?P<id>\d+)/$',
        'sendinel.medicine.views.register_patient_save',
        name = 'medicine_register_patient_save'),
    url(r'^medicine/send-message/$',
        'sendinel.medicine.views.send_message',
        name = 'medicine_send_message')
)