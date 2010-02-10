from sendinel.backend.models import *
from sendinel.backend.output import *
import sendinel.backend.tests.contenttype_helper
from django.test import TestCase


class ModelsTest(TestCase):
    """
    """
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
        
class HospitalAppointmentTest(TestCase):
    """
    Test for the HospitalAppointment class which derives from Sendable.
    """
    
    def setUp(self):
        self.appointment = HospitalAppointment()
        self.appointment.recipient = Patient()
        self.appointment.hospital = Hospital()
        self.appointment.doctor = Doctor()
    
    # def test_save_without_all_attributes(self):
        # self.appointment.save
        
    def test_get_data_for_sms(self):
        self.appointment.recipient.phone_number = 12345
        data = self.appointment.get_data_for_sms()
        self.assertEquals(data.phone_number, 12345)
        self.assertTrue(type(data)== string)
        
        
class TextMessageTest(TestCase):
    """
    Test for the TextMessage class which derives from Sendable.
    """
    
    def setUp(self):
        self.message = TextMessage()
        self.message.recipient = Patient()
    
    # def test_save_without_all_attributes(self):
        # self.appointment.save
        
    def test_get_data_for_sms(self):
        self.message.recipient.phone_number = 12345
        data = self.message.get_data_for_sms()
        self.assertEquals(data.phone_number, 12345)
        self.assertTrue(type(data)== String)


