from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from sendinel.backend.models import ScheduledEvent, InfoService, InfoMessage, \
                                    Subscription

class InfoserviceTest(TestCase):
    
    client = Client()
    
    fixtures = ['backend']
    
    def setUp(self):
        user = User.objects.create_user('john', 'l@example.com', 'passwd')
        self.client.login(username='john', password="passwd")
    
    def test_create_infomessage(self):
    
        counter = ScheduledEvent.objects.all().count()
        infoservice = InfoService.objects.filter(pk = 1)[0]
    
        response = self.client.post(reverse("staff_create_infomessage",
            kwargs={"id":1}), {
            "text" : "This is a testmessage",
            "date" : "2010-01-01 00:00:00"
        })
                
        self.assertRedirects(response, reverse("staff_list_infoservices"))
        
        offset = infoservice.members.all().count()
        
        self.assertEquals(ScheduledEvent.objects.all().count(), 
                          counter + offset)
        
        for message in InfoMessage.objects.all():
            subscription = Subscription.objects.filter(
                                            patient = message.recipient,
                                            infoservice = infoservice)[0]
            
            self.assertEquals(message.way_of_communication,
                              subscription.way_of_communication)                  
        