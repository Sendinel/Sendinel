from django.test import TestCase

from sendinel.backend.models import *
from sendinel.backend.output import *
import sendinel.backend.tests.contenttype_helper


class ModelsTest(TestCase):

    fixtures = ['backend']

    def setUp(self):
        self.event = ScheduledEvent.objects.get(pk=1)
    
    def test_sendable_polymorphic(self):
        appointment = self.event.sendable
        self.assertEquals(type(appointment), HospitalAppointment, 'Sendable polymorphic type is wrong')

    def test_sendable_get_data_for_sending(self):
        appointment = self.event.sendable
        appointment.way_of_communication="sms"
        data = OutputData()
        appointment.get_data_for_sms = lambda: data
        self.assertEquals(appointment.get_data_for_sending(), data)
        

      

class ModelsSMSTest(TestCase):
    
    fixtures = ['backend']
    
    def test_hospital_appointment_get_data_for_sms(self):
        data = HospitalAppointment.objects.get( pk = 2).get_data_for_sms()
        self.assertions_for_sms_output_object(data)
        
    def test_text_message_get_data_for_sms(self):
        data = TextMessage.objects.get(pk = 1).get_data_for_sms()
        self.assertions_for_sms_output_object(data)
        
    def assertions_for_sms_output_object(self, data):
        self.assertEquals(type(data), SMSOutputData)
        self.assertEquals(data.phone_number, "12345")
        self.assertEquals(type(data.data), unicode)



        
        


