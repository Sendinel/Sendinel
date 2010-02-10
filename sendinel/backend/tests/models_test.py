from sendinel.backend.models import *
from sendinel.backend.output import *
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.core import serializers

data = open("backend/fixtures/contenttype.yaml").read()
deserialized = serializers.deserialize("yaml", data)
object_dict = dict([[object.object.model, object.object.id] for object in deserialized if isinstance(object.object, ContentType)])

counter = 1000

def set_content_type_id(sender, **kwargs):
    content_type = kwargs.get('instance')
    new_id = object_dict.get(content_type.model, None)
    if new_id:
        content_type.pk = object_dict[content_type.model]
    else:
        global counter
        content_type.pk = counter
        counter += 1
pre_save.connect(set_content_type_id, sender=ContentType)


class ModelsTest(TestCase):
    """
    """
    fixtures = ['backend']

    def setUp(self):
        self.event = ScheduledEvent.objects.get(pk=1)
    
    def test_sendable_polymorphic(self):
        appointment = self.event.sendable
        self.assertEquals(type(appointment), HospitalAppointment, 'Sendable polymorphic type is wrong')

    def test_sendable_polymorphic_method(self):
        appointment = self.event.sendable
        appointment.way_of_communication="sms"
        data = OutputData()
        appointment.get_data_for_sms = lambda: data
        self.assertEquals(appointment.get_data_for_sending(), object)
        
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
        

