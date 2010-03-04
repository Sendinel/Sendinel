from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import *
from sendinel.backend.output import *


class ScheduledEventTest(TestCase):

    fixtures = ['backend']

    def setUp(self):
        self.event = ScheduledEvent.objects.get(pk=1)
    
    def test_sendable_polymorphic(self):
        appointment = self.event.sendable
        self.assertEquals(type(appointment),
                            HospitalAppointment,
                            'Sendable polymorphic type is wrong')

    def test_sendable_get_data_for_sending(self):
        appointment = self.event.sendable
        appointment.way_of_communication="sms"
        data = OutputData()
        appointment.get_data_for_sms = lambda: data
        self.assertEquals(appointment.get_data_for_sending(), data)
        

class HospitalAppointmentTest(TestCase):
    fixtures = ['backend']
    
    def setUp(self):
      self.appointment = HospitalAppointment.objects.get(pk = 1)

    def test_create_scheduled_event(self):
        number_of_events = ScheduledEvent.objects.count()
        appointment_date = datetime(2010, 02, 24, 13, 43, 59)
        self.appointment.date = appointment_date
        self.appointment.create_scheduled_event()

        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)

        scheduled_event = ScheduledEvent.objects \
                            .order_by('pk').reverse()[:1][0]
        send_time_should = appointment_date - \
                            settings.REMINDER_TIME_BEFORE_APPOINTMENT
        self.assertEquals(scheduled_event.send_time,
                            send_time_should)
                            
    def test_save_with_patient_no_hospital(self):
        Hospital.objects.all().delete()
        try:
            self.appointment.hospital
            self.fail()
        except Hospital.DoesNotExist:
            pass
        patient = Patient(name="Test Person", phone_number="030123456789")
        self.appointment.save_with_patient(patient)
        self.assertTrue(1, Hospital.objects.all().count())
        self.assertEquals(Hospital.objects.all()[0].name, settings.DEFAULT_HOSPITAL_NAME)
        self.assertEquals(self.appointment.hospital.name, settings.DEFAULT_HOSPITAL_NAME)

    def test_save_with_patient_with_hospital(self):
        patient = Patient(name="Test Person", phone_number="030123456789")
        hospital = self.appointment.hospital
        self.appointment.save_with_patient(patient)
        self.assertEquals(self.appointment.recipient, patient)
        self.assertEquals(self.appointment.hospital, hospital)
        
class ModelsSMSTest(TestCase):
    
    fixtures = ['backend']
    
    def test_hospital_appointment_get_data_for_sms(self):
        smsoutputdata1 = SMSOutputData()
        smsoutputdata1.phone_number = "01234"
        data = HospitalAppointment.objects.get(pk = 1).get_data_for_sms()
        entry = data[0]
        
        self.assertEquals(len(data), 1)
        self.assertEquals(type(entry), SMSOutputData)
        self.assertEquals(entry.phone_number, "01234")
        self.assertEquals(type(entry.data), unicode)
        
    def test_text_message_get_data_for_sms(self):
        numbers = ["01234", "09876"]
        data = InfoMessage.objects.get(pk = 1).get_data_for_sms()
        
        self.assertTrue(len(data) >= 1)
        for entry in data:
            self.assertEquals(type(entry), SMSOutputData)
            self.assertTrue(entry.phone_number in numbers)
            self.assertEquals(type(entry.data), unicode)
            
        
class ModelsUsergroupTest(TestCase):
    def setUp(self):
        self.group = Usergroup(name = "Gruppe")
        self.group.save()
        self.patient = Patient()
        self.patient.save()
        self.group.members.add(self.patient)
    
    def test_no_groups_with_same_name(self):
        first_group = Usergroup(name ="Hospitalinfos")
        first_group.save()
        second_group = Usergroup(name ="Hospitalinfos")
        self.assertRaises(IntegrityError, second_group.save)
    
    #TODO bei Form testen, dass keine Nullwerte angegeben werden duerfen
    # def test_no_groups_with_empty_name(self):
        # self.assertRaises(IntegrityError, Usergroup(name = None).save)
        # amount = Usergroup.objects.all().count()
        # first_group = Usergroup()
        # import pdb; pdb.set_trace()
        # first_group.save()
        # print first_group.__str__
        # self.assertEquals(Usergroup.objects.all().count(), amount) 
        
    def test_group_member_relation_add(self):
        self.assertTrue(self.patient in self.group.members.all())
        self.assertTrue(self.group in self.patient.groups())

    def test_group_member_relation_delete(self):
        self.group.members.remove(self.patient)
        self.assertTrue(self.patient not in self.group.members.all())
        self.assertTrue(self.group not in self.patient.groups())

