from django.test import TestCase 
from django.test.client import Client

import sendinel.web.views 
import copy

class AuthenticateViewTests(TestCase):
    
    urls = "web.urls"
    
    def setUp(self):
        self.client = Client()
            
    def test_authenticate_phonenumber(self):
        response = self.client.get("/authenticate_phonenumber/")
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="number"')
        self.assertContains(response, 'name="name"')
        
        response = self.client.post("/authenticate_phonenumber",
            {
                'number':'01234 / 56789012',
                'name' : 'Homer Simpson'
            })
            
        self.failUnlessEqual(response.status_code, 301)
                
        response = self.client.post("/authenticate_phonenumber/",
            {
                'number' : 'abcdfef',
                'name' : ''
            })                   
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="number"')
        self.assertContains(response, 'name="name"')
        
    def test_check_call_received(self):
        check_log_save = sendinel.web.views.AuthHelper.check_log
        
        def return_true(self, number):
            return True
        
        sendinel.web.views.AuthHelper.check_log = return_true

        response = self.client.post("/check_call_received/",
            {
                'number':'0123456789012'
            })
                
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "received")
        
        def return_false(self, number):
            return False
        
        sendinel.web.views.AuthHelper.check_log = return_false
        
        response = self.client.post("/check_call_received/",
            {
                'number':'0123456789012'
            })
            
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "waiting")
        
        def exception_raiser(self):
            raise Exception
        
        sendinel.web.views.AuthHelper.check_log = exception_raiser
        
        response = self.client.post("/check_call_received/",
            {
                'number':'0123456789012'
            })  
            
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "failed")      

        sendinel.web.views.AuthHelper.check_log = check_log_save
        
        