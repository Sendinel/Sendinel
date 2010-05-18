from django.test import TestCase
from datetime import datetime, timedelta

from sendinel.backend.models import ScheduledEvent, \
                                    Patient, \
                                    WayOfCommunication, \
                                    get_woc
from sendinel.infoservices.models import InfoMessage
from sendinel.backend import output, scheduler
from sendinel import settings

class SchedulerTest(TestCase):    
    
    counter = 0
    fixtures = ['backend_test']
    
    def test_scheduler(self):     
        
        def scheduled_events_count(state = 'new'):
            
            return scheduler.get_all_due_events().count()

        def queued_events_count(state = 'queued'):
            
            return scheduler.get_all_queued_events().count()

            
        def send(data):
            SchedulerTest.counter += 1

        def mock_process_events():
            for event in scheduler.get_all_queued_events():
                event.state = "done"
                event.save()
        
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
        # exactly two messages were scheduled and had the state "new"

        # we expect only one message to be processed at a time, so
        # the second one has to stay with state "new"
        self.assertEquals(1, SchedulerTest.counter)

        # assert that one event has been processed and one is left
        self.assertEquals(scheduled_events_count(), 1)
        self.assertEquals(queued_events_count(), 1)

        # running the scheduler again should not change the situation,
        # because the fact that the file is still in queue means that
        # has not been processed yet

        scheduler.run(run_only_one_time = True)

        self.assertEquals(1, SchedulerTest.counter)
        self.assertEquals(scheduled_events_count(), 1)
        self.assertEquals(queued_events_count(), 1)

        # let's pretend the Asterisk server has processed the file

        mock_process_events()
        self.assertEquals(queued_events_count(), 0)

        # now the scheduler is run again and should process the one event left

        scheduler.run(run_only_one_time = True)

        # assert that no events with state new exist anymore and one is queued
        self.assertEquals(scheduled_events_count(), 0)
        self.assertEquals(queued_events_count(), 1)
        
        # Now we also process the last event and ensure there's none left
        mock_process_events()
        self.assertEquals(queued_events_count(), 0)

        # Running the scheduler without any due event should be no problem

        scheduler.run(run_only_one_time = True)

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

        # pay attention to the space in the empty line, because in a real
        # file an empty line behaves more like a line with a space in it

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
        
    def test_check_spool_files(self):
        def get_mock_status(filename):
            """
                This is a mock method to represent check_spoolfile_status
                It is told which status to return by using the (in this case
                useless) filename parameter
            """
            return filename

        original_get_spoolfile_status = scheduler.get_spoolfile_status
        scheduler.get_spoolfile_status = get_mock_status

        patient = Patient()
        patient.save()

        sendable = InfoMessage(text="Test Message",
                               way_of_communication = get_woc("sms"))
        sendable.recipient = patient
        sendable.save()

        event1 = ScheduledEvent(sendable=sendable,
                               send_time=datetime.now(),
                               state = "queued",
                               filename = "Completed")
        event1.save()

        event2 = ScheduledEvent(sendable=sendable,
                               send_time=datetime.now(),
                               state = "queued",
                               filename = "Expired")
        event2.save()


        # now: the real testing
               
        scheduler.check_spool_files()
       
        self.assertEquals(ScheduledEvent.objects.get(pk = event1.pk).state, \
                                    "done")

        self.assertEquals(ScheduledEvent.objects.get(pk = event2.pk).state, \
                                    "new")

        event2.filename = "Expired"
        event2.save()

        scheduler.check_spool_files()

        self.assertEquals(ScheduledEvent.objects.get(pk = event2.pk).state, \
                                    "new")

        self.assertEquals(ScheduledEvent.objects.get(pk = event2.pk).retry, 1)

        event2.retry = settings.ASTERISK_RETRY
        event2.filename = "Expired"
        event2.save()

        scheduler.check_spool_files()

        self.assertEquals(ScheduledEvent.objects.get(pk = event2.pk).state, \
                                    "failed")

        event3 = ScheduledEvent(sendable=sendable,
                               send_time=datetime.now(),
                               state = "queued",
                               filename = "Failed")


        event3.save()
        scheduler.check_spool_files()


        self.assertEquals(ScheduledEvent.objects.get(pk = event3.pk).state, \
                                    "failed")



        # change everything back to normal
        event1.delete()
        event2.delete()
        event3.delete()

        scheduler.get_spoolfile_status = original_get_spoolfile_status

    def test_get_all_queued_events(self):
        patient = Patient()
        patient.save()

        sendable = InfoMessage(text="Test Message",
                               way_of_communication = get_woc("sms"))
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
        
        # The fixtures already contain two due events        
        self.assertEquals(scheduler.get_all_due_events().count(), 2)
        
        sendable = InfoMessage(text="Test Message",
                               way_of_communication = get_woc("sms"))
        sendable.recipient = patient
        sendable.save()
        
        schedule1 = ScheduledEvent(sendable=sendable, send_time=datetime.now())
        schedule1.save()
        
        schedule2 = ScheduledEvent(sendable=sendable, 
                               send_time=(datetime.now() - timedelta(days=1)))
        schedule2.save()
        
        schedule3 = ScheduledEvent(sendable=sendable, 
                               send_time=(datetime.now() + timedelta(days=1)))
        schedule3.save()
        
        self.assertEquals(scheduler.get_all_due_events().count(), 4)
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
        
        self.assertEquals(scheduler.get_all_due_events().count(), 4)
        
        schedule1.delete()
        schedule2.delete()
        schedule3.delete()
        schedule4.delete()
        schedule5.delete()
        
