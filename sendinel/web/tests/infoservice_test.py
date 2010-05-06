from django.test import TestCase
from django.core.urlresolvers import reverse
from sendinel.backend.models import InfoService, Subscription, Patient
from sendinel.settings import AUTH
from sendinel.utils import last

class WebInfoServiceTest(TestCase):
    def setUp(self):
        self.info = InfoService(name = "testinfoservice")
        self.info.save()
        self.patient = Patient(name="eu",phone_number = "01234")
        self.patient.save()
        self.subscription = Subscription(infoservice = self.info, 
                                         way_of_communication = "sms", 
                                         patient = self.patient)
        self.subscription.save()
     
    def create_register_infoservice_form(self):
        response = self.client.get(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="way_of_communication"')
        return response
        
    def test_infoservices_on_main_page(self):
        response = self.client.get(reverse('web_index'))

        infoservices = InfoService.objects.all()
        for infoservice in infoservices:
            self.assertContains(response, infoservice.name)
            self.assertContains(response, 
                                reverse('web_infoservice_register',
                                         kwargs={'id': infoservice.id}))

        
    def test_register_infoservice(self):
        self.create_register_infoservice_form()
        response = self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012'})

        self.assertTrue(self.client.session.has_key('way_of_communication'))
        self.assertTrue(self.client.session.has_key('authenticate_phonenumber'))
        
        if AUTH:
            self.assertEquals(response.status_code, 200)
        else:
            self.assertEquals(response.status_code, 302)
      
    def test_register_infoservice_submit_validations(self):
        response = self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012'})
        self.assertEquals(response.status_code, 302)
            
        response = self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'0123afffg789012'})
        self.assertContains(response, 'Please enter numbers only')

        response = self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'234 / 56789012'})
        self.assertContains(response, 'Please enter a cell phone number.')
        
    def test_save_registration_infoservice(self):
        subscription_count = Subscription.objects.all().count()

        self.client.post(reverse('web_infoservice_register',
                         kwargs={'id': self.info.id}),
                         {"way_of_communication": "sms",
                          "phone_number": "0123456"})
                          
        response = self.client.get(reverse('web_infoservice_register_save',
                                   kwargs={'id': self.info.id}))
                          
                                      
        self.assertEquals(Subscription.objects.all().count(),
                          subscription_count + 1)
        new_subscription = last(Subscription)
        self.assertEquals(new_subscription.patient.phone_number, "0123456")
        self.assertEquals(new_subscription.infoservice, self.info)
        self.assertEquals(new_subscription.way_of_communication, "sms")
        

    
    def test_remove_subscription(self):
        subscription_count = Subscription.objects.all().count()
        
        self.subscription.delete()
                            
        self.assertEquals(Subscription.objects.all().count(), 
                          subscription_count - 1)
        self.assertTrue(Subscription.objects.filter(pk = self.info.id).count() == 0)
            