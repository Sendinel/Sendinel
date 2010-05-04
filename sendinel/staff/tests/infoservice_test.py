from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from sendinel.backend.models import ScheduledEvent, InfoService, InfoMessage, \
                                    Subscription, Patient, Subscription

class StaffInfoServiceTest(TestCase):
    
    client = Client()
    
    fixtures = ['backend_test']
    
    def setUp(self):
        User.objects.create_user('john', 'l@example.com', 'passwd')
        self.client.login(username='john', password="passwd")
    
    def test_create_infomessage(self):
    
        counter = ScheduledEvent.objects.all().count()
        infoservice = InfoService.objects.filter(pk = 1)[0]
    
        response = self.client.post(reverse("staff_create_infomessage",
            kwargs={"id":1}), {
            "text" : "This is a testmessage",
            "date" : "2010-01-01 00:00:00"
        })
                
        self.assertEquals(response.status_code, 200)
        
        offset = infoservice.members.all().count()
        
        self.assertEquals(ScheduledEvent.objects.all().count(), 
                          counter + offset)
        
        for message in InfoMessage.objects.all():
            subscription = Subscription.objects.filter(
                                            patient = message.recipient,
                                            infoservice = infoservice)[0]
            
            self.assertEquals(message.way_of_communication,
                              subscription.way_of_communication)                  
                              
    def test_create_infoservice(self):
        response = self.client.get(reverse("staff_infoservice_create"))
        self.assertContains(response, 'name="name"')
        response = self.client.post(reverse("staff_infoservice_create"), 
                                {"name" : "This is a name for an infoservice"})
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse("staff_list_infoservices"))
        self.assertContains(response, "This is a name for an infoservice")
        
    def test_manage_infoservice_groups(self):
        info = InfoService(name = "testgroup")
        info.save()
        patient = Patient(phone_number = "012345")
        patient.save()
        subscription = Subscription(infoservice = info, 
                                    patient = patient,
                                    way_of_communication = "voice")
        subscription.save()
        response = self.client.get(reverse("staff_list_infoservices"))
        self.assertContains(response, "Group members")
        response = self.client.get(reverse("staff_infoservice_members", 
                                           kwargs={"id": info.id}))
        self.assertContains(response, patient.phone_number)
        
        
    def test_delete_members_of_infoservice(self):
        infoservice = InfoService.objects.filter(pk = 1)[0]
        patient = infoservice.members.all()[0]
        subscription = Subscription.objects.get(patient=patient, infoservice=infoservice)
        response = self.client.post(reverse("staff_infoservice_members_delete",
                                            kwargs={"id" : infoservice.id}),
                                    {'subscription_id' : subscription.id})
        new_members = infoservice.members.all()
        self.assertTrue(not patient in new_members)
        self.assertTrue(not subscription in Subscription.objects.all())
        self.assertRedirects(response, reverse("staff_infoservice_members", 
                                               kwargs={"id": infoservice.id}))
            
        
        