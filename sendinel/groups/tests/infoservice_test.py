from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from sendinel.backend.models import ScheduledEvent, Patient
from sendinel.groups.models import InfoService, InfoMessage, Subscription
from sendinel.groups import views as groups_views
from sendinel.settings import AUTH
from sendinel.utils import last


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
        subscription_count = Subscription.objects.all().count()
        patient = infoservice.members.all()[0]
        subscription = Subscription.objects.get(patient=patient, infoservice=infoservice)
        response = self.client.post(reverse("staff_infoservice_members_delete",
                                            kwargs={"id" : infoservice.id}),
                                    {'subscription_id' : subscription.id})
        self.assertTrue(not patient in infoservice.members.all())
        self.assertTrue(not subscription in Subscription.objects.all())
        self.assertEquals(subscription_count - 1, Subscription.objects.all().count())
        self.assertRedirects(response, reverse("staff_infoservice_members", 
                                               kwargs={"id": infoservice.id}))
                                               
    def test_delete_infoservice(self):
        infoservices_count = InfoService.objects.all().count()
        infoservice = InfoService.objects.get(id = 1)
        response = self.client.post(reverse("staff_infoservice_delete"), 
                                    {'infoservice_id' : infoservice.id})
        self.assertTrue(not infoservice in InfoService.objects.all())
        self.assertEquals(infoservices_count - 1, InfoService.objects.all().count())
        self.assertRedirects(response, reverse("staff_list_infoservices"))               
        
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
    
    def register_infoservice_validations(self):
        return self.client.post(reverse('web_infoservice_register', 
                                    kwargs={'id': self.info.id}),
                                    {'way_of_communication': 'sms',
                                     'phone_number':'01234 / 56789012'})

    def test_register_infoservice_submit_validations(self):
        # disable authentication
        original_value = groups_views.AUTH
        groups_views.AUTH = False
        
        response = self.register_infoservice_validations()

        self.assertEquals(response.status_code, 302)
        
        groups_views.AUTH = True
        
        response = self.register_infoservice_validations()
        self.assertEquals(response.status_code, 200)
        
        # restore AUTH value
        groups_views.AUTH = original_value
        
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

        