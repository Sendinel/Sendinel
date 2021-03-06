from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import Patient, ScheduledEvent
from sendinel.notifications.models import NotificationType, \
                                    Notification
from sendinel.backend.output import VoiceOutputData, \
                                    SMSOutputData, \
                                    BluetoothOutputData



                                    
class NotificationTest(TestCase):
    fixtures = ['backend_test']
    
    def setUp(self):
        self.notification = Notification.objects.get(id = 1)

    def test_create_scheduled_event(self):
        number_of_events = ScheduledEvent.objects.count()
        notification_date = datetime(2010, 02, 24, 13, 43, 59)
        self.notification.date = notification_date
        self.notification.create_scheduled_event()

        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)

        scheduled_event = ScheduledEvent.objects \
                            .order_by('pk').reverse()[:1][0]
        send_time_should = notification_date - \
                            settings.REMINDER_TIME_BEFORE_APPOINTMENT
        self.assertEquals(scheduled_event.send_time,
                            send_time_should)

    def test_save_with_patient(self):
        patient = Patient(name="Test Person", phone_number="030123456789")
        hospital = self.notification.hospital
        self.notification.save_with_patient(patient)
        self.assertEquals(self.notification.recipient, patient)
        self.assertEquals(self.notification.hospital, hospital) 
        
    def test_get_data_for_bluetooth(self):
        #create new notification without saving
        notification = Notification()        
        notification.date = datetime(2010, 4, 4)
        notification.notification_type = NotificationType.objects.get(pk = 1)
        notification.bluetooth_mac_address = "00AA11BB22"
        notification.bluetooth_server_address = "123.456.789.1"
                
        output_data = notification.get_data_for_bluetooth()
        
        self.assertEquals(type(output_data), BluetoothOutputData)
        self.assertEquals(output_data.bluetooth_mac_address, "00AA11BB22")
        self.assertEquals(output_data.server_address, \
                          '123.456.789.1')
        self.assertEquals(type(output_data.data).__name__, "unicode") 
    
    def test_get_data_for_sms(self):
        self.notification.notification_type.template = "This is a template with a $date " + \
            "for the $hospital and a $time and, " + \
            "we use this long template to check if it is reduced before sending it via SMS"
        self.notification.recipient.phone_number = "012345678"
        self.notification.hospital.name = "HospitalnameIsLoooooooooooooooooooooooooong"
        output_data = self.notification.get_data_for_sms()
        
        self.assertEquals(type(output_data), SMSOutputData)
        self.assertEquals(output_data.phone_number, "012345678")
        self.assertEquals(type(output_data.data), unicode)
        
        self.assertTrue(len(output_data.data) <= 160)
        
    def test_get_data_for_voice(self):
        self.notification.notification_type.template = "This is a very long template with a $date " + \
            "for the $hospital and also has a $time and is much longer than 160 characters, " + \
            "we use this long template to check if it is reduced before sending it via SMS"
        self.notification.recipient.phone_number = "012345678"
        output_data = self.notification.get_data_for_voice()
        
        self.assertEquals(type(output_data), VoiceOutputData)
        self.assertEquals(output_data.phone_number, "012345678")
        self.assertEquals(type(output_data.data), unicode)
        
        self.assertTrue(len(output_data.data) > \
            len(self.notification.notification_type.template))
