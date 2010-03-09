from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import messages
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
        i = messages.get_messages(response.request)
        #import pdb; pdb.set_trace()
       # self.assert
        self.assertRedirects(response, 
                            reverse('web_authenticate_phonenumber') + \
                             "?next=" + 
                             reverse('web_infoservice_register', \
                                     kwargs={'id': self.info.id}))