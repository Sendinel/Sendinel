from django.test import TestCase
from datetime import datetime

from sendinel.backend.models import ScheduledEvent, Sendable, InfoMessage, \
                                    HospitalAppointment
from sendinel.backend import scheduler
from sendinel.backend import output

class SchedulerTest(TestCase):    
    
    counter = 0
    fixtures = ['backend']
    
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