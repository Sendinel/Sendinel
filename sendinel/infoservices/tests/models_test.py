from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import Patient, \
                                    WayOfCommunication, \
                                    get_woc
from sendinel.infoservices.models import InfoMessage, InfoService, Subscription
from sendinel.backend.output import VoiceOutputData, SMSOutputData



class InfoMessageTest(TestCase):
    fixtures = ['backend_test']
    
    def setUp(self):
        self.info_message = InfoMessage.objects.get(pk = 1)
    
    def test_get_data_for_sms(self):
        self.info_message.recipient.phone_number = "012345678"        
        info_output = self.info_message.get_data_for_sms()

        self.assertEquals(type(info_output), SMSOutputData)
        self.assertEquals(info_output.phone_number, "012345678")
        self.assertEquals(type(info_output.data), unicode)
        
    def test_get_data_for_voice(self):
        self.info_message.recipient.phone_number = "012345678"
        output_data = self.info_message.get_data_for_voice()
        
        self.assertEquals(type(output_data), VoiceOutputData)
        self.assertEquals(output_data.phone_number, "012345678")
        self.assertEquals(type(output_data.data), unicode)
        
        
class InfoServiceModelTest(TestCase):
    def setUp(self):
        self.infoservice = InfoService(name = "Gruppe", type="information")
        self.infoservice.save()
        self.patient = Patient()
        self.patient.save()
    
    def test_no_infoservices_with_same_name(self):
        first_infoservice = InfoService(name ="Hospitalinfos", type="information")
        first_infoservice.save()
        second_infoservice = InfoService(name ="Hospitalinfos", type="information")
        self.assertRaises(IntegrityError, second_infoservice.save)
        
    def test_no_infoservices_with_no_name(self):
        self.assertRaises(IntegrityError, InfoService(name = None).save)  
        self.assertRaises(IntegrityError, InfoService().save)          
        
    def test_no_infoservices_with_empty_type(self):
        an_infoservice = InfoService(name = "Hospitalinfos")
        self.assertRaises(IntegrityError, an_infoservice.save)

class SubscriptionTest(TestCase):
    
    fixtures = ["backend_test"]
    
    def setUp(self):
        self.woc = get_woc("sms")
    
        self.infoservice = InfoService(name = "Gruppe", 
                                       type = "information")
        self.infoservice.save()
        self.patient = Patient()
        self.patient.save()
        self.subscription = Subscription(patient = self.patient, 
                                         infoservice = self.infoservice,
                                         way_of_communication = self.woc)
        self.subscription.save()
        
    def test_infoservice_member_relation_add(self):
        self.assertTrue(self.patient in self.infoservice.members.all())

    def test_infoservice_member_relation_delete(self):
        self.subscription.delete()
        self.assertTrue(self.patient not in self.infoservice.members.all())
        
    def test_subscription_creation(self):
        subscription = Subscription()        
        
        self.assertRaises(IntegrityError, subscription.save)
        
        infoservice = InfoService(name = "information", type="information")
        infoservice.save()
        
        subscription.patient = self.patient
        subscription.infoservice = infoservice
        subscription.way_of_communication = self.woc
        
        subscription.save()
        
        self.assertEquals(self.infoservice.members.all().count(), 1)
        self.assertEquals(self.infoservice.members.all()[0], self.patient)
        self.assertTrue(subscription in Subscription.objects.all())
