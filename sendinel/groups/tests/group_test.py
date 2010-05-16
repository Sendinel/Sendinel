from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from sendinel.backend.models import ScheduledEvent, Patient
# from sendinel.backend.tests.helper import disable_authentication
from sendinel.groups.models import InfoService, InfoMessage, Subscription
from sendinel.groups import views as groups_views
from sendinel.utils import last


class StaffInfoServiceTest(TestCase):
    
    client = Client()
    
    fixtures = ['backend_test']
    
    def setUp(self):
        User.objects.create_user('john', 'l@example.com', 'passwd')
        self.client.login(username='john', password="passwd")
    
    
    def test_create_infomessage_get(self):
        response = self.client.get(reverse("staff_create_infomessage",
                                   kwargs={"id":1}))
        self.assertEquals(response.status_code, 200)
                                    
    
    def test_create_infomessage_post(self):
    
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
    
    def create_group(self, group_type, title, field_title):
        response = self.client.get(reverse("groups_create",
                                    kwargs={'group_type': group_type}))
        
        self.assertContains(response, 'name="name"')
        self.assertContains(response, title)
        self.assertContains(response, field_title)
        
        response = self.client.post(reverse("groups_create",
                                    kwargs={'group_type': group_type}), 
                                {"name" : "This is a name for a group"})
        
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "This is a name for a group")
        self.assertContains(response, title)
        
        response = self.client.get(reverse("groups_index",
                                    kwargs={'group_type': group_type}))
                                    
        self.assertContains(response, "This is a name for a group")
        self.assertContains(response, title)
           
    def test_create_information_group(self):
        self.create_group('information', 
                     'information group', 
                     "Inform patients about")
    
    def text_create_medicine_group(self):                 
        self.create_group('medicine', 
                     'waiting list for medicine',
                     'The patients are waiting for the following medicine:')
    
    def manage_groups(self, group_type, table_head, member_button, 
                      remove_button, remove_patient_button, group_name):
        info = InfoService(name = "testgroup", type = group_type)
        info.save()
        
        patient = Patient(phone_number = "012345")
        patient.save()
        
        subscription = Subscription(infoservice = info, 
                                    patient = patient,
                                    way_of_communication = "voice")
        subscription.save()
        
        response = self.client.get(reverse("groups_index",
                                    kwargs = {'group_type': group_type}))
        self.assertContains(response, member_button)
        self.assertContains(response, remove_button)
        self.assertContains(response, table_head)
        
        response = self.client.get(reverse("staff_infoservice_members", 
                                                   kwargs={"id": info.id,
                                                   }))
                                                           
        self.assertContains(response, patient.phone_number)
        self.assertContains(response, remove_patient_button)
        self.assertContains(response, group_name)
        
    def test_manage_information_groups(self):
        self.manage_groups("information", 
                           "Information", 
                           "Group members",
                           "Remove group",
                           "Remove patient from group",
                           "information group")
    
    def test_manage_medicine_groups(self):
        self.manage_groups("medicine", 
                           "Medicine", 
                           "List members",
                           "Remove list",
                           "Remove patient from list",
                           "waiting list for medicine")
    
    def delete_members_of_group(self, group_type):
        infoservice = InfoService.objects.filter(type = group_type)[0]
        subscription_count = Subscription.objects.all().count()
        patient = infoservice.members.all()[0]
        subscription = Subscription.objects.get(patient=patient, 
                                            infoservice=infoservice)
                                            
        response = self.client.post(reverse("staff_infoservice_members_delete",
                                            kwargs={"id" : infoservice.id}),
                                    {'subscription_id' : subscription.id})
                                    
        self.assertTrue(not patient in infoservice.members.all())
        self.assertTrue(not subscription in Subscription.objects.all())
        self.assertEquals(subscription_count - 1, 
                            Subscription.objects.all().count())
        self.assertRedirects(response, reverse("staff_infoservice_members",
                                               kwargs={"id": infoservice.id}))
        
    def test_delete_members_of_infoservice(self):
        self.delete_members_of_group('information')
        self.delete_members_of_group('medicine')
                                               
    def test_delete_infoservice(self):
        infoservices_count = InfoService.objects.all().count()
        infoservice = InfoService.objects.get(id = 1)
        response = self.client.post(reverse("staff_infoservice_delete"), 
                                    {'infoservice_id' : infoservice.id})
        self.assertTrue(not infoservice in InfoService.objects.all())
        self.assertEquals(infoservices_count - 1, 
                            InfoService.objects.all().count())
        self.assertRedirects(response, reverse("groups_index",
                                        kwargs={'group_type': 'information'}))


class WebInfoServiceTest(TestCase):
    
    fixtures = ['backend_test']
    

    def setUp(self):
        self.info = InfoService(name = "testinfoservice", type="information")
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
            if infoservice.type == "information":
                self.assertContains(response, infoservice.name)
                self.assertContains(response, 
                                reverse('web_infoservice_register',
                                         kwargs={'id': infoservice.id}))
            else:
                self.assertNotContains(response, infoservice.name)

    # @disable_authentication
    # def test_register_infoservice(self):
    #     redirection_path = reverse('web_infoservice_register_save', \
    #                                 kwargs = {'id': self.info.id})
    # 
    #     self.create_register_infoservice_form()
    #     response = self.client.post(reverse('web_infoservice_register', 
    #                                 kwargs={'id': self.info.id}),
    #                                 {'way_of_communication': 'sms',
    #                                  'phone_number':'01234 / 56789012'})
    # 
    #     self.assertTrue(self.client.session.has_key('way_of_communication'))
    #     self.assertTrue(self.client.session.has_key('authenticate_phonenumber'))
    #     
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, redirection_path)
    #     return response
    #     
    # 
    # @disable_authentication
    # def test_register_infoservice_submit_validations(self):
    #    
    #     response = self.client.post(reverse('web_infoservice_register', 
    #                                 kwargs={'id': self.info.id}),
    #                                 {'way_of_communication': 'sms',
    #                                  'phone_number':'01234 / 56789012'})
    # 
    #     self.assertEquals(response.status_code, 302)
    # 
    #     response = self.client.post(reverse('web_infoservice_register', 
    #                                 kwargs={'id': self.info.id}),
    #                                 {'way_of_communication': 'sms',
    #                                  'phone_number':'0123afffg789012'})
    #     self.assertContains(response, 'Please enter numbers only')
    # 
    #     response = self.client.post(reverse('web_infoservice_register', 
    #                                 kwargs={'id': self.info.id}),
    #                                 {'way_of_communication': 'sms',
    #                                  'phone_number':'234 / 56789012'})
    #     self.assertContains(response, 'Please enter a cell phone number.')
    #     
    #     


        
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