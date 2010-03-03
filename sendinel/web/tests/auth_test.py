import copy
from datetime import datetime

from django.test import TestCase 
from django.test.client import Client

from sendinel.backend.models import AuthenticationCall
import sendinel.web.views 


class AuthenticateViewTests(TestCase):
    
    urls = "web.urls"

    def test_authenticate_phonenumber(self):
        response = self.client.get("/authenticate_phonenumber/")
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="number"')
        self.assertContains(response, 'name="name"')

        
        response = self.client.post("/authenticate_phonenumber/", {
                'number':'01234 / 56789012',
                'name' : 'Homer Simpson'})

        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name,
                          "authenticate_phonenumber_call.html")
        self.assertContains(response, "auth.js")
        self.assertContains(response, "<noscript>")

        # sessions seem not to work with django 1.2 beta1 TestClient.
        # see - seems to be the same problem
        # http://groups.google.com/group/django-users/browse_thread/thread/9ba607ca6bee2b7e/0c1e4d73a0996caf?lnk=raot
        
        # session_data = self.client.session['authenticate_phonenumber']
        # self.assertEquals(session_data['number'], "0123456789012")
        # self.assertEquals(session_data['name'], "Homer Simpson")
        # self.assertTrue(isinstance(session_data['start_time'], datetime))

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
        pass
        # TODO
        # cannot be tested since sessions seem not to work with TestClient
        # see test_authenticate_phonenumber
        
        # AuthenticationCall.objects.all().delete()
        # 
        # self.client.post("/authenticate_phonenumber", {
        #         'number':'01234 / 56789012',
        #         'name' : 'Homer Simpson'})
        # 
        # response = self.client.post("/check_call_received/")
        #         
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "waiting")
        # 
        # AuthenticationCall(number = "0123456789012").save()
        # 
        # response = self.client.post("/check_call_received/")
        #     
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "received")
        # 
        # self.client.session['authenticate_phonenumber']['start_time'] = \
        #                                                         datetime(2007)
        # 
        # response = self.client.post("/check_call_received/")  
        #     
        # self.failUnlessEqual(response.status_code, 200)
        # self.assertContains(response, "failed")      
        
        def test_delete_timed_out_authentication_calls():
            AuthenticationCall(number = '023444', time = datetime(2007)).save()
            AuthenticationCall(number = '033233', time = datetime(3000)).save()
            delete_timed_out_authentication_calls()
            
            self.assertEquals(1, AuthenticationCall.objects.all().count())
            
           
            