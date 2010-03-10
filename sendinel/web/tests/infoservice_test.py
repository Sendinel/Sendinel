from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from sendinel.backend.models import InfoService

class InfoServiceTest(TestCase):
    def setUp(self):
        self.info = InfoService(name = "testinfoservice")
        self.info.save()
     
    def test_infoservices_on_main_page(self):
        response = self.client.get(reverse('web_index'))
        self.assertContains(response, "Register for Information Services")
        infoservices = InfoService.objects.all()
        for infoservice in infoservices:
            self.assertContains(response, infoservice.name)
            self.assertContains(response, 
                                reverse('web_infoservice_register',
                                         kwargs={'id': infoservice.id}))

        
    def test_register_infoservice(self):
        response = self.client.get(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}))
        self.assertEquals(response.status_code, 200)
        response = self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'number':'01234 / 56789012'})

        self.assertTrue(self.client.session.has_key('way_of_communication'))
        self.assertTrue(self.client.session.has_key('authenticate_phonenumber'))
        self.assertEquals(response.status_code, 200)
      
    def test_save_registration_infoservice(self):
        self.client.get(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}))
        response = self.client.get(reverse('web_authenticate_phonenumber') + \
                              "?next=" + 
                              reverse('web_infoservice_register_save', \
                                      kwargs={'id': self.info.id}))
                                      