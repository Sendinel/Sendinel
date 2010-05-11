
from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.groups.models import InfoService, Subscription
from sendinel.groups import views as groups_views
from sendinel.utils import last

class MedicineTest(TestCase):
    
    fixtures = ['backend_test']
    
    def test_register_patient_save(self):
        subscription_count = Subscription.objects.all().count()

        # pk = 3 is a medicine in fixtures
        self.client.post(reverse('groups_medicine_register_patient'),
                         {"way_of_communication": "sms",
                          "phone_number": "0123456",
                          "medicine": "3"})
                          
        response = self.client.get(reverse('groups_medicine_register_patient_save',
                                   kwargs={'id': '3'}))
                                      
        self.assertEquals(Subscription.objects.all().count(),
                          subscription_count + 1)
        new_subscription = last(Subscription)
        self.assertEquals(new_subscription.patient.phone_number, "0123456")
        self.assertEquals(new_subscription.infoservice.id, 3)
        self.assertEquals(new_subscription.way_of_communication, "sms")    
    
    def test_register_patient(self):
        # disable authentication
        original_value = groups_views.AUTH
        groups_views.AUTH = False
        
        redirection_path = reverse('groups_medicine_register_patient_save',
                                         kwargs={'id': '3'})
        self.register_patient_with_assertions(redirection_path)
        
        # enable authentication
        groups_views.AUTH = True
        
        redirection_path = reverse('web_authenticate_phonenumber') \
                    + "?next=" + \
                    reverse('groups_medicine_register_patient_save', \
                    kwargs={'id': '3'})
        self.register_patient_with_assertions( redirection_path)
        
        # restore authentication to original value
        groups_views.AUTH = original_value
        
        
    def register_patient_with_assertions(self,redirection_path): 
        response = self.client.post(
                        reverse('groups_medicine_register_patient'),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012',
                                     'medicine': '3'}) # pk = 3 is a medicine

        self.assertTrue(self.client.session.has_key('way_of_communication'))
        self.assertTrue(self.client.session.has_key('medicine'))
        self.assertTrue(self.client.session.has_key \
                                        ('authenticate_phonenumber'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, redirection_path)
       
                                 
        
    def test_create_register_patient_form(self):
        response = self.client.get(reverse('groups_medicine_register_patient'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="way_of_communication"')
        self.assertContains(response, 'name="medicine"')
        return response    
        
    def test_medicine_in_register_patient_form(self):
        response = self.client.get(reverse('groups_medicine_register_patient'))
        medicines = InfoService.objects.all().filter(type="medicine")
        for medicine in medicines:
            self.assertContains(response, unicode(medicine))
        
    def test_send_message_form(self):
        response = self.client.get(reverse('groups_medicine_send_message'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="medicine"')
        self.assertContains(response, 'textarea')
        
        
    def test_add_medicine(self):
        pass
        