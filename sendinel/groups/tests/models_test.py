from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import Patient
from sendinel.groups.models import InfoMessage, InfoService, Subscription
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
        self.infoservice = InfoService(name = "Gruppe")
        self.infoservice.save()
        self.patient = Patient()
        self.patient.save()
    
    def test_no_infoservices_with_same_or_empty_name(self):
        first_infoservice = InfoService(name ="Hospitalinfos")
        first_infoservice.save()
        second_infoservice = InfoService(name ="Hospitalinfos")
        self.assertRaises(IntegrityError, second_infoservice.save)
        self.assertRaises(IntegrityError, InfoService(name = None).save)        

class SubscriptionTest(TestCase):
    
    def setUp(self):
        self.infoservice = InfoService(name = "Gruppe")
        self.infoservice.save()
        self.patient = Patient()
        self.patient.save()
        self.subscription = Subscription(patient = self.patient, 
                                         infoservice = self.infoservice)
        self.subscription.save()
        
    def test_infoservice_member_relation_add(self):
        self.assertTrue(self.patient in self.infoservice.members.all())
        self.assertTrue(self.infoservice in self.patient.infoservices())

    def test_infoservice_member_relation_delete(self):
        self.subscription.delete()
        self.assertTrue(self.patient not in self.infoservice.members.all())
        self.assertTrue(self.infoservice not in self.patient.infoservices())
        
    def test_subscription_creation(self):
        subscription = Subscription()        
        
        self.assertRaises(IntegrityError, subscription.save)
        
        infoservice = InfoService(name = "Group")
        infoservice.save()
        
        subscription.patient = self.patient
        subscription.infoservice = infoservice
        
        subscription.save()
        
        self.assertEquals(self.infoservice.members.all().count(), 1)
        self.assertEquals(self.infoservice.members.all()[0], self.patient)
        self.assertTrue(self.infoservice in self.patient.infoservices())
        self.assertTrue(subscription in Subscription.objects.all())
