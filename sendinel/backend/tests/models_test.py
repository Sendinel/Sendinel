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

