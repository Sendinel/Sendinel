
from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.backend.models import Patient, ScheduledEvent
from sendinel.backend.tests.helper import disable_authentication
from sendinel.infoservices.models import InfoService, Subscription
from sendinel.medicine import views as medicine_views
from sendinel.utils import last

class MedicineTest(TestCase):
    
    fixtures = ['backend_test']
    
    def test_register_save(self):
        subscription_count = Subscription.objects.all().count()

        # pk = 3 is a medicine in fixtures
        self.client.post(reverse('medicine_register'),
                         {"way_of_communication": "sms",
                          "phone_number": "0123456",
                          "medicine": "3"})
                          
        response = self.client.get(
                                reverse('medicine_register_save',
                                kwargs={'medicine_id': '3'}))
                                      
        self.assertEquals(Subscription.objects.all().count(),
                          subscription_count + 1)
        new_subscription = last(Subscription)
        self.assertEquals(new_subscription.patient.phone_number, "0123456")
        self.assertEquals(new_subscription.infoservice.id, 3)
        self.assertEquals(new_subscription.way_of_communication, "sms")    
    
    @disable_authentication
    def test_register(self):
        redirection_path = reverse('medicine_register_save',
                                         kwargs={'medicine_id': '3'})

        response = self.client.post(
                        reverse('medicine_register'),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012',
                                     'medicine': '3'}) # pk = 3 is a medicine

        self.assertTrue(self.client.session.has_key('way_of_communication'))
        self.assertTrue(self.client.session.has_key('medicine'))
        self.assertTrue(self.client.session.has_key \
                                        ('authenticate_phonenumber'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, redirection_path)
       
                                 
        
    def test_create_register_form(self):
        response = self.client.get(reverse('medicine_register'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="way_of_communication"')
        self.assertContains(response, 'name="medicine"')
        return response    
        
    def test_medicine_in_register_form(self):
        response = self.client.get(reverse('medicine_register'))
        medicines = InfoService.objects.all().filter(type="medicine")
        for medicine in medicines:
            self.assertContains(response, unicode(medicine))
        
    def test_send_message_form(self):
        response = self.client.get(reverse('medicine_send_message'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="medicine"')
        self.assertContains(response, 'textarea')
    
    def test_send_message(self):
        a_medicine = InfoService(name='Malarone', type='medicine')
        a_medicine.save()
        subscription = Subscription(patient = Patient.objects.all()[0],
                                way_of_communication = "sms",
                                infoservice = a_medicine)
        subscription.save()
        subscription = Subscription(patient = Patient.objects.all()[1],
                                way_of_communication = "sms",
                                infoservice = a_medicine)
        subscription.save()
        info_service_count = InfoService.objects.all().count()
        members_count = a_medicine.members.count()
        scheduled_events_count = ScheduledEvent.objects.all().count()
        a_text = 'Hello, the medicine Malarone is now available at your ' + \
                 'clinic. Please come and pick it up.'
        response = self.client.post(reverse('medicine_send_message'),
                                     { 'medicine': a_medicine.pk, 
                                       'text': a_text })
                                       
        self.assertEquals(InfoService.objects.all().count() +  1, 
                          info_service_count)
        self.assertEquals(ScheduledEvent.objects.all().count(),
                          scheduled_events_count + members_count)
        self.assertTemplateUsed(response, 'web/status_message.html')
        self.assertTemplateNotUsed(response, 'medicine/message_create.html')