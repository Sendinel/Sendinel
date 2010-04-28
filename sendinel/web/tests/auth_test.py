import copy
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.backend.models import AuthenticationCall, AppointmentType
from sendinel.web import views


class AuthenticateViewTests(TestCase):
    fixtures = ['backend_test']
    urls = "urls"

    def test_authenticate_phonenumber_messages(self):
        # infoservice = Infoservice(name="tesstinfoservice")
        # infoservice.save()
        # self.client.post(reverse('web_authenticate_phonenumber') +"?next=" + 
                                 # reverse('web_infoservice_register', \
                                          # kwargs={'id': infoservice.id})),
            # {infoservice_text = "You want to register " + \
                                # "for" + str(infoservice)})
        # self.assertContains(r
        # infoservice.delete()
        pass
        
    def test_authenticate_phonenumber(self):
        
        appointment_type = AppointmentType.objects.get(pk=1)
        
        self.client.get(reverse('web_appointment_create', \
                kwargs={"appointment_type_name": appointment_type.name })) 
        data = {'date': '2012-08-12',
                'phone_number': '01733685224',
                'way_of_communication': 'sms'}
        self.client.post(reverse('web_appointment_create', \
                kwargs = {"appointment_type_name": appointment_type.name }), data)
     
        response = self.client.post(reverse("web_authenticate_phonenumber"))

        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name,
                          "web/authenticate_phonenumber_call.html")
        self.assertContains(response, "auth.js")
        self.assertContains(response, "<noscript>")
        
        session_data = self.client.session['authenticate_phonenumber']
        self.assertEquals(session_data['number'], "01733685224")
        self.assertTrue(isinstance(session_data['start_time'], datetime))

        # TODO check delete_timed_out_authentication_calls gets called

        # TODO implement Form validation
        # response = self.client.post("/authenticate_phonenumber/",
        #     {
        #         'number' : 'abcdfef',
        #         'name' : ''
        #     })                   
        # 
        # self.failUnlessEqual(response.status_code, 200)
        # 
        # self.assertContains(response, 'name="name"')
        
    def test_check_call_received(self):
        # make sure there are no AuthenticationCall objects in the db
        print "Pending: web/auth_test.py test_check_call_received"
        # AuthenticationCall.objects.all().delete()
        # 
        # self.client.post("/web/authenticate_phonenumber/", 
        #                 {'number':'01234 / 56789012'})
        # 
        # response = self.client.post("/web/check_call_received/")
        # 
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "waiting")
        # 
        # AuthenticationCall(number = "0123456789012").save()
        # 
        # response = self.client.post("/web/check_call_received/")
        #     
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "received")
        # 
        # # make sure timeout is over
        # real_timeout = views.AUTHENTICATION_CALL_TIMEOUT
        # views.AUTHENTICATION_CALL_TIMEOUT = timedelta(minutes = -1)
        # 
        # response = self.client.post("/web/check_call_received/")  
        # 
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "failed")      
        # 
        # views.AUTHENTICATION_CALL_TIMEOUT = real_timeout
        


