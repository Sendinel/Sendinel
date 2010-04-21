from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import Hospital, HospitalAppointment, \
                                    InfoMessage, InfoService,  Patient, \
                                    AppointmentType, ScheduledEvent, \
                                    Subscription
from sendinel.backend.output import VoiceOutputData, SMSOutputData, \
                                    BluetoothOutputData


class SendableTest(TestCase):

    fixtures = ['backend']

    def setUp(self):
        self.sendable = InfoMessage()
        self.sendable.way_of_communication = "sms"
        self.sendable.text = "Test Text"

    def test_sendable_get_data_for_sending(self):
        pass

class HospitalTest(TestCase):
    fixtures = ['backend']
    
    def test_get_hospital_no_hospital(self):
        Hospital.objects.all().delete()
        hospital = Hospital.get_current_hospital()
        self.assertTrue(1, Hospital.objects.all().count())
        self.assertEquals(Hospital.objects.all()[0].name, settings.DEFAULT_HOSPITAL_NAME)
        self.assertEquals(hospital.name, settings.DEFAULT_HOSPITAL_NAME)
    
    def test_get_hospital_with_hospital(self):
        hospital = Hospital.objects.get(current_hospital = True)
        self.assertEquals(Hospital.get_current_hospital(), hospital)

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

    def test_save_with_patient(self):
        patient = Patient(name="Test Person", phone_number="030123456789")
        hospital = self.appointment.hospital
        self.appointment.save_with_patient(patient)
        self.assertEquals(self.appointment.recipient, patient)
        self.assertEquals(self.appointment.hospital, hospital) 
        
    def test_get_data_for_bluetooth(self):
        #create new appointment without saving
        appointment = HospitalAppointment()        
        appointment.date = datetime(2010, 4, 4)
        appointment.appointment_type = AppointmentType.objects.get(pk = 1)
        appointment.bluetooth_mac_address = "00AA11BB22"
                
        output_data = appointment.get_data_for_bluetooth()
        
        self.assertEquals(type(output_data), BluetoothOutputData)
        self.assertEquals(output_data.bluetooth_mac_address, "00AA11BB22")
        self.assertEquals(output_data.server_address, \
                          settings.BLUETOOTH_SERVER_ADDRESS)
        self.assertEquals(type(output_data.data).__name__, "unicode") 
    
    def test_get_data_for_sms(self):
        self.appointment.recipient.phone_number = "012345678"
        output_data = self.appointment.get_data_for_sms()
        
        self.assertEquals(type(output_data), SMSOutputData)
        self.assertEquals(output_data.phone_number, "012345678")
        self.assertEquals(type(output_data.data), unicode)
        
    def test_get_data_for_voice(self):
        self.appointment.recipient.phone_number = "012345678"
        output_data = self.appointment.get_data_for_voice()
        
        self.assertEquals(type(output_data), VoiceOutputData)
        self.assertEquals(output_data.phone_number, "012345678")
        self.assertEquals(type(output_data.data), unicode)
        
class InfoMessageTest(TestCase):
    fixtures = ['backend']
    
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
    
    def test_no_infoservices_with_same_name(self):
        first_infoservice = InfoService(name ="Hospitalinfos")
        first_infoservice.save()
        second_infoservice = InfoService(name ="Hospitalinfos")
        self.assertRaises(IntegrityError, second_infoservice.save)
    
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