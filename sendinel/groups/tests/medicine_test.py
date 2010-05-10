
from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.groups.models import InfoService
from sendinel.settings import AUTH

class MedicineTest(TestCase):
    
    fixtures = ['backend_test']
    
    def test_register_patient(self):
        response = self.client.post(
                        reverse('groups_medicine_register_patient'),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012',
                                     'medicine': '3'}) # pk = 3 is a medicine

        self.assertTrue(self.client.session.has_key('way_of_communication'))
        self.assertTrue(self.client.session.has_key \
                                        ('authenticate_phonenumber'))
        self.assertTrue(self.client.session.has_key('medicine'))
        
        if AUTH:
            self.assertEquals(response.status_code, 200)
        else:
            self.assertEquals(response.status_code, 302)

        
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
        
    def test_send_message(self):
        pass
        
    def test_add_medicine(self):
        pass
        