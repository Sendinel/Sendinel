from django.test import TestCase
from datetime import datetime, timedelta

from sendinel.backend.models import ScheduledEvent, Patient
from sendinel.infoservices.models import InfoMessage
from sendinel.backend import output, scheduler

class SchedulerTest(TestCase):    
    
    counter = 0
    fixtures = ['backend_test']
    
    def test_scheduler(self):     
        
        def scheduled_events_count(state = 'new'):
            
            return scheduler.get_all_due_events().count()
            
        def send(data):
            SchedulerTest.counter += 1
        
        sms_send_old = output.SMSOutputData.send
        bluetooth_send_old = output.BluetoothOutputData.send
        voice_send_old = output.VoiceOutputData.send
        
        output.SMSOutputData.send = send
        output.BluetoothOutputData.send = send
        output.VoiceOutputData.send = send
        
        SchedulerTest.counter = 0
        self.assertTrue(scheduled_events_count() > 0)
                
        scheduler.run(run_only_one_time = True)
        
        # assert that all scheduled events have been processed by send()
        # as defined in fixtures there is one usergroup with 2 members and
        # one single patient
        self.assertEquals(1, SchedulerTest.counter)
        # assert that no events with state new exist anymore
        self.assertEquals(scheduled_events_count(), 0)
        
        output.SMSOutputData.send = sms_send_old
        output.BluetoothOutputData.send = bluetooth_send_old
        output.VoiceOutputData.send = voice_send_old

    def test_spool_file_parsing(self):
        class MockFile:
            """
                This class represents a mocked file object
                It defaults to an untouched Asterisk spool file
            """
            counter = 0
            fake_data = """Channel: Local/2000
WaitTime: 2
RetryTime: 5
MaxRetries: 8000
Data: datacard0,0123456,This is a Test
Archive: true
"""
            def readline(input):
                try:
                    data = MockFile.fake_data.splitlines()[MockFile.counter]
                except:
                    return None 
                MockFile.counter += 1
                return data
        real_open = scheduler.openFile
        fake_open = lambda filename: MockFile()
        scheduler.openFile = fake_open
        filename = "testspoolfile"

        status = scheduler.get_spoolfile_status(filename)
        self.assertEquals(status, "Queued")

        MockFile.counter = 0

        MockFile.fake_data = """Channel: Local/2000
WaitTime: 2
RetryTime: 5
MaxRetries: 8000
Data: datacard0,0123456,This is a Test
Archive: true
Status: Failed
"""


        status = scheduler.get_spoolfile_status(filename)
        self.assertEquals(status, "Failed")

        scheduler.openFile = real_open
        MockFile.counter = 0
        
    def test_get_all_queued_events(self):
        patient = Patient()
        patient.save()

        sendable = InfoMessage(text="Test Message")
        sendable.recipient = patient
        sendable.save()

        self.assertEquals(scheduler.get_all_queued_events().count(), 0)

        schedule1 = ScheduledEvent(sendable=sendable,
                               send_time=datetime.now(),
                               state = "queued")
        schedule1.save()

        self.assertEquals(scheduler.get_all_queued_events().count(), 1)

        schedule2 = ScheduledEvent(sendable=sendable,
                               send_time=(datetime.now() - timedelta(days=1)),
                               state = "sent")
        schedule2.save()

        self.assertTrue(schedule1 in scheduler.get_all_queued_events())
        self.assertFalse(schedule2 in scheduler.get_all_queued_events())

        self.assertEquals(scheduler.get_all_queued_events().count(), 1)

        schedule2.state = "queued"
        schedule2.save()

        self.assertEquals(scheduler.get_all_queued_events().count(), 2)

        schedule1.delete()
        schedule2.delete()


    def test_get_all_due_events(self):
        patient = Patient()
        patient.save()
        
        sendable = InfoMessage(text="Test Message")
        sendable.recipient = patient
        sendable.save()
        
        self.assertEquals(scheduler.get_all_due_events().count(), 1)
        
        schedule1 = ScheduledEvent(sendable=sendable, send_time=datetime.now())
        schedule1.save()
        
        schedule2 = ScheduledEvent(sendable=sendable, 
                               send_time=(datetime.now() - timedelta(days=1)))
        schedule2.save()
        
        schedule3 = ScheduledEvent(sendable=sendable, 
                               send_time=(datetime.now() + timedelta(days=1)))
        schedule3.save()
        
        self.assertEquals(scheduler.get_all_due_events().count(), 3)
        self.assertTrue(schedule1 in scheduler.get_all_due_events())
        self.assertTrue(schedule2 in scheduler.get_all_due_events())
        self.assertFalse(schedule3 in scheduler.get_all_due_events())
        
        schedule4 = ScheduledEvent(sendable=sendable, 
                               send_time=datetime.now(),
                               state = "failed")
        schedule4.save()
        
        schedule5 = ScheduledEvent(sendable=sendable, 
                               send_time=(datetime.now() - timedelta(days=1)),
                               state = "sent")
        schedule5.save()
        
        self.assertEquals(scheduler.get_all_due_events().count(), 3)
        
        schedule1.delete()
        schedule2.delete()
        schedule3.delete()
        schedule4.delete()
        schedule5.delete()
        
