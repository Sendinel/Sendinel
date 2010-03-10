import copy
from datetime import datetime, timedelta

from django.test import TestCase

from sendinel.backend.models import AuthenticationCall
from sendinel.web import views


class AuthenticateViewTests(TestCase):
    
    urls = "web.urls"

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
        response = self.client.get("/authenticate_phonenumber/")
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="number"')
        
        response = self.client.post("/authenticate_phonenumber/", 
                                    {'number':'01234 / 56789012'})

        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name,
                          "web/authenticate_phonenumber_call.html")
        self.assertContains(response, "auth.js")
        self.assertContains(response, "<noscript>")
        
        session_data = self.client.session['authenticate_phonenumber']
        self.assertEquals(session_data['number'], "0123456789012")
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
        AuthenticationCall.objects.all().delete()
        
        self.client.post("/authenticate_phonenumber/", 
                        {'number':'01234 / 56789012'})

        response = self.client.post("/check_call_received/")

        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "waiting")
        
        AuthenticationCall(number = "0123456789012").save()
        
        response = self.client.post("/check_call_received/")
            
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "received")
        
        # make sure timeout is over
        real_timeout = views.AUTHENTICATION_CALL_TIMEOUT
        views.AUTHENTICATION_CALL_TIMEOUT = timedelta(minutes = -1)

        response = self.client.post("/check_call_received/")  
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "failed")      
        
        views.AUTHENTICATION_CALL_TIMEOUT = real_timeout
        


