from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import *
from sendinel.backend.output import *


class SendableTest(TestCase):

    fixtures = ['backend']

    def setUp(self):
        self.sendable = InfoMessage()
        self.sendable.way_of_communication = "sms"
        self.sendable.text = "Test Text"

    def test_sendable_get_data_for_sending(self):
        pass
        

class HospitalAppointmentTest(TestCase):
    fixtures = ['backend']
    
    def setUp(self):
      self.appointment = HospitalAppointment.objects.get(id = 1)

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
        
        self.assertEquals(Hospital.objects.all()[0].name, 
                          settings.DEFAULT_HOSPITAL_NAME)
                          
        self.assertEquals(self.appointment.hospital.name, 
                          settings.DEFAULT_HOSPITAL_NAME)

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
        smsoutputdata1.phone_number = "01621785295"
        appointment = HospitalAppointment.objects.get(pk = 1).get_data_for_sms()
        
        self.assertEquals(type(appointment), SMSOutputData)
        self.assertEquals(appointment.phone_number, "01621785295")
        self.assertEquals(type(appointment.data), unicode)
        
    def test_info_message_get_data_for_sms(self):
        number = u"01621785295"
        info_output = InfoMessage.objects.get(pk = 1).get_data_for_sms()
        recipient = InfoMessage.objects.get(pk = 1).recipient

        self.assertEquals(type(info_output), SMSOutputData)
        self.assertEquals(info_output.phone_number, recipient.phone_number)
        self.assertEquals(type(info_output.data), unicode)
            
        
class ModelsUsergroupTest(TestCase):
    def setUp(self):
        self.group = Usergroup(name = "Gruppe")
        self.group.save()
        self.patient = Patient()
        self.patient.save()
    
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
        

class SubscriptionTest(TestCase):
    
    def setUp(self):
        self.group = Usergroup(name = "Gruppe")
        self.group.save()
        self.patient = Patient()
        self.patient.save()
        self.subscription = Subscription(patient = self.patient, 
                                         usergroup = self.group)
        self.subscription.save()
        
    def test_group_member_relation_add(self):
        self.assertTrue(self.patient in self.group.members.all())
        self.assertTrue(self.group in self.patient.groups())

    def test_group_member_relation_delete(self):
        self.subscription.delete()
        self.assertTrue(self.patient not in self.group.members.all())
        self.assertTrue(self.group not in self.patient.groups())
        
    def test_subscription_creation(self):
        subscription = Subscription()        
        
        self.assertRaises(IntegrityError, subscription.save)
        
        usergroup = Usergroup(name = "Group")
        usergroup.save()
        
        subscription.patient = self.patient
        subscription.usergroup = usergroup
        
        subscription.save()
        
        self.assertEquals(self.group.members.all().count(), 1)
        self.assertEquals(self.group.members.all()[0], self.patient)
        self.assertTrue(self.group in self.patient.groups())